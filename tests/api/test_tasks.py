from api_clients.tasks import TasksClient
from utils.helpers import (
    CLICKUP_HEADERS,
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
    body = response.json()
    assert "id" in body, "В ответе нет id созданной задачи"
    assert body["name"] == CLICKUP_PAYLOAD["name"], "Имя задачи не совпадает"
    assert body["status"]["status"] == "to do", "Статус задачи не соответствует"


def test_fail_create_task(tasks_client, get_list_id):
    response = tasks_client.create_task(list_id=get_list_id, payload=None)
    assert response.status_code == 400
    body = response.json()
    assert "err" in body or "error" in body, "Нет сообщения об ошибке в ответе"


def test_success_get_task(tasks_client, test_task, get_list_id):
    response = tasks_client.get_tasks(list_id=get_list_id)
    assert response.status_code == 200
    body = response.json()
    assert "tasks" in body, "Ответ не содержит список задач"
    assert any(t["id"] == test_task["id"] for t in body["tasks"]), "Созданная задача не найдена"


def test_fail_get_task(tasks_client, get_list_id):
    tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)
    response = tasks_client.get_tasks(list_id=get_list_id)
    assert response.status_code == 400
    body = response.json()
    assert body.get("err") == "Authorization header required", "Текст ошибки не совпадает с ожидаемым - Authorization header required"


def test_success_update_task(tasks_client, test_task):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_POST_HEADER)
    response = tasks_client.update_task(task_id=task_id, payload=CLICKUP_PAYLOAD_UPDATE)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id, "Обновлена не та задача"
    assert body["name"] == "TestTask_gamma", "Имя задачи не обновлено корректно"


def test_fail_update_task(tasks_client, test_task):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_POST_HEADER)
    response = tasks_client.update_task(task_id=task_id, payload=CLICKUP_BAD_PAYLOAD)
    assert response.status_code == 400
    body = response.json()
    assert body.get("err") == "Status does not exist", "Текст ошибки не совпадает с ожидаемым - Status does not exist"


def test_success_delete_task(tasks_client, test_task):
    task_id = test_task["id"]
    response = tasks_client.delete_task(task_id=task_id)
    assert response.status_code == 204
    check = tasks_client.get_tasks(list_id=test_task["list"]["id"])
    assert all(t["id"] != task_id for t in check.json()["tasks"]), "Задача не была удалена"


def test_fail_delete_task(tasks_client, test_task, get_list_id):
    task_id = test_task["id"]
    tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)
    response = tasks_client.delete_task(task_id=task_id)
    assert response.status_code == 400, "Удаление с некорректными заголовками прошло успешно — это ошибка"

    # Проверяем, что задача всё ещё существует
    tasks_client.session.headers.update(CLICKUP_HEADERS)  # вернули корректные заголовки
    task_list = tasks_client.get_tasks(list_id=get_list_id).json()

    assert any(t["id"] == task_id for t in task_list["tasks"]), "Задача была удалена, хотя не должна была"
    