from pathlib import Path
from typing import cast

import aws_cdk as cdk
from constructs import Construct

root_path = str(Path(__file__).parent.resolve())


class LighthouseTestStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        tasks_table = cdk.aws_dynamodb.Table(
            self,
            "TasksTable",
            partition_key=cdk.aws_dynamodb.Attribute(
                name="taskId",
                type=cdk.aws_dynamodb.AttributeType.STRING,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        code_functions = cdk.aws_lambda.Code.from_asset(
            root_path,
            bundling={
                "image": cdk.aws_lambda.Runtime.PYTHON_3_12.bundling_image,
                "command": [
                    "bash",
                    "-c",
                    "pip install -r requirements.txt --platform manylinux2014_x86_64 -t /asset-output --only-binary=:all: && cp -au . /asset-output",
                ],
            },
        )

        enviroment_functions = {
            "SERVICE_NAME": "LighthouseTest",
            "TASKS_TABLE_NAME": tasks_table.table_name,
        }

        create_task_lambda = cdk.aws_lambda.Function(
            self,
            "LighthouseTestCreateTaskFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="functions.create_task.handler",
            code=code_functions,
            environment=enviroment_functions,
        )

        get_task_lambda = cdk.aws_lambda.Function(
            self,
            "LighthouseTestGetTaskFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="functions.get_task.handler",
            code=code_functions,
            environment=enviroment_functions,
        )

        update_task_lambda = cdk.aws_lambda.Function(
            self,
            "LighthouseTestUpdateTaskFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="functions.update_task.handler",
            code=code_functions,
            environment=enviroment_functions,
        )

        delete_task_lambda = cdk.aws_lambda.Function(
            self,
            "LighthouseTestDeleteTaskFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="functions.delete_task.handler",
            code=code_functions,
            environment=enviroment_functions,
        )

        tasks_table.grant_read_write_data(create_task_lambda)
        tasks_table.grant_read_data(get_task_lambda)
        tasks_table.grant_read_write_data(update_task_lambda)
        tasks_table.grant_read_write_data(delete_task_lambda)

        api = cdk.aws_apigateway.RestApi(
            self,
            "LighthouseTestApi",
            rest_api_name="LighthouseTestApi",
            description="API for Lighthouse Test",
        )

        tasks_resource = api.root.add_resource("tasks")
        task_id_resource = tasks_resource.add_resource("{task_id}")

        tasks_resource.add_method(
            "POST",
            cdk.aws_apigateway.LambdaIntegration(
                cast(cdk.aws_lambda.IFunction, create_task_lambda)
            ),
        )

        task_id_resource.add_method(
            "GET",
            cdk.aws_apigateway.LambdaIntegration(
                cast(cdk.aws_lambda.IFunction, get_task_lambda)
            ),
        )

        task_id_resource.add_method(
            "PUT",
            cdk.aws_apigateway.LambdaIntegration(
                cast(cdk.aws_lambda.IFunction, update_task_lambda)
            ),
        )

        task_id_resource.add_method(
            "DELETE",
            cdk.aws_apigateway.LambdaIntegration(
                cast(cdk.aws_lambda.IFunction, delete_task_lambda)
            ),
        )
