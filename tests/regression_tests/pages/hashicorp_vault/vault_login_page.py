from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class VaultLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.token_field = page.locator('input[name="token"]')
        self.sign_in_button = page.get_by_role("button", name="Sign in")

    def sign_in(self, token: str):
        self.token_field.fill(token)
        self.sign_in_button.click()
