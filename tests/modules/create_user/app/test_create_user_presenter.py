import json
import time

from src.modules.create_user.app.create_user_presenter import lambda_handler


class TestCreateUserPresenter:

    def test_create_user_success(self):
        """Teste de sucesso completo com todos os campos obrigatórios"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "rawQueryString": "",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "test-api",
                "domainName": "test.lambda-url.us-west-2.on.aws",
                "http": {
                    "method": "POST",
                    "path": "/create-user",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1",
                    "userAgent": "test-agent"
                },
                "requestId": "test-request-id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "01/Jan/2025:00:00:00 +0000",
                "timeEpoch": int(time.time())
            },
            "body": json.dumps({
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "João Silva Santos",
                "email": "joao.silva@teste.com",
                "cellphone": "11987654321",
                "p_type": "PF",
                "cpf_cnpj": "71214584110",
                "address": "Rua das Flores, 123",
                "cep": "01234567",
                "birthdate": int(time.time() - (25 * 365.25 * 24 * 60 * 60)),  # 25 anos
                "plan": "Bronze"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        response_body = json.loads(response["body"])
        assert response_body["message"] == "Usuário criado com sucesso"
        assert response_body["user"]["user_id"] == "550e8400-e29b-41d4-a716-446655440000"
        assert response_body["user"]["name"] == "João Silva Santos"
        assert response_body["user"]["email"] == "joao.silva@teste.com"

    def test_create_user_success_without_birthdate(self):
        """Teste de sucesso sem birthdate (campo opcional)"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": "650e8400-e29b-41d4-a716-446655440001",
                "name": "Maria Oliveira",
                "email": "maria@teste.com",
                "cellphone": "11987654322",
                "p_type": "PF",
                "cpf_cnpj": "98765432100",
                "address": "Av. Paulista, 1000",
                "cep": "01310100",
                "plan": "Silver"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        response_body = json.loads(response["body"])
        assert response_body["message"] == "Usuário criado com sucesso"
        assert response_body["user"]["user_id"] == "650e8400-e29b-41d4-a716-446655440001"

    def test_create_user_person_juridica(self):
        """Teste com pessoa jurídica"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": "750e8400-e29b-41d4-a716-446655440002",
                "name": "TechCorp Soluções LTDA",
                "email": "contato@techcorp.com",
                "cellphone": "1133334444",
                "p_type": "PJ",
                "cpf_cnpj": "60.749.736/0001-99",
                "address": "Rua dos Desenvolvedores, 500",
                "cep": "04567890",
                "plan": "Gold"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        response_body = json.loads(response["body"])
        assert response_body["user"]["p_type"] == "PJ"
        assert response_body["user"]["plan"] == "Gold"

    def test_create_user_missing_required_field(self):
        """Teste de erro: campo obrigatório ausente"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "name": "Teste Incompleto",
                "email": "teste@incompleto.com",
                "cellphone": "11999999999",
                "p_type": "PF",
                "cpf_cnpj": "12345678901",
                "address": "Rua Teste, 123",
                "cep": "01234567",
                "plan": "Bronze"
                # user_id ausente
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert "user_id" in response["body"]

    def test_create_user_invalid_enum_p_type(self):
        """Teste de erro: enum p_type inválido"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": "850e8400-e29b-41d4-a716-446655440003",
                "name": "Teste Enum Inválido",
                "email": "teste@enum.com",
                "cellphone": "11999999999",
                "p_type": "INVALID_TYPE",
                "cpf_cnpj": "12345678901",
                "address": "Rua Teste, 123",
                "cep": "01234567",
                "plan": "Bronze"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert "p_type" in response["body"]

    def test_create_user_invalid_enum_plan(self):
        """Teste de erro: enum plan inválido"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": "950e8400-e29b-41d4-a716-446655440004",
                "name": "Teste Plan Inválido",
                "email": "teste@plan.com",
                "cellphone": "11999999999",
                "p_type": "PF",
                "cpf_cnpj": "12345678901",
                "address": "Rua Teste, 123",
                "cep": "01234567",
                "plan": "INVALID_PLAN"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert "plan" in response["body"]

    def test_create_user_wrong_type_parameter(self):
        """Teste de erro: tipo de parâmetro incorreto"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": 123456,  # Deveria ser string
                "name": "Teste Tipo Incorreto",
                "email": "teste@tipo.com",
                "cellphone": "11999999999",
                "p_type": "PF",
                "cpf_cnpj": "12345678901",
                "address": "Rua Teste, 123",
                "cep": "01234567",
                "plan": "Bronze"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert "user_id" in response["body"]

    def test_create_user_minor_age_error(self):
        """Teste de erro: usuário menor de idade"""
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/create-user",
            "headers": {
                "content-type": "application/json"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/create-user"
                }
            },
            "body": json.dumps({
                "user_id": "a50e8400-e29b-41d4-a716-446655440005",
                "name": "Menor de Idade",
                "email": "menor@teste.com",
                "cellphone": "11999999999",
                "p_type": "PF",
                "cpf_cnpj": "12345678901",
                "address": "Rua Teste, 123",
                "cep": "01234567",
                "birthdate": int(time.time() - (16 * 365.25 * 24 * 60 * 60)),  # 16 anos
                "plan": "Bronze"
            }),
            "isBase64Encoded": False
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert "age" in response["body"] or "menor" in response["body"].lower()
