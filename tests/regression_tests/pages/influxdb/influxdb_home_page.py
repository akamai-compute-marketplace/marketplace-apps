from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class InfluxDBHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.get_started_heading = self.page.get_by_role("heading", name="Get Started")
