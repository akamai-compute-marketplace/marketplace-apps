from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CriblRegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("[id='root.email']")
        self.accept_checkbox = page.get_by_text("I accept the license agreement")
        self.register_button = page.get_by_role("button", name="Register")

    def register(self, email: str):
        self.email_input.fill(email)
        self.accept_checkbox.click()
        self.register_button.click()
