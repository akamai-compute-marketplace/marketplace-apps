from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class FlaskHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role("heading", name="Welcome to Your Flask App", level=1)
