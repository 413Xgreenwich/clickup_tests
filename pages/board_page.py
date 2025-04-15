from pages.base_page import BasePage


class BoardPage(BasePage):
    BOARD_BUTTON_SELECTOR = '[data-test="data-view-item__view-id-body-Board"]'
    ADD_TASK_TODO_BUTTON = '[data-test="board-group__create-task-button__Add Task"]'
    TASK_INPUT_LOCATOR = '[data-test="quick-create-task-panel__panel-board__input"]'
    TASK_ENTER_BUTTON = '[data-test="quick-create-task-panel__panel-board__enter-button"]'
    TASK_CONTEXT_MENU_BUTTON = '[data-test="board-actions-menu__ellipsis__TestTask_beta"]'
    TASK_DELETE_BUTTON = '[data-test="quick-actions-menu__delete-task"]'


    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "90151068928/v/l/2kypr980-375"

    def go_to_board_tab(self):
        self.wait_for_selector_and_click(self.BOARD_BUTTON_SELECTOR)
        self.assert_text_present_on_page("in progress")

    def create_the_task(self):
        self.wait_for_selector_and_click(self.ADD_TASK_TODO_BUTTON)
        self.wait_for_selector_and_type(self.TASK_INPUT_LOCATOR, "TestTask_beta", 100)
        self.wait_for_selector_and_click(self.TASK_ENTER_BUTTON)
        self.assert_text_present_on_page("Created")

    def delete_the_task(self):
        self.hover_over('.open-task-clickable-area[_ngcontent-ng-c17472219]')
        self.wait_for_selector_and_click(self.TASK_CONTEXT_MENU_BUTTON)
        self.wait_for_selector_and_click(self.TASK_DELETE_BUTTON)
        self.assert_text_present_on_page("Task moved to trash")