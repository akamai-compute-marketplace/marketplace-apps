from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class HaltdosLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.full_name_field = self.page.locator("#name")
