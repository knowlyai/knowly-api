import json

from src.modules.get_transactions_by_user.app.get_transactions_by_user_presenter import lambda_handler


class TestGetTransactionsByUserPresenter:

    def test_get_transactions_by_user_success(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims": {
                        "sub": "fdddafb9-687a-4982-a025-54fb12671932",
                        "name": "Enzo Sakamoto",
                        "email": "saka@moto.com"
                    }
                },
                "domainName": "<url-id>.lambda-url.region.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "GET",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "01/Jun/2025:12:00:00 +0000",
                "timeEpoch": 1717252800000
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert isinstance(body, dict)
        assert "transactions" in body
        assert "message" in body
        assert body["message"] == "Transações do usuário foram retornadas"
        assert isinstance(body["transactions"], list)
        assert len(body["transactions"]) == 3
        for transaction in body["transactions"]:
            assert transaction["user_id"] == "fdddafb9-687a-4982-a025-54fb12671932"

    def test_get_transactions_by_user_missing_requester_user(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {  # sem authorizer.claims
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {},
                "domainName": "<url-id>.lambda-url.region.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "GET",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "01/Jun/2025:12:00:00 +0000",
                "timeEpoch": 1717252800000
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400
        assert "requester_user" in response["body"]
