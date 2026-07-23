from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PiholeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.password_input = self.page.locator("input[type='password']")
        self.login_button = self.page.get_by_role("button", name="Log in (uses cookie)")

    def login(self, password: str):
        self.password_input.fill(password)
        self.login_button.click()
