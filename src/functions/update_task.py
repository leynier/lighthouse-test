from .core.app import app, convert_to_handler, logger, tracer
from .core.dynamodb import tasks_table
from .core.exceptions import NotFound
from .core.models import TaskGetModel, TaskUpdateModel


@app.put("/tasks/{task_id}")
@tracer.capture_method
def update_task(task_id: str, model: TaskUpdateModel) -> TaskGetModel:
    response = tasks_table.get_item(Key={"taskId": task_id})
    item = response.get("Item")
    if not item:
        logger.warning(f"Task {task_id} not found")
        raise NotFound("Task")
    item.update(model.model_dump(exclude_unset=True))
    tasks_table.put_item(Item=item)
    logger.info(f"Updated task {task_id}")
    return TaskGetModel.model_validate(item)


handler = convert_to_handler(app)
