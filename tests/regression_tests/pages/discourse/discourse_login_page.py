from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DiscourseLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.locator("#login-account-name")
        self.password_input = self.page.locator("#login-account-password")
        self.login_button = self.page.locator("#login-button")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
