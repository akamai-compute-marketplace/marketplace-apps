from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class LangflowFlowsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.user_menu_button = self.page.get_by_test_id("user_menu_button")
