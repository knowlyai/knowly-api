import json
import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_presenter import lambda_handler
from src.shared.infra.repositories.transaction_repository_mock import TransactionRepositoryMock


class Test_GetTransactionsByUserPresenter:

    def test_get_transactions_by_user_success(self):
        repo = TransactionRepositoryMock()
        first_tx = repo.transactions[0]
        valid_user_id = first_tx.user_id

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": f"user_id={valid_user_id}",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
                "user_id": valid_user_id
            },
            "requestContext": {
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
        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert isinstance(body, list)
        assert any(tx["user_id"] == valid_user_id for tx in body)
        sample = body[0]
        assert "id" in sample and isinstance(sample["id"], str)
        assert "plan" in sample and isinstance(sample["plan"], str)
        assert "value" in sample and isinstance(sample["value"], float)
        assert "create_date" in sample and isinstance(sample["create_date"], int)

    def test_get_transactions_by_user_missing_user_id(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {},
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 400