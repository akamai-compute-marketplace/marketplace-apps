from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class LempHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="LEMP Stack", exact=True)
        self.what_is_lemp_heading = self.page.get_by_role("heading", name="What is LEMP?")
