from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class SplunkHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.welcome_heading = self.page.get_by_role("heading", name="Hello, Administrator", level=1)
        self.administrator_button = self.page.get_by_role("button", name="Administrator")
