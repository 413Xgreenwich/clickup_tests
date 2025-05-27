from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "login"

    USERNAME_SELECTOR = '[data-test="login-email-input"]'
    PASSWORD_SELECTOR = '[data-test="login-password-input"]'
    LOGIN_BUTTON_SELECTOR = '[data-test="login-submit"]'

    def login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username, 100)
        self.wait_for_selector_and_type(self.PASSWORD_SELECTOR, password, 100)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
