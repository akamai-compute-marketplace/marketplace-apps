from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PiholeDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_nav_link = self.page.get_by_role("link", name="Dashboard")
        self.status_indicator = self.page.locator("#status")
