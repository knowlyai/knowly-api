import os

from aws_cdk import (
    aws_cognito, RemovalPolicy
)
from constructs import Construct


class CognitoStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_ref_name = os.environ.get("GITHUB_REF_NAME")
        # Gera prefixo de domínio (precisa ser único na região). Substitui caracteres inválidos.
        domain_prefix_base = f"knowly-{github_ref_name}" if github_ref_name else "knowly"
        safe_domain_prefix = ''.join(c.lower() if c.isalnum() or c == '-' else '-' for c in domain_prefix_base)[:63]

        self.user_pool = aws_cognito.UserPool(self, f"knowly_user_pool_{github_ref_name}",
                                                removal_policy=RemovalPolicy.DESTROY,
                                                self_sign_up_enabled=True,
                                                auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
                                                email=aws_cognito.UserPoolEmail.with_cognito(),
                                                user_verification=aws_cognito.UserVerificationConfig(
                                                    email_subject="Bem vindo ao sistema de autenticação Knowly",
                                                    email_body="Olá! \n\nObrigado por se registrar no Knowly. \n\n Clique no link abaixo para verificar seu e-mail e ativar sua conta: \n\n {##Verify Email##} \n\n Se você não se registrou no Knowly, por favor ignore este e-mail.",
                                                    email_style=aws_cognito.VerificationEmailStyle.LINK),
                                                standard_attributes=aws_cognito.StandardAttributes(
                                                    email=aws_cognito.StandardAttribute(
                                                        required=True,
                                                        mutable=True
                                                    ),
                                                    phone_number=aws_cognito.StandardAttribute(
                                                        required=False,
                                                        mutable=True
                                                    ),
                                                    fullname=aws_cognito.StandardAttribute(
                                                        required=True,
                                                        mutable=True
                                                    ),
                                                ),
                                              sign_in_aliases=aws_cognito.SignInAliases(
                                                    email=True,
                                              ),
                                              )
        # Adiciona domínio necessário para envio de email de verificação com LINK
        self.user_pool.add_domain("UserPoolDomain", cognito_domain=aws_cognito.CognitoDomainOptions(
            domain_prefix=safe_domain_prefix
        ))

        self.client = self.user_pool.add_client(f"knowly_user_pool_client_{github_ref_name}",
                                                auth_flows=aws_cognito.AuthFlow(
                                                    admin_user_password=True,
                                                    custom=True,
                                                    user_password=True,
                                                    user_srp=True
                                                ),
                                                generate_secret=False)