from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoplinLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Log in to Joplin Server")
        self.email_input = self.page.locator('input[name="email"]')
        self.password_input = self.page.locator('input[name="password"]')
        self.login_button = self.page.get_by_role("button", name="Login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
