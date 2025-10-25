import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.domain.repositories.keys_repository_interface import IKeysRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)

envs = Environments.get_envs()

bedrock = boto3.client(
    "bedrock-agent-runtime",
    region_name=envs.region,
)


class ChatUseCase:
    def __init__(self, keys_repository: IKeysRepository):
        self.keys_repository = keys_repository
        self._validate_configuration()

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "REGION"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def _validate_parameters(self, kb_key: str, model: str, prompt: str, top_k: int):
        """Valida os parâmetros de entrada"""
        if not kb_key or len(kb_key.strip()) == 0:
            raise ValueError("kb_key é obrigatória")

        if top_k <= 0:
            raise ValueError("Número de resultados (top_k) deve ser maior que zero")

        if top_k > 100:
            raise ValueError("Número de resultados (top_k) não pode ser maior que 100")

        if len(prompt.strip()) < 3:
            raise ValueError("Prompt deve ter pelo menos 3 caracteres")

        if len(prompt.strip()) > 10000:
            raise ValueError("Prompt não pode ter mais que 10.000 caracteres")

    def __call__(self, kb_key: str, model: str, prompt: str, top_k: int = 5) -> dict:
        """Executa o chat com a base de conhecimento"""
        kb_id = None  # Inicializa para evitar referência antes de atribuição
        try:
            # Validar parâmetros
            self._validate_parameters(kb_key, model, prompt, top_k)

            # Buscar kb_id pela kb_key
            kb_id = self.keys_repository.get_kb_id_by_key(kb_key)

            model_arn = f"arn:aws:bedrock:us-east-1::foundation-model/{model}"
            extra_prompt = """
            Regras de comportamento:
            Idioma: responda no mesmo idioma da pergunta (detecção automática).
            Prioridade das fontes: trate o conteúdo da base como verdade canônica. Em caso de conflito com conhecimento prévio, siga a base.
            Escopo: não responda nada que não esteja sustentado pela base. Se faltar evidência, diga que não encontrou na base e, se fizer sentido, peça detalhes adicionais.
            Precisão: não invente nomes, números, datas, citações ou passos. Se algo estiver ambíguo ou incompleto, explicite a incerteza.
            Concisão: respostas curtas, diretas e úteis. Evite verbosidade.
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
