from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MilvusLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_input = self.page.locator("#accessKey")
        self.key_input = self.page.locator("#secretKey")
        self.login_button = self.page.get_by_role("button", name="Login", exact=True)

    def login(self, username: str, password: str):
        self.account_input.fill(username)
        self.key_input.fill(password)
        self.login_button.click()
