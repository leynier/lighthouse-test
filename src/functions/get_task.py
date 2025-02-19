from .core.app import app, convert_to_handler, logger, tracer
from .core.dynamodb import tasks_table
from .core.exceptions import NotFound
from .core.models import TaskGetModel


@app.get("/tasks/{task_id}")
@tracer.capture_method
def get_task(task_id: str) -> TaskGetModel:
    response = tasks_table.get_item(Key={"taskId": task_id})
    item = response.get("Item")
    if not item:
        logger.warning(f"Task {task_id} not found")
        raise NotFound("Task")
    return TaskGetModel.model_validate(item)


handler = convert_to_handler(app)
