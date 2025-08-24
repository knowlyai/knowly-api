from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.helpers.errors.usecase_errors import (
    InfrastructureError,
    DatabaseError,
    ConfigurationError,
    ExternalServiceError
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
        self.s3 = boto3.client(
            "s3",
            region_name=os.getenv("AWS_REGION_NAME")
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
        user_id = item.get('user_id', '')
        kb_id = item.get('kb_id', '')

        # Buscar arquivos e tamanho total do S3
        files, total_size_mb = self._get_kb_files_and_size(user_id, kb_id)

        return {
            "kb_id": kb_id,
            "name": item.get('name', ''),
            "display_name": item.get('display_name', ''),
            "description": item.get('description', ''),
            "created_at": int(item.get('created_at', 0)),
            "updated_at": int(item.get('updated_at', 0)),
            "status": item.get('status', ''),
            "files": files,
            "total_size_mb": total_size_mb
        }

    def _get_kb_files_and_size(self, user_id: str, kb_id: str):
        """
        Busca arquivos do S3 para uma base de conhecimento específica
        Retorna lista de URLs dos arquivos e tamanho total em MB
        """
        try:
            bucket_name = 'knowly-knowledge-bases-files'
            region = os.getenv("AWS_REGION_NAME", "us-east-1")

            prefix = f"{user_id}/{kb_id}/"

            files = []
            total_size_bytes = 0

            # Listar objetos com o prefixo específico
            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        size = obj['Size']

                        # Extrair apenas o nome do arquivo (remove o prefixo)
                        filename = key.replace(prefix, '')

                        # Gerar URL do arquivo no formato HTTPS do S3
                        # URL encode do filename para caracteres especiais
                        import urllib.parse
                        encoded_filename = urllib.parse.quote(filename, safe='')
                        file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{user_id}/{kb_id}/{encoded_filename}"

                        files.append({
                            "filename": filename,
                            "url": file_url,
                            "size_bytes": size
                        })

                        total_size_bytes += size

            # Converter bytes para MB
            total_size_mb = round(total_size_bytes / (1024 * 1024), 2)

            return files, total_size_mb

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                # Se o bucket não existir, retornar lista vazia
                return [], 0.0
            elif error_code == 'AccessDenied':
                raise ExternalServiceError("S3", "Acesso negado ao listar arquivos do bucket S3")
            else:
                raise ExternalServiceError("S3", f"Erro ao listar arquivos do S3: {e.response['Error']['Message']}")
        except Exception as e:
            # Em caso de erro, retornar lista vazia para não quebrar a resposta
            return [], 0.0
