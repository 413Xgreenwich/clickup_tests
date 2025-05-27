from playwright.sync_api import expect


class BasePage:
    __BASE_URL = "https://app.clickup.com/"

    def __init__(self, page):
        self.page = page
        self._endpoint = ""

    def _get_full_url(self):
        return f"{self.__BASE_URL}{self._endpoint}"

    def hover_over(self, selector):
        self.page.locator(selector).hover()

    def navigate_to(self):
        full_url = self._get_full_url()
        self.page.goto(full_url)
        self.page.wait_for_load_state("load")
        expect(self.page).to_have_url(full_url)

    def wait_for_selector_and_click(self, selector):
        self.page.wait_for_selector(selector)
        self.page.click(selector)

    def wait_for_selector_and_type(self, selector, value, delay):
        self.page.wait_for_selector(selector)
        self.page.type(selector, value, delay=delay)

    def assert_text_present_on_page(self, text):
        expect(self.page.locator("body")).to_contain_text(text, timeout=1500000)
