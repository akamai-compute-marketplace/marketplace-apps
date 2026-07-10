from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class MoodleDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_heading = self.page.get_by_role("heading", name="Dashboard", level=1, exact=True)
