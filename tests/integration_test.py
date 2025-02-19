from os import getenv

from dotenv import load_dotenv
from pytest import fixture, mark
from requests import delete, get, post, put

from src.functions.core.models import TaskStatus


class Store:
    def __init__(self):
        self.task: dict | None = None

    def set_task(self, task: dict) -> None:
        self.task = task

    def get_task(self) -> dict | None:
        return self.task


@fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@fixture(scope="session")
def api_url() -> str:
    url = getenv("API_GATEWAY_URL")
    if not url:
        raise ValueError("API_GATEWAY_URL not found in environment variables")
    return url.rstrip("/")


@fixture(scope="session")
def store() -> Store:
    return Store()


@mark.dependency(name="create")
def test_create_task(api_url: str, store: Store):
    create_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": TaskStatus.PENDING,
    }
    response = post(f"{api_url}/tasks", json=create_data)
    assert response.status_code == 201
    task = response.json()
    store.set_task(task)
    assert task["title"] == create_data["title"]
    assert task["description"] == create_data["description"]
    assert task["status"] == create_data["status"]
    assert "taskId" in task


@mark.dependency(depends=["create"], name="get")
def test_get_task(api_url: str, store: Store):
    task = store.get_task()
    assert task is not None, "Task was not created in previous test"
    response = get(f"{api_url}/tasks/{task['taskId']}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["taskId"] == task["taskId"]
    assert retrieved_task["title"] == task["title"]
    assert retrieved_task["description"] == task["description"]
    assert retrieved_task["status"] == task["status"]


@mark.dependency(depends=["get"], name="update")
def test_update_task(api_url: str, store: Store):
    task = store.get_task()
    assert task is not None, "Task was not created in previous test"
    update_data = {"title": "Updated Task", "status": TaskStatus.COMPLETED}
    response = put(f"{api_url}/tasks/{task['taskId']}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    store.set_task(updated_task)
    assert updated_task["taskId"] == task["taskId"]
    assert updated_task["title"] == update_data["title"]
    assert updated_task["status"] == update_data["status"]


@mark.dependency(depends=["update"], name="delete")
def test_delete_task(api_url: str, store: Store):
    task = store.get_task()
    assert task is not None, "Task was not created in previous test"
    response = delete(f"{api_url}/tasks/{task['taskId']}")
    assert response.status_code == 204
    response = get(f"{api_url}/tasks/{task['taskId']}")
    assert response.status_code == 404


def test_error_cases(api_url):
    """Test error cases for non-existent tasks"""
    response = get(f"{api_url}/tasks/nonexistent")
    assert response.status_code == 404
    update_data = {"title": "Updated Task"}
    response = put(f"{api_url}/tasks/nonexistent", json=update_data)
    assert response.status_code == 404
    response = delete(f"{api_url}/tasks/nonexistent")
    assert response.status_code == 404
