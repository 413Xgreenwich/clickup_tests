from pages.base_page import BasePage
import api_clients.tasks


class BoardPage(BasePage):
    BOARD_BUTTON_SELECTOR = '[data-test="data-view-item__view-id-body-Board"]'
    ADD_TASK_TODO_BUTTON = '[data-test="board-group__create-task-button__Add Task"]'
    TASK_INPUT_LOCATOR = '[data-test="quick-create-task-panel__panel-board__input"]'
    TASK_ENTER_BUTTON = (
        '[data-test="quick-create-task-panel__panel-board__enter-button"]'
    )
    TASK_AREA_SELECTOR_TEMPLATE = '.open-task-clickable-area:has-text("%s")'
    CONTEXT_MENU_SELECTOR = '[data-test="board-actions-menu__ellipsis__%s"]'
    TASK_DELETE_BUTTON = '[data-test="quick-actions-menu__delete-task"]'

    def __init__(self, page, team_id):
        super().__init__(page)
        self._endpoint = f"{team_id}/v/b/t/{team_id}"

    def go_to_board_tab(self):
        self.wait_for_selector_and_click(self.BOARD_BUTTON_SELECTOR)
        self.assert_text_present_on_page("in progress")

    def create_the_task(self, task_name):
        self.wait_for_selector_and_click(self.ADD_TASK_TODO_BUTTON)
        self.wait_for_selector_and_type(self.TASK_INPUT_LOCATOR, task_name, 100)
        self.wait_for_selector_and_click(self.TASK_ENTER_BUTTON)
        self.assert_text_present_on_page("Created")

    def delete_the_task(self, task_name):
        task_area_selector = self.TASK_AREA_SELECTOR_TEMPLATE % task_name
        self.hover_over(task_area_selector)
        context_menu_selector = self.CONTEXT_MENU_SELECTOR % task_name
        self.wait_for_selector_and_click(context_menu_selector)
        self.wait_for_selector_and_click(self.TASK_DELETE_BUTTON)
        self.assert_text_present_on_page("Task moved to trash")
