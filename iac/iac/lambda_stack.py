from aws_cdk import (
    aws_lambda as lambda_,
    Duration
)
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, AuthorizationType, CognitoUserPoolsAuthorizer
from constructs import Construct


class LambdaStack(Construct):
    functions_that_need_dynamo_permissions = []

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict, user_pool) -> None:
        super().__init__(scope, "KnowlyApiLambdas")

        # Authorizer Cognito (User Pool)
        self.authorizer = CognitoUserPoolsAuthorizer(
            self,
            "KnowlyCognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )

        self.lambda_layer = lambda_.LayerVersion(self, "Knowly_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_13]
                                                 )

        # ---- User Resource ----
        user_resource = api_gateway_resource.add_resource("user")

        self.get_user_function = self._add_method_to_resource(
            module_name="get_user",
            http_method="GET",
            target_resource=user_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        self.create_user_function = self._add_method_to_resource(
            module_name="create_user",
            http_method="POST",
            target_resource=user_resource,
            environment_variables=environment_variables
        )

        self.delete_user_function = self._add_method_to_resource(
            module_name="delete_user",
            http_method="DELETE",
            target_resource=user_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        self.update_user_function = self._add_method_to_resource(
            module_name="update_user",
            http_method="PATCH",
            target_resource=user_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        # ---- Auth Resource ----
        auth_resource = api_gateway_resource.add_resource("auth")

        self.get_token_function = self._add_method_to_resource(
            module_name="get_token",
            http_method="POST",
            target_resource=auth_resource,
            environment_variables=environment_variables
        )

        # ---- Transactions Resource ----
        transactions_resource = api_gateway_resource.add_resource("transactions")

        self.get_transactions_by_user_function = self._add_method_to_resource(
            module_name="get_transactions_by_user",
            http_method="GET",
            target_resource=transactions_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        # ---- Subscriptions Resource ----
        subscriptions_resource = api_gateway_resource.add_resource("subscriptions")

        self.get_subscriptions_by_user_function = self._add_method_to_resource(
            module_name="get_subscriptions_by_user",
            http_method="GET",
            target_resource=subscriptions_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        self.update_subscription_function = self._add_method_to_resource(
            module_name="update_subscription",
            http_method="PUT",
            target_resource=subscriptions_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        # ---- Knowledge Base Resource ----
        kb_resource = api_gateway_resource.add_resource("kb")

        self.create_kb_function = self._add_method_to_resource(
            module_name="create_kb",
            http_method="POST",
            target_resource=kb_resource,
            environment_variables=environment_variables,
            requires_authorizer=True
        )

        self.functions_that_need_dynamo_permissions = [self.get_user_function, self.create_user_function,
                                                self.delete_user_function, self.update_user_function,
                                                self.get_transactions_by_user_function, self.get_subscriptions_by_user_function,
                                                self.update_subscription_function]

    def _add_method_to_resource(
            self,
            *,
            module_name: str,
            http_method: str,
            target_resource: Resource,
            environment_variables: dict,
            requires_authorizer: bool = False
      ) -> lambda_.Function:
        fn = lambda_.Function(
            self,
            module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15),
        )

        integration = LambdaIntegration(fn)
        if requires_authorizer:
            target_resource.add_method(
                http_method,
                integration,
                authorization_type=AuthorizationType.COGNITO,
                authorizer=self.authorizer
            )
        else:
            target_resource.add_method(http_method, integration)
        return fn
