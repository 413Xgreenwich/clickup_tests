import allure
from pages.board_page import BoardPage
from utils.helpers import CLICKUP_PAYLOAD


@allure.feature("UI: Задачи на доске")
class TestBoardTasks:

    @allure.description("Проверка создания задачи через API и удаления через UI")
    def test_ui_delete_task(
        self, authorized_user, tasks_client, get_list_id, team_id, unique_task_name
    ):
        with allure.step("Создаём задачу через API"):
            payload = CLICKUP_PAYLOAD.copy()
            payload["name"] = unique_task_name
            response = tasks_client.create_task(list_id=get_list_id, payload=payload)
        assert response.status_code == 200, "Задача не создана"

        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user, team_id)
            board_page.go_to_board_tab()

        with allure.step("Удаляем задачу через UI по имени"):
            board_page.delete_the_task(unique_task_name)

        with allure.step("Проверяем через API, что задача удалена"):
            tasks = tasks_client.get_tasks(list_id=get_list_id).json()["tasks"]
            assert all(
                t["name"] != unique_task_name for t in tasks
            ), "Задача не была удалена"

    @allure.description("Проверка создания задачи через UI и удаления через API")
    def test_ui_create_task(
        self, authorized_user, tasks_client, get_list_id, team_id, unique_task_name
    ):
        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user, team_id)
            board_page.go_to_board_tab()

        with allure.step("Создаём задачу через UI с уникальным именем"):
            board_page.create_the_task(unique_task_name)

        with allure.step("Получаем список задач через API и ищем нужную по имени"):
            response = tasks_client.get_tasks(list_id=get_list_id)
        assert response.status_code == 200

        body = response.json()
        found_task = next(
            (t for t in body["tasks"] if t["name"] == unique_task_name), None
        )
        assert found_task is not None, "Задача не найдена по имени"

        with allure.step("Удаляем задачу через API"):
            tasks_client.delete_task(found_task["id"])
