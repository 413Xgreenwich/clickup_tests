from api_clients.tasks import TasksClient
from utils.helpers import (
    CLICKUP_PAYLOAD,
    CLICKUP_BAD_HEADERS,
    CLICKUP_POST_HEADER,
    CLICKUP_BAD_PAYLOAD,
    CLICKUP_PAYLOAD_UPDATE
)

def test_success_create_task(tasks_client, get_list_id):
    response = tasks_client.create_task(list_id=get_list_id, payload=CLICKUP_PAYLOAD)
    assert response.status_code == 200
    task_id = response.json()["id"]
    cleanup = tasks_client.delete_task(task_id)
    assert cleanup.status_code == 204


def test_fail_create_task(tasks_client, get_list_id):
    response = tasks_client.create_task(list_id=get_list_id, payload=None)
    assert response.status_code == 400


def test_success_get_task(tasks_client, test_task, get_list_id):
    response = tasks_client.get_tasks(list_id=get_list_id)
    assert response.status_code == 200


def test_fail_get_task(tasks_client, get_list_id):
    tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)
    response = tasks_client.get_tasks(list_id=get_list_id)
    assert response.status_code == 400


def test_success_update_task(tasks_client, test_task):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_POST_HEADER)
    response = tasks_client.update_task(task_id=task_id, payload=CLICKUP_PAYLOAD_UPDATE)
    assert response.status_code == 200
    assert response.json()["name"] == "TestTask_gamma"


def test_fail_update_task(tasks_client, test_task):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_POST_HEADER)
    response = tasks_client.update_task(task_id=task_id, payload=CLICKUP_BAD_PAYLOAD)
    assert response.status_code == 400


def test_success_delete_task(tasks_client, test_task):
    task_id = test_task["id"]
    response = tasks_client.delete_task(task_id=task_id)
    assert response.status_code == 204


def test_fail_delete_task(tasks_client, test_task):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)
    response = tasks_client.delete_task(task_id=task_id)
    assert response.status_code == 400