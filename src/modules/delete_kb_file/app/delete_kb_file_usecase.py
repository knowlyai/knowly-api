from dotenv import load_dotenv
import os
import boto3

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.getenv('AWS_REGION_NAME')
)

class DeleteKbFileUseCase:
    def __call__(self, bucket: str, user_id: str, kb_id: str, file_name: str) -> str:
        """
        Deleta um arquivo do S3 no caminho user_id/kb_id/file_name
        """
        key = f"{user_id}/{kb_id}/{file_name}"
        try:
            s3.delete_object(Bucket=bucket, Key=key)
            return f"Arquivo '{file_name}' deletado com sucesso do bucket '{bucket}'."
        except Exception as e:
            raise Exception(f"Erro ao deletar arquivo: {str(e)}")

