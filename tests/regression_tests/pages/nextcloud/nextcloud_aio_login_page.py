from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NextcloudAioLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Nextcloud AIO Login", exact=True)
        self.password_input = self.page.locator("#master-password")
        self.login_button = self.page.get_by_role("button", name="Log in", exact=True)

    def login(self, passphrase: str):
        self.password_input.fill(passphrase)
        self.login_button.click()
