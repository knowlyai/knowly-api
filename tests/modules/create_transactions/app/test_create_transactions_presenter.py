import os
os.environ["STAGE"] = "TEST"

import json
from src.modules.create_transactions.app.create_transactions_presenter import lambda_handler


class TestCreateTransactionsPresenter:

    def test_create_transaction_success(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/transactions",
            "rawQueryString": "",
            "cookies": [],
            "headers": {"content-type": "application/json"},
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
                "http": {
                    "method": "POST",
                    "path": "/transactions",
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
            "body": json.dumps({
                "tran_id": "11111111-2222-3333-4444-555555555555",
                "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
                "plan": "Gold",
                "value": 49.9,
                "create_date": 1724630400
            }),
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 201

        body = json.loads(response["body"])
        assert "transaction" in body
        assert "message" in body
        assert body["message"] == "Transação criada com sucesso"
        assert body["transaction"]["tran_id"] == "11111111-2222-3333-4444-555555555555"
        assert body["transaction"]["user_id"] == "fdddafb9-687a-4982-a025-54fb12671932"
        assert body["transaction"]["plan"] == "Gold"
        assert body["transaction"]["value"] == 49.9
        assert body["transaction"]["create_date"] == 1724630400

    def test_create_transaction_missing_tran_id(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/transactions",
            "rawQueryString": "",
            "cookies": [],
            "headers": {"content-type": "application/json"},
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
                "http": {
                    "method": "POST",
                    "path": "/transactions",
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
            "body": json.dumps({
                "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
                "plan": "Gold",
                "value": 10.0
            }),
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400
        assert "O campo tran_id está faltando" in response["body"]