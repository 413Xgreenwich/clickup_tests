import allure
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@allure.feature("UI: Авторизация")
class TestLogin:

    @allure.description("Проверка успешного входа в систему")
    def test_success_login(self, sync_browser):
        with allure.step("Создаём новую страницу браузера"):
            page = sync_browser.new_page()
        with allure.step("Выполняем логин с корректными данными"):
            login_page = LoginPage(page)
            login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
        with allure.step("Проверяем наличие элементов успешного входа"):
            login_page.assert_text_present_on_page("Workspace")
            login_page.assert_text_present_on_page("Board")

    @allure.description("Проверка ошибки при некорректном пароле")
    def test_fail_login(self, sync_browser):
        with allure.step("Создаём новую страницу браузера"):
            page = sync_browser.new_page()
        with allure.step("Выполняем логин с некорректным паролем"):
            login_page = LoginPage(page)
            login_page.login(CLICKUP_EMAIL, "12345678")
        with allure.step("Проверяем текст ошибки"):
            login_page.assert_text_present_on_page("Incorrect password for this email.")
