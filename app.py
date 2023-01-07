import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as deployment

app = cdk.App()
stack = cdk.Stack(app, "cdk-cloud-front-s3-oai-stack")

# バケットを作成する
bucket = s3.Bucket(stack, "Bucket", block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
deployment.BucketDeployment(
    stack,
    "BucketDeployment",
    sources=[deployment.Source.asset("html")],
    destination_bucket=bucket,
)

# CloudFrontのディストリビューションを作成する
distribution = cloudfront.Distribution(
    stack,
    "Distribution",
    default_behavior=cloudfront.BehaviorOptions(origin=origins.S3Origin(bucket)),
    default_root_object="index.html",
    error_responses=[
        cloudfront.ErrorResponse(http_status=404, response_http_status=200, response_page_path="/errors/404.html"),
        cloudfront.ErrorResponse(http_status=403, response_http_status=200, response_page_path="/errors/403.html"),
    ],
)

# バケットにpathが存在しない場合404で返答させる
oai: cloudfront.OriginAccessIdentity = distribution.node.find_child("Origin1").node.find_child("S3Origin")
policy = iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    principals=[iam.CanonicalUserPrincipal(oai.cloud_front_origin_access_identity_s3_canonical_user_id)],
    resources=[bucket.bucket_arn],
    actions=["s3:ListBucket"],
)
bucket.add_to_resource_policy(policy)

app.synth()
