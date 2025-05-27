import pytest
import requests
import allure
import uuid
from playwright.sync_api import sync_playwright
from api_clients.tasks import TasksClient
from utils.helpers import (
    CLICKUP_HEADERS,
    CLICKUP_BASE_URL,
    CLICKUP_PAYLOAD,
    CLICKUP_EMAIL,
    CLICKUP_PASSWORD,
)
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def auth_session():
    with allure.step("Создание requests-сессии с заголовками ClickUp"):
        session = requests.Session()
        session.headers.update(CLICKUP_HEADERS)
        return session


@pytest.fixture
def tasks_client():
    with allure.step("Создание экземпляра TasksClient"):
        return TasksClient(CLICKUP_BASE_URL)


@pytest.fixture
def create_and_delete_task(get_list_id):
    client = TasksClient(CLICKUP_BASE_URL)

    with allure.step("Создание задачи через API"):
        response = client.create_task(list_id=get_list_id, payload=CLICKUP_PAYLOAD)
        task = response.json()
        task_id = task["id"]

    yield task

    with allure.step("Удаление задачи после завершения теста"):
        client.delete_task(task_id)


@pytest.fixture
def get_list_id(tasks_client):
    return tasks_client.get_first_list_id()


@pytest.fixture
def authorized_user(sync_browser):
    with allure.step("Создаём новую вкладку и логинимся через UI"):
        page = sync_browser.new_page()
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
        yield page
        with allure.step("Выход из аккаунта"):
            page.click('[data-test="user-main-settings-menu__dropdown-toggle"]')
            page.click('[data-test="dropdown-list-item__Log out"]')
            page.close()


@pytest.fixture(scope="session")
def sync_browser():
    with allure.step("Запуск браузера Playwright"):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        with allure.step("Закрытие браузера Playwright"):
            browser.close()
            playwright.stop()


@pytest.fixture
def team_id(tasks_client):
    return tasks_client.get_first_workspace_id()


@pytest.fixture
def unique_task_name():
    return f"TestTask_{uuid.uuid4().hex[:8]}"
