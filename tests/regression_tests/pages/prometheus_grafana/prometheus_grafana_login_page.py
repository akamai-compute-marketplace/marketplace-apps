from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GrafanaLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("email or username")
        self.password_input = page.get_by_placeholder("password")
        self.login_button = page.get_by_role("button", name="Log in")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
