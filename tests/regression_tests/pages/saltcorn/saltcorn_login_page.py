from playwright.sync_api import Page

from regression_tests.pages.saltcorn.saltcorn_base_page import SaltcornBasePage


class SaltcornLoginPage(SaltcornBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input = self.page.locator('#inputemail')
        self.password_input = self.page.locator('#inputpassword')
        self.login_button = self.page.get_by_role("button", name="Login", exact=True)


    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
