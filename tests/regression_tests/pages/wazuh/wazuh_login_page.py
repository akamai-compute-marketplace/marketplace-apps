from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class WazuhLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.get_by_role("textbox", name="username_input")
        self.password_input = self.page.get_by_role("textbox", name="password_input")
        self.login_button = self.page.get_by_role("button", name="basicauth_login_button")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
