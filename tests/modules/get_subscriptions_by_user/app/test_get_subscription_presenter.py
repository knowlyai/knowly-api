import json

from src.modules.get_subscriptions_by_user.app.get_subscriptions_by_user_presenter import lambda_handler


class TestGetSubscriptionPresenter:

    def test_get_subscription(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "id=sub-1",
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
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
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
        assert body['subscriptions'][0]["sub_id"] == "fbf1af68-33c1-4f41-9290-5823158397a8"
        assert body['subscriptions'][0]["user_id"] == "fdddafb9-687a-4982-a025-54fb12671932"
        assert body['subscriptions'][0]["previous_plan"] == "Bronze"
        assert body['subscriptions'][0]["new_plan"] == "Gold"
        assert body['subscriptions'][0]["update_date"] == 1700000000
        assert "message" in body and isinstance(body["message"], str)
