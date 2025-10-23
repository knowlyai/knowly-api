import os

from aws_cdk import (
    aws_cognito, RemovalPolicy, Duration
)
from constructs import Construct

SES_REGION = "us-east-1"
FROM_EMAIL = "knowly.dev.br"
FROM_NAME  = "no-reply@knowly.dev.br"

class CognitoStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_ref_name = os.environ.get("GITHUB_REF_NAME")
        domain_prefix_base = f"knowly-{github_ref_name}" if github_ref_name else "knowly"
        safe_domain_prefix = ''.join(
            c.lower() if c.isalnum() or c == '-' else '-'
            for c in domain_prefix_base
        )[:63]

        self.user_pool = aws_cognito.UserPool(
            self, f"knowly_user_pool_{github_ref_name}",
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=True,
            auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
            email=aws_cognito.UserPoolEmail.with_cognito(),
            # email=aws_cognito.UserPoolEmail.with_ses(
            #     from_email=FROM_EMAIL,
            #     from_name=FROM_NAME,
            #     ses_region=SES_REGION
            # ),
            user_verification=aws_cognito.UserVerificationConfig(
                email_subject="Bem vindo ao sistema de autenticação Knowly",
                email_body=(
                    "Olá!\n\nObrigado por se registrar no Knowly.\n\n"
                    "Clique no link abaixo para verificar seu e-mail e ativar sua conta:\n\n"
                    "{##Verify Email##}\n\n"
                    "Se você não se registrou no Knowly, por favor ignore este e-mail."
                ),
                email_style=aws_cognito.VerificationEmailStyle.LINK,
            ),
            standard_attributes=aws_cognito.StandardAttributes(
                email=aws_cognito.StandardAttribute(required=True, mutable=True),
                phone_number=aws_cognito.StandardAttribute(required=False, mutable=True),
                fullname=aws_cognito.StandardAttribute(required=True, mutable=True),
            ),
            sign_in_aliases=aws_cognito.SignInAliases(email=True),
        )

        self.user_pool.add_domain(
            "UserPoolDomain",
            cognito_domain=aws_cognito.CognitoDomainOptions(domain_prefix=safe_domain_prefix),
        )

        self.client = self.user_pool.add_client(
            f"knowly_user_pool_client_{github_ref_name}",
            auth_flows=aws_cognito.AuthFlow(
                admin_user_password=True,
                custom=True,
                user_password=True,
                user_srp=True,
            ),
            generate_secret=False,
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(7),
        )

#redeploy