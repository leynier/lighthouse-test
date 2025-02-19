from os import getenv

from boto3 import resource

dynamodb = resource("dynamodb")

tasks_table_name = getenv("TASKS_TABLE_NAME")
if not tasks_table_name:
    raise ValueError("TASKS_TABLE_NAME environment variable is not set")
tasks_table = dynamodb.Table(tasks_table_name)
