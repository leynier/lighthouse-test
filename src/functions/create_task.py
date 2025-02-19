from uuid import uuid4

from .core.app import app, convert_to_handler, logger, tracer
from .core.dynamodb import tasks_table
from .core.models import TaskCreateModel, TaskGetModel


@app.post("/tasks", status_code=201)
@tracer.capture_method
def create_task(model: TaskCreateModel) -> TaskGetModel:
    item = TaskGetModel(
        taskId=str(uuid4()),
        **model.model_dump(),
    )
    tasks_table.put_item(Item=item.model_dump())
    logger.info(f"Created task {item.taskId}")
    return item


handler = convert_to_handler(app)
