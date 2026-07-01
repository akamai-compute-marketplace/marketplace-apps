from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class JupyterlabLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.token_input = self.page.get_by_role("textbox", name="Password or token:")
        self.login_button = self.page.get_by_role("button", name="Log in", exact=True)

    def login(self, token: str):
        self.token_input.fill(token)
        self.login_button.click()
