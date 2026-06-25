from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class HarborLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="LOG IN")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
