import json

from src.modules.update_subscription.app.update_subscription_presenter import lambda_handler


class Test_UpdateSubscriptionPresenter:

    def test_update_subscription(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {},
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
                "time": "01/Jun/2025:12:00:00 +0000",
                "timeEpoch": 1717252800000
            },
            "body": json.dumps({
                "id": "sub-1",
                "new_plan": "GOLD"
            }),
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["id"] == "sub-1"
        assert body["previous_plan"] == "SILVER"
        assert body["new_plan"] == "GOLD"
        assert "update_date" in body  
        assert body["message"] == "subscription updated successfully"