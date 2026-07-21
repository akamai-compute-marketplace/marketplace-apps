from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OpenLitespeedWordpressLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.locator("#user_login")
        self.password_input = self.page.locator("#user_pass")
        self.login_button = self.page.locator("#wp-submit")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
