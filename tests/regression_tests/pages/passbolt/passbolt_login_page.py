from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PassboltLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input = self.page.locator("#username-input")
        self.terms_checkbox = self.page.locator("#checkbox-terms")
        self.next_button = self.page.locator("button[type='submit']")
