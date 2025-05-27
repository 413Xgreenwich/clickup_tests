import allure
import pytest
from utils.helpers import (
    CLICKUP_HEADERS,
    CLICKUP_PAYLOAD,
    CLICKUP_BAD_HEADERS,
    CLICKUP_POST_HEADER,
    CLICKUP_BAD_PAYLOAD,
    CLICKUP_PAYLOAD_UPDATE,
)


@allure.feature("API: Работа с задачами")
class TestTasks:

    @allure.description("Проверка успешного создания задачи")
    def test_success_create_task(self, tasks_client, get_list_id):
        with allure.step("Создаём задачу"):
            response = tasks_client.create_task(
                list_id=get_list_id, payload=CLICKUP_PAYLOAD
            )
        assert response.status_code == 200, "Задача не создана"

        with allure.step("Проверяем ответ"):
            body = response.json()
            assert "id" in body, "В ответе нет id созданной задачи"
            assert body["name"] == CLICKUP_PAYLOAD["name"], "Имя задачи не совпадает"
            assert body["status"]["status"] == "to do", "Статус задачи не соответствует"

        with allure.step("Удаляем задачу (clean-up)"):
            task_id = body["id"]
            cleanup = tasks_client.delete_task(task_id)
            assert cleanup.status_code == 204, "Не удалось удалить задачу"

    @allure.description("Проверка ошибок при создании задачи с невалидными данными")
    @pytest.mark.parametrize(
        "payload, expected_status, expected_error",
        [
            (None, 400, None),  # Без тела вообще
            ({}, 400, None),  # Пустой json
            ({"name": ""}, 400, None),  # Пустое имя
            ({"invalid_key": "value"}, 400, None),  # Некорректный ключ
        ],
    )
    def test_fail_create_task(
        self, tasks_client, get_list_id, payload, expected_status, expected_error
    ):
        with allure.step(f"Пробуем создать задачу с payload={payload}"):
            response = tasks_client.create_task(list_id=get_list_id, payload=payload)
        assert response.status_code == expected_status

        with allure.step("Проверяем тело ответа на наличие ошибки"):
            body = response.json()
            if expected_error:
                assert expected_error in str(body), f"Ошибка не совпадает: {body}"
            else:
                assert (
                    "err" in body or "error" in body
                ), "Нет сообщения об ошибке в ответе"

    @allure.description("Проверка получения списка задач")
    def test_success_get_task(self, tasks_client, create_and_delete_task, get_list_id):
        with allure.step("Получаем список задач"):
            response = tasks_client.get_tasks(list_id=get_list_id)
        assert response.status_code == 200

        with allure.step("Проверяем наличие созданной задачи в списке"):
            body = response.json()
            assert "tasks" in body, "Ответ не содержит список задач"
            assert any(
                t["id"] == create_and_delete_task["id"] for t in body["tasks"]
            ), "Созданная задача не найдена"

    @allure.description(
        "Проверка ошибки при получении задач с некорректными заголовками"
    )
    def test_fail_get_task(self, tasks_client, get_list_id):
        with allure.step("Обновляем заголовки на некорректные"):
            tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)

        with allure.step("Отправляем запрос и проверяем ответ"):
            response = tasks_client.get_tasks(list_id=get_list_id)
        assert response.status_code == 400

        with allure.step("Проверяем тело ошибки"):
            body = response.json()
            assert (
                body.get("err") == "Authorization header required"
            ), "Текст ошибки не совпадает с ожидаемым - Authorization header required"

    @allure.description("Проверка успешного обновления задачи")
    def test_success_update_task(self, tasks_client, create_and_delete_task):
        task_id = create_and_delete_task["id"]

        with allure.step("Обновляем заголовки на POST"):
            tasks_client.session.headers.update(CLICKUP_POST_HEADER)

        with allure.step("Отправляем PUT-запрос на обновление задачи"):
            response = tasks_client.update_task(
                task_id=task_id, payload=CLICKUP_PAYLOAD_UPDATE
            )
        assert response.status_code == 200

        with allure.step("Проверяем тело ответа"):
            body = response.json()
            assert body["id"] == task_id, "Обновлена не та задача"
            assert body["name"] == "TestTask_gamma", "Имя задачи не обновлено корректно"

    @allure.description("Проверка ошибки при обновлении задачи с некорректным статусом")
    def test_fail_update_task(self, tasks_client, create_and_delete_task):
        task_id = create_and_delete_task["id"]

        with allure.step("Обновляем заголовки на POST"):
            tasks_client.session.headers.update(CLICKUP_POST_HEADER)

        with allure.step("Отправляем PUT-запрос с несуществующим статусом"):
            response = tasks_client.update_task(
                task_id=task_id, payload=CLICKUP_BAD_PAYLOAD
            )
        assert response.status_code == 400

        with allure.step("Проверяем ошибку в теле ответа"):
            body = response.json()
            assert (
                body.get("err") == "Status does not exist"
            ), "Текст ошибки не совпадает с ожидаемым - Status does not exist"

    @allure.description("Проверка успешного удаления задачи")
    def test_success_delete_task(self, tasks_client, create_and_delete_task):
        task_id = create_and_delete_task["id"]

        with allure.step("Удаляем задачу"):
            response = tasks_client.delete_task(task_id=task_id)
        assert response.status_code == 204

        with allure.step("Проверяем, что задача действительно удалена"):
            check = tasks_client.get_tasks(list_id=create_and_delete_task["list"]["id"])
            assert all(
                t["id"] != task_id for t in check.json()["tasks"]
            ), "Задача не была удалена"

    @allure.description(
        "Проверка ошибки при удалении задачи с некорректными заголовками"
    )
    def test_fail_delete_task(self, tasks_client, create_and_delete_task, get_list_id):
        task_id = create_and_delete_task["id"]

        with allure.step("Обновляем заголовки на некорректные"):
            tasks_client.session.headers.update(CLICKUP_BAD_HEADERS)

        with allure.step("Пытаемся удалить задачу"):
            response = tasks_client.delete_task(task_id=task_id)
        assert (
            response.status_code == 400
        ), "Удаление с некорректными заголовками прошло успешно — это ошибка"

        with allure.step("Возвращаем заголовки и убеждаемся, что задача осталась"):
            tasks_client.session.headers.update(CLICKUP_HEADERS)
            task_list = tasks_client.get_tasks(list_id=get_list_id).json()
            assert any(
                t["id"] == task_id for t in task_list["tasks"]
            ), "Задача была удалена, хотя не должна была"
