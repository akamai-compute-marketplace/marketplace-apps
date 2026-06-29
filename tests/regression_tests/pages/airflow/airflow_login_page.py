from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class AirflowLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.locator("[name='username']")
        self.password_input = self.page.locator("[name='password']")
        self.sign_in_button = self.page.locator("button[type='submit']")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()
