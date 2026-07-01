from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GitLabLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.get_by_test_id("username-field")
        self.password_input = self.page.get_by_test_id("password-field")
        self.login_button = self.page.get_by_test_id("sign-in-button")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
