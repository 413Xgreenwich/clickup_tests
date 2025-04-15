import pytest, requests, allure
from utils.helpers import *


@allure.feature("API-тесты проверки функционала задачи")
class TestTasks:

    @allure.description("Проверка создания задачи без тела запроса")
    def test_fail_create_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        new_task = auth_session.post(url)
        assert (
            new_task.status_code == 400
        ), "Код ошибки при заведомо некорректном запросе не совпадает с ожидаемым"

    @allure.description("Проверка корректного создания задачи")
    def test_success_create_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        headers.update(CLICKUP_POST_HEADER)
        new_task = auth_session.post(url, json=CLICKUP_PAYLOAD, headers=headers)
        assert new_task.status_code == 200, "Ошибка при создании новой задачи"

    @allure.description("Проверка получения списка задач с некорректными заголовками")
    def test_fail_get_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_BAD_HEADERS
        task_list = auth_session.get(url, headers=headers)
        assert (
            task_list.status_code == 400
        ), "Код ошибки при заведомо некорректном запросе не совпадает с ожидаемым"

    @allure.description("Проверка корректного получения списка задач")
    def test_success_get_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        task_list = auth_session.get(url, headers=headers)
        assert task_list.status_code == 200, "Ошибка при получении списка задач"

    @allure.description("Попытка задать невозможный статус задачи")
    def test_fail_update_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        task_list = auth_session.get(url, headers=headers)
        task_id = task_list.json()["tasks"][0]["id"]
        url = f"{CLICKUP_BASE_URL}/task/{task_id}"
        headers.update(CLICKUP_POST_HEADER)
        payload_update = CLICKUP_BAD_PAYLOAD
        update_task = auth_session.put(url, json=payload_update, headers=headers)
        assert update_task.status_code == 400, "Код ошибки при заведомо некорректном запросе не совпадает с ожидаемым"

    @allure.description("Проверка успешного обновления названия задачи")
    def test_success_update_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        task_list = auth_session.get(url, headers=headers)
        task_id = task_list.json()["tasks"][0]["id"]
        url = f"{CLICKUP_BASE_URL}/task/{task_id}"
        headers.update(CLICKUP_POST_HEADER)
        payload_update = CLICKUP_PAYLOAD_UPDATE
        update_task = auth_session.put(url, json=payload_update, headers=headers)
        assert update_task.json()["name"] == "TestTask_gamma", "Имя задачи не обновлено, или обновлено некорректно"
        assert update_task.status_code == 200, "Ошибка при попытке обновить название задачи"

    @allure.description("Проверка удаления задачи с запросом с некорректными заголовками")
    def test_fail_delete_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        task_list = auth_session.get(url, headers=headers)
        task_id = task_list.json()["tasks"][0]["id"]
        url = f"{CLICKUP_BASE_URL}/task/{task_id}"
        headers = CLICKUP_BAD_HEADERS
        delete_task = auth_session.delete(url, headers=headers)
        assert delete_task.status_code == 400, "Не удалось удалить задачу"

    @allure.description("Проверка успешного удаления задачи")
    def test_success_delete_task(self, auth_session, get_list_id):
        url = f"{CLICKUP_BASE_URL}/list/{get_list_id}/task"
        headers = CLICKUP_HEADERS
        task_list = auth_session.get(url, headers=headers)
        task_id = task_list.json()["tasks"][0]["id"]
        url = f"{CLICKUP_BASE_URL}/task/{task_id}"
        delete_task = auth_session.delete(url, headers=headers)
        assert delete_task.status_code == 204, "Ошибка при попытке удалить задачу"
