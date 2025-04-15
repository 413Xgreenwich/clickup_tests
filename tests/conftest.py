import pytest, requests
from playwright.sync_api import sync_playwright
from api_clients.tasks import TasksClient
from utils.helpers import CLICKUP_HEADERS, CLICKUP_BASE_URL, CLICKUP_PAYLOAD, CLICKUP_EMAIL, CLICKUP_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(CLICKUP_HEADERS)
    return session

@pytest.fixture
def tasks_client():
    return TasksClient(CLICKUP_BASE_URL)

@pytest.fixture
def test_task(get_list_id):
    client = TasksClient(CLICKUP_BASE_URL)
    
    response = client.create_task(list_id=get_list_id, payload=CLICKUP_PAYLOAD)
    task = response.json()
    task_id = task["id"]

    yield task

    client.delete_task(task_id)

@pytest.fixture(scope="session")
def get_list_id():
    session = requests.Session()
    session.headers.update(CLICKUP_HEADERS)

    workspace_response = requests.get(
        f"{CLICKUP_BASE_URL}/team", headers=CLICKUP_HEADERS
    )

    workspace_id = workspace_response.json()["teams"][0]["id"]

    space_response = requests.get(
        f"{CLICKUP_BASE_URL}/team/{workspace_id}/space", headers=CLICKUP_HEADERS
    )

    space_id = space_response.json()["spaces"][0]["id"]

    folder_response = requests.get(
        f"{CLICKUP_BASE_URL}/space/{space_id}/folder", headers=CLICKUP_HEADERS
    )

    folder_id = folder_response.json()["folders"][0]["id"]

    list_response = requests.get(
        f"{CLICKUP_BASE_URL}/folder/{folder_id}/list", headers=CLICKUP_HEADERS
    )

    list_id = list_response.json()["lists"][0]["id"]

    return list_id

@pytest.fixture
def authorized_user():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

        yield page

        page.click('[data-test="user-main-settings-menu__dropdown-toggle"]')
        page.click('[data-test="dropdown-list-item__Log out"]')
        browser.close()