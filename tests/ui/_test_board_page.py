from playwright.sync_api import sync_playwright
from pages.board_page import BoardPage


def test_go_to_board_tab(authorized_user):
    board_page = BoardPage(authorized_user)
    board_page.go_to_board_tab()