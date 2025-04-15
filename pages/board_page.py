from pages.base_page import BasePage


class BoardPage(BasePage):
    BOARD_BUTTON_SELECTOR = '[data-test="data-view-item__view-id-body-Board"]'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "90151068928/v/l/2kypr980-375"

    def go_to_board_tab(self):
        self.wait_for_selector_and_click(self.BOARD_BUTTON_SELECTOR)
        self.assert_text_present_on_page("in progress")