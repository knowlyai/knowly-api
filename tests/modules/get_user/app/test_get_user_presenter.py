import json
from dataclasses import dataclass
import pytest

from src.modules.get_user.app.get_user_presenter import lambda_handler


class TestGetUserPresenter:

    def test_get_user(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "user_id": "fdddafb9-687a-4982-a025-54fb12671932"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": "Hello from client!",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])['user']["name"] == "Enzo Sakamoto"
        assert json.loads(response["body"])['user']["email"] == "saka@moto.com"
        assert json.loads(response["body"])['user']["cellphone"] == "11 95320-2088"
        assert json.loads(response["body"])['user']["p_type"] == "PF"
        assert json.loads(response["body"])['user']["cpf_cnpj"] == "37973280871"
        assert json.loads(response["body"])['user']["address"] == "Rua das Flores, 123"
        assert json.loads(response["body"])['user']["cep"] == "04111111"
        assert json.loads(response["body"])['user']["plan"] == "Gold"
        assert json.loads(response["body"])['user']["creation_date"] == 1749079322
        assert json.loads(response["body"])['user']["update_date"] == 1749079323
        assert json.loads(response["body"])['user']["birthdate"] == 1022368922
        assert json.loads(response["body"])['user']["user_id"] == "fdddafb9-687a-4982-a025-54fb12671932"
        assert json.loads(response["body"])['message'] == "the user was retrieved successfully"

