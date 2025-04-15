from playwright.sync_api import sync_playwright, expect
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


def test_success_login(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

def test_fail_login(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.bad_login(CLICKUP_EMAIL, "12345678")