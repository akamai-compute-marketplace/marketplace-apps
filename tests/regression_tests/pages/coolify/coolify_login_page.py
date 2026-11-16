from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CoolifyLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.locator("input[name='email']")
        self.password_input = self.page.locator("input[name='password']")
        self.login_button = self.page.get_by_role("button", name="Login", exact=True)
        self.skip_setup_button = self.page.get_by_role("button", name="Skip setup", exact=True)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def skip_setup_if_present(self):
        try:
            self.skip_setup_button.wait_for(state="visible", timeout=10000)
            self.skip_setup_button.click()
        except Exception:
            pass
