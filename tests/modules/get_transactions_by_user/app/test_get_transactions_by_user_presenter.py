import json

from src.modules.get_transactions_by_user.app.get_transactions_by_user_presenter import lambda_handler
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetTransactionsByUserPresenter:

    def test_get_transactions_by_user_success(self):
        repo = UserRepositoryMock()
        first_user = repo.users[0]
        valid_user_id = first_user.user_id

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
        assert isinstance(body, dict)
        assert "transactions" in body
        assert "message" in body
        assert body["message"] == "Transações do usuário foram retornadas"
        assert isinstance(body["transactions"], list)
        assert len(body["transactions"]) == 3

        # Verificar estrutura das transações
        for transaction in body["transactions"]:
            assert isinstance(transaction, dict)
            assert "tran_id" in transaction
            assert "user_id" in transaction
            assert "value" in transaction
            assert "create_date" in transaction
            assert "plan" in transaction
            assert transaction["user_id"] == valid_user_id

    def test_get_transactions_by_user_missing_user_id(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
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
        assert response["statusCode"] == 400
        assert "O campo user_id está faltando" in response["body"]

    def test_get_transactions_by_user_user_not_found(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "user_id=nonexistent-user-id",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
                "user_id": "nonexistent-user-id"
            },
            "requestContext": {},
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 404
        assert "Nenhum item encontrado para user_id" in response["body"]

    def test_get_transactions_by_user_empty_transactions(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "user_id=5042b518-83ca-4cbf-84fc-c992da2506e5",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
                "user_id": "5042b518-83ca-4cbf-84fc-c992da2506e5"
            },
            "requestContext": {},
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
        assert len(body["transactions"]) == 0

    def test_get_transactions_by_user_invalid_user_id_type(self):
        # Testando quando user_id é passado como número em query parameter
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "user_id=123",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
                "user_id": "123"  # Query parameters são sempre strings no Lambda
            },
            "requestContext": {},
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 404  # user_id "123" não existe
        assert "Nenhum item encontrado para user_id" in response["body"]
