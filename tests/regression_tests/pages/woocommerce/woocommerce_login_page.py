from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class WooCommerceLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.get_by_role("textbox", name="Username or Email Address")
        self.password_input = self.page.get_by_role("textbox", name="Password", exact=True)
        self.login_button = self.page.get_by_role("button", name="Log In")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
