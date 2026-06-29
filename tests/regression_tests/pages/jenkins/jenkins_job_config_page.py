from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JenkinsJobConfigPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.save_button = self.page.get_by_role("button", name="Save")
