from dotenv import load_dotenv
import os
import uuid
import boto3

load_dotenv()

bedrock = boto3.client(
    "bedrock-agent",
    region_name=os.getenv('AWS_REGION_NAME')
)


class SyncKbUseCase:
    @staticmethod
    def _get_ds_name(kb_id: str) -> str:
        return f"s3-ds-{kb_id}"

    @staticmethod
    def _create_or_get_data_source(bucket_name: str, user_id: str, kb_id: str) -> str:
        bucket_arn = f"arn:aws:s3:::{bucket_name}"
        ds_name = f"s3-ds-{kb_id}"
        prefix = f"{user_id}/{kb_id}"
        for page in bedrock.get_paginator("list_data_sources").paginate(knowledgeBaseId=kb_id):
            for ds in page["dataSourceSummaries"]:
                if ds["name"] == ds_name:
                    return ds["dataSourceId"]

        resp = bedrock.create_data_source(
            clientToken=str(uuid.uuid4()),
            knowledgeBaseId=kb_id,
            name=ds_name,
            description="Arquivos enviados pelo usuário via prefixo S3",
            dataSourceConfiguration={
                "type": "S3",
                "s3Configuration": {
                    "bucketArn": bucket_arn,
                    "inclusionPrefixes": [prefix]
                },
            },
            vectorIngestionConfiguration={
                "chunkingConfiguration": {
                    "chunkingStrategy": "SEMANTIC",
                    "fixedSizeChunkingConfiguration": {
                        "maxTokens": 800,
                        "overlapPercentage": 20
                    },
                    "semanticChunkingConfiguration": {
                        "breakpointPercentileThreshold": 95,
                        "bufferSize": 1,
                        "maxTokens": 800
                    }
                }
            }
        )
        return resp["dataSource"]["dataSourceId"]

    @staticmethod
    def _start_ingestion_and_wait(kb_id: str, ds_id: str):
        job = bedrock.start_ingestion_job(
            clientToken=str(uuid.uuid4()),
            knowledgeBaseId=kb_id,
            dataSourceId=ds_id,
        )["ingestionJob"]

        job_id = job["ingestionJobId"]
        return f"Job {job_id} iniciado…"

    def __call__(self, bucket_name: str, user_id: str, kb_id: str) -> str:
        ds_id = self._create_or_get_data_source(bucket_name, user_id, kb_id)
        resp = self._start_ingestion_and_wait(kb_id, ds_id)
        return resp
