import pytest, requests
from playwright.sync_api import sync_playwright
from utils.helpers import CLICKUP_HEADERS, CLICKUP_BASE_URL


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
