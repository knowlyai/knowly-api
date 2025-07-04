import json

from src.modules.delete_user.app.delete_user_presenter import lambda_handler


class TestDeleteUserPresenter:

    def test_delete_user(self):
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
                "parameter1": "1"
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
            "body": '{"user_id": "fdddafb9-687a-4982-a025-54fb12671932"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        expected = {'user': {
            'user_id': 'fdddafb9-687a-4982-a025-54fb12671932',
            'name': 'Enzo Sakamoto',
            'email': 'saka@moto.com',
            'cellphone': '11 95320-2088',
            'p_type': 'PF',
            'cpf_cnpj': '37973280871',
            'address': 'Rua das Flores, 123',
            'cep': '04111111',
            'plan': 'Gold',
            'creation_date': 1749079322,
            'update_date': 1749079323,
            'birthdate': 1022368922
        },
            'message': 'O usuário foi excluído com sucesso'}

        assert json.loads(response["body"]) == expected
        assert response["statusCode"] == 200
