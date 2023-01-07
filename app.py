import pathlib
import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as deployment

app = cdk.App()
stack = cdk.Stack(app, "cdk-cloud-front-s3-oai-stack")

# バケットを作成する
bucket = s3.Bucket(stack, "Bucket")
deployment.BucketDeployment(
    stack,
    "BucketDeployment",
    sources=[deployment.Source.asset("html")],
    destination_bucket=bucket,
)

# CloudFrontのディストリビューションを作成する
cloudfront.Distribution(
    stack,
    "Distribution",
    default_behavior=cloudfront.BehaviorOptions(origin=origins.S3Origin(bucket)),
    default_root_object="index.html"
)

app.synth()
