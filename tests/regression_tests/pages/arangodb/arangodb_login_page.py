from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class ArangoDBLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.page.locator("#loginUsername")
        self.password_input = self.page.locator("#loginPassword")
        self.login_button = self.page.locator("#submitLogin")
        self.select_db_button = self.page.locator("#goToDatabase")
        self.user_bar = self.page.locator("#userBar")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.select_db_button.click()
