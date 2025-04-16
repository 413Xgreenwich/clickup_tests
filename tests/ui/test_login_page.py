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

    @allure.description("Проверка ошибки при некорректном пароле")
    def test_fail_login(self, sync_browser):
        with allure.step("Создаём новую страницу браузера"):
            page = sync_browser.new_page()

        with allure.step("Выполняем логин с некорректным паролем"):
            login_page = LoginPage(page)
            login_page.bad_login(CLICKUP_EMAIL, "12345678")