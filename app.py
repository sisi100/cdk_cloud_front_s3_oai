import aws_cdk as cdk

app = cdk.App()
stack = cdk.Stack(app, "cdk_cloud_front_s3_oai-stack")

# ここに必要なリソース書く

app.synth()
