from fastapi import Response, status

from .core.app import app, convert_to_handler, logger, tracer
from .core.dynamodb import tasks_table
from .core.exceptions import NotFound


@app.delete("/tasks/{task_id}")
@tracer.capture_method
def delete_task(task_id: str):
    response = tasks_table.get_item(Key={"taskId": task_id})
    item = response.get("Item")
    if not item:
        logger.warning(f"Task {task_id} not found")
        raise NotFound("Task")
    tasks_table.delete_item(Key={"taskId": task_id})
    logger.info(f"Deleted task {task_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


handler = convert_to_handler(app)
