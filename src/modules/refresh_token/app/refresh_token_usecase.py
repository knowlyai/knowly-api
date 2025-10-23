import boto3
import os

class RefreshTokenUseCase:
    def __init__(self) -> None:
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        if not self.client_id:
            raise ValueError("COGNITO_CLIENT_ID environment variable must be set and non-empty.")
        self.region = os.getenv("COGNITO_REGION") or os.getenv("REGION") or "us-east-1"
        self.cognito = boto3.client("cognito-idp", region_name=self.region)

    def __call__(self, refresh_token: str) -> dict:
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token
                }
            )
            self.cognito.get_tokens_from_refresh_token()

            if "AuthenticationResult" in response and response["AuthenticationResult"] is not None:
                result = response["AuthenticationResult"]
                return {
                    "id_token": result.get("IdToken"),
                    "access_token": result.get("AccessToken"),
                    "expires_in": result.get("ExpiresIn"),
                    "token_type": result.get("TokenType"),
                }

            return {}

        except Exception as e:
            raise e