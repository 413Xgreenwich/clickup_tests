import allure
from pages.board_page import BoardPage
from utils.helpers import CLICKUP_PAYLOAD


@allure.feature("UI: Задачи на доске")
class TestBoardTasks:

    @allure.description("Проверка создания задачи через API и удаления через UI")
    def test_ui_delete_task(self, authorized_user, tasks_client, get_list_id, team_id):
        with allure.step("Создаём задачу через API"):
            response = tasks_client.create_task(list_id=get_list_id, payload=CLICKUP_PAYLOAD)
        assert response.status_code == 200, "Задача не создана"

        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user, team_id)
            board_page.go_to_board_tab()

        with allure.step("Удаляем задачу через UI"):
            board_page.delete_the_task()

    @allure.description("Проверка создания задачи через UI и удаления через API")
    def test_ui_create_task(self, authorized_user, tasks_client, get_list_id, team_id):
        with allure.step("Переходим на вкладку доски"):
            board_page = BoardPage(authorized_user, team_id)
            board_page.go_to_board_tab()

        with allure.step("Создаём задачу через UI"):
            board_page.create_the_task()

        with allure.step("Получаем список задач через API"):
            response = tasks_client.get_tasks(list_id=get_list_id)
        assert response.status_code == 200

        with allure.step("Удаляем задачу через API"):
            body = response.json()
            task_id = body["tasks"][0]["id"]
            tasks_client.delete_task(task_id)




