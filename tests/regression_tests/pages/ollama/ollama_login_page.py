from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OllamaLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input = self.page.locator("#email")
        self.password_input = self.page.locator("#password")
        self.sign_in_button = self.page.locator("button[type='submit']")

    def login(self, username: str, password: str):
        self.email_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()
