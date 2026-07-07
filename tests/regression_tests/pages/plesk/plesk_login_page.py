from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PleskLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.page.locator("#login_name")
        self.password_input = self.page.locator("#passwd")
        self.login_button = self.page.locator(".login-page__login-button")
        self.accept_all_cookies_button = self.page.get_by_role("button", name="Accept all cookies")

    def dismiss_cookie_banner_if_present(self, timeout: int = 3000):
        try:
            self.accept_all_cookies_button.click(timeout=timeout)
        except Exception:
            pass

    def login(self, username: str, password: str):
        self.dismiss_cookie_banner_if_present()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

