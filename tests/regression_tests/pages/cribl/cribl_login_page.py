from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CriblLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.ai_data_notice_continue_button = page.get_by_role(
            "dialog", name="Cribl AI will use your Organization’s data"
        ).get_by_role("button", name="Continue")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def dismiss_ai_data_notice_if_present(self):
        try:
            self.ai_data_notice_continue_button.wait_for(state="visible", timeout=10000)
            self.ai_data_notice_continue_button.click()
        except Exception:
            pass
