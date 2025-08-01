import aws_cdk as core
import aws_cdk.assertions as assertions

from my_cdk_lambda_project.my_cdk_lambda_project_stack import MyCdkLambdaProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_cdk_lambda_project/my_cdk_lambda_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyCdkLambdaProjectStack(app, "my-cdk-lambda-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
