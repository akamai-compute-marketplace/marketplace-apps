from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class AkauntingDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_navigation = self.page.get_by_text("Dashboard", exact=True)
        self.welcome_heading = self.page.get_by_text("Welcome", exact=True)
