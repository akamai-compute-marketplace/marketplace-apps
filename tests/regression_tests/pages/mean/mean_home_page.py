from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MeanHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.hello_heading = self.page.get_by_role("heading", name="Hello, client")
        self.running_message = self.page.get_by_text("Congratulations! Your app is running.")
