from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MastodonLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = self.page.get_by_role("textbox", name="E-mail address")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Log in")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
