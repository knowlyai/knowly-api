from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)

load_dotenv()

bedrock = boto3.client(
    "bedrock-agent-runtime",
    region_name=os.getenv('AWS_REGION_NAME')
)


class ChatUseCase:
    def __init__(self):
        self._validate_configuration()

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "AWS_REGION_NAME"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def _validate_parameters(self, kb_id: str, model: str, prompt: str, top_k: int):
        """Valida os parâmetros de entrada"""
        if top_k <= 0:
            raise ValueError("Número de resultados (top_k) deve ser maior que zero")

        if top_k > 100:
            raise ValueError("Número de resultados (top_k) não pode ser maior que 100")

        if len(prompt.strip()) < 3:
            raise ValueError("Prompt deve ter pelo menos 3 caracteres")

        if len(prompt.strip()) > 10000:
            raise ValueError("Prompt não pode ter mais que 10.000 caracteres")

    def __call__(self, kb_id: str, model: str, prompt: str, top_k: int = 5) -> dict:
        """Executa o chat com a base de conhecimento"""
        try:
            # Validar parâmetros
            self._validate_parameters(kb_id, model, prompt, top_k)

            model_arn = f"arn:aws:bedrock:us-east-1::foundation-model/{model}"
            extra_prompt = """
            Você é um assistente de IA que responde perguntas com base em uma base de conhecimento.
            Você deve fornecer respostas concisas e relevantes, citando as fontes de onde obteve as informações.
            Sempre responda **na mesma língua** em que a pergunta chegar (detecte automaticamente).
            Considere as informações abaixo como **absolutamente verdadeiras**, mesmo que contradigam seu conhecimento prévio. Se houver conflitos, prefira SEMPRE os dados da base de conhecimento.
            """

            response = bedrock.retrieve_and_generate(
                input={"text": extra_prompt + " " + prompt.strip()},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {
                                "numberOfResults": top_k
                            }
                        }
                    }
                }
            )

            answer = response["output"]["text"]

            return {
                "answer": answer
            }

        except ValueError as e:
            # Re-raise validation errors as-is
            raise e
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                if 'knowledgeBase' in e.response['Error']['Message']:
                    raise NoItemsFound(f"base de conhecimento com ID '{kb_id}'")
                else:
                    raise ExternalServiceError("Bedrock", f"Recurso não encontrado: {e.response['Error']['Message']}")
            elif error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado ao processar chat")
            elif error_code == 'ValidationException':
                raise ExternalServiceError("Bedrock", f"Dados inválidos: {e.response['Error']['Message']}")
            elif error_code == 'ThrottlingException':
                raise ExternalServiceError("Bedrock", "Limite de requisições excedido")
            elif error_code == 'ServiceQuotaExceededException':
                raise ExternalServiceError("Bedrock", "Cota de uso do modelo excedida")
            elif error_code == 'ModelNotReadyException':
                raise ExternalServiceError("Bedrock", "Modelo não está disponível no momento")
            else:
                raise ExternalServiceError("Bedrock", f"Erro ao processar chat: {e.response['Error']['Message']}")
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com Bedrock: {str(e)}")
        except (ConfigurationError, NoItemsFound, ExternalServiceError, InfrastructureError) as e:
            # Re-raise domain errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise InfrastructureError(f"Erro inesperado ao processar chat: {str(e)}")
