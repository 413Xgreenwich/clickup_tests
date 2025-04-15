from playwright.sync_api import sync_playwright
from pages.board_page import BoardPage
from utils.helpers import CLICKUP_PAYLOAD


def test_ui_create_task(authorized_user, tasks_client, get_list_id):
    response = tasks_client.create_task(list_id=get_list_id, payload=CLICKUP_PAYLOAD)
    assert response.status_code == 200, "Задача не создана"

    board_page = BoardPage(authorized_user)
    board_page.go_to_board_tab()

    board_page.delete_the_task()

def test_ui_delete_task(authorized_user, tasks_client, get_list_id):
    board_page = BoardPage(authorized_user)
    board_page.go_to_board_tab()
    board_page.create_the_task()

    response = tasks_client.get_tasks(list_id=get_list_id)
    assert response.status_code == 200
    body = response.json()
    tasks_client.delete_task(body["tasks"][0]["id"])



