from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JenkinsUnlockPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Unlock Jenkins")
        self.admin_password_input = self.page.get_by_role("textbox", name="Administrator password")
        self.continue_button = self.page.get_by_role("button", name="Continue")

    def unlock(self, password: str):
        self.admin_password_input.fill(password)
        self.continue_button.click()
