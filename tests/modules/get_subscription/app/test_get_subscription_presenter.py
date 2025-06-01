import json
import pytest

from src.modules.get_subscription.app.get_subscription_presenter import lambda_handler


class Test_GetSubscriptionPresenter:

    def test_get_subscription(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "id=sub-1",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {
                "id": "sub-1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {},
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
        assert body["id"] == "sub-1"
        assert body["user_id"] == "user-1"
        assert body["previous_plan"] == "BRONZE"
        assert body["new_plan"] == "SILVER"
        assert body["update_date"] == 1700000000
        assert "message" in body and isinstance(body["message"], str)