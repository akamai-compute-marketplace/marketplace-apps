from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PrometheusPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.query_input = page.get_by_placeholder("Enter expression (press Shift+Enter for newlines)")
        self.execute_button = page.get_by_role("button", name="Execute")
