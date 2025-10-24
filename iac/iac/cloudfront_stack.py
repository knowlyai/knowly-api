from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
)
from constructs import Construct


class CloudFrontStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, bucket: s3.Bucket, stage: str = "TEST", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Origin Access Identity para o CloudFront acessar o bucket privado
        self.oai = cloudfront.OriginAccessIdentity(
            self, "KnowlyOAI",
            comment=f"OAI for Knowly Knowledge Base files - {stage}"
        )

        # Conceder permissão de leitura ao OAI
        bucket.grant_read(self.oai)

        # Distribuição do CloudFront
        self.distribution = cloudfront.Distribution(
            self, "KnowlyDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(
                    bucket,
                    origin_access_identity=self.oai
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
            ),
            enabled=True,
            comment=f"Knowly Knowledge Base Files Distribution - {stage}",
        )

        self.distribution_domain_name = self.distribution.distribution_domain_name
        self.distribution_id = self.distribution.distribution_id

