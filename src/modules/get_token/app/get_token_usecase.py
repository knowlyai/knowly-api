import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError


class GetTokenUseCase:
    def __init__(self) -> None:
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.region = os.getenv("COGNITO_REGION") or os.getenv("REGION") or "us-east-1"
        self.cognito = boto3.client("cognito-idp", region_name=self.region)

    def __call__(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password
                }
            )

            if "AuthenticationResult" in response and response["AuthenticationResult"] is not None:
                result = response["AuthenticationResult"]
                return {
                    "id_token": result.get("IdToken"),
                    "access_token": result.get("AccessToken"),
                    "refresh_token": result.get("RefreshToken"),
                    "expires_in": result.get("ExpiresIn"),
                    "token_type": result.get("TokenType"),
                }

            return {
                "challenge_name": response.get("ChallengeName"),
                "session": response.get("Session"),
            }

        except ClientError as e:
            raise e
