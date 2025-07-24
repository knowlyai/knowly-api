from aws_cdk import (
    aws_lambda as lambda_,
    Duration
)
from aws_cdk.aws_apigateway import Resource, LambdaIntegration
from constructs import Construct


class LambdaStack(Construct):
    functions_that_need_dynamo_permissions = []

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict) -> None:
        super().__init__(scope, "KnowlyApiLambdas")

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
            environment_variables=environment_variables
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
            environment_variables=environment_variables
        )

        self.update_user_function = self._add_method_to_resource(
            module_name="update_user",
            http_method="PATCH",
            target_resource=user_resource,
            environment_variables=environment_variables
        )

        # ---- Transactions Resource ----
        transactions_resource = api_gateway_resource.add_resource("transactions")

        self.get_transactions_by_user_function = self._add_method_to_resource(
            module_name="get_transactions_by_user",
            http_method="GET",
            target_resource=transactions_resource,
            environment_variables=environment_variables
        )

        # ---- Subscriptions Resource ----
        subscriptions_resource = api_gateway_resource.add_resource("subscriptions")

        self.get_subscriptions_by_user_function = self._add_method_to_resource(
            module_name="get_subscriptions_by_user",
            http_method="GET",
            target_resource=subscriptions_resource,
            environment_variables=environment_variables
        )

        self.update_subscription_function = self._add_method_to_resource(
            module_name="update_subscription",
            http_method="PUT",
            target_resource=subscriptions_resource,
            environment_variables=environment_variables
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
            environment_variables: dict
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

        target_resource.add_method(http_method, LambdaIntegration(fn))
        return fn
