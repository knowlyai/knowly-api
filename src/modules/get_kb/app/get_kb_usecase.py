from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.helpers.errors.usecase_errors import (
    InfrastructureError,
    DatabaseError,
    ConfigurationError
)

load_dotenv()

class GetKbUseCase:
    def __init__(self):
        self._validate_configuration()
        self.ddb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION_NAME")
        )
        self.table = self.ddb.Table(
            os.getenv("DYNAMODB_TABLE_NAME")
        )

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "AWS_REGION_NAME",
            "DYNAMODB_TABLE_NAME"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def get_knowledge_bases(self, user_id: str, kb_id: str = None):
        """
        Busca bases de conhecimento por user_id
        Se kb_id for fornecido, retorna apenas aquela base específica
        """
        try:
            if kb_id:
                # Buscar base específica
                response = self.table.get_item(
                    Key={'kb_id': kb_id}
                )

                if 'Item' not in response:
                    return {"knowledge_bases": []}

                item = response['Item']

                # Verificar se a base pertence ao usuário
                if item.get('user_id') != user_id:
                    return {"knowledge_bases": []}

                # Formatar o item
                formatted_item = self._format_kb_item(item)
                return {"knowledge_bases": [formatted_item]}
            else:
                # Buscar todas as bases do usuário
                response = self.table.scan(
                    FilterExpression='user_id = :user_id',
                    ExpressionAttributeValues={
                        ':user_id': user_id
                    }
                )

                knowledge_bases = []
                for item in response['Items']:
                    formatted_item = self._format_kb_item(item)
                    knowledge_bases.append(formatted_item)

                return {"knowledge_bases": knowledge_bases}

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                raise DatabaseError("Tabela não encontrada no DynamoDB")
            elif error_code == 'ValidationException':
                raise DatabaseError(f"Erro de validação no DynamoDB: {e.response['Error']['Message']}")
            else:
                raise DatabaseError(f"Erro ao consultar DynamoDB: {e.response['Error']['Message']}")
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com AWS: {str(e)}")

    def _format_kb_item(self, item):
        """Formata um item do DynamoDB para o formato de resposta"""
        return {
            "kb_id": item.get('kb_id', ''),
            "name": item.get('name', ''),
            "description": item.get('description', ''),
            "created_at": int(item.get('created_at', 0)),
            "updated_at": int(item.get('updated_at', 0)),
            "status": item.get('status', '')
        }
