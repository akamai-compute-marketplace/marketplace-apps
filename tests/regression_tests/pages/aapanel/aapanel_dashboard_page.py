from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class AaPanelDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_navigation = self.page.get_by_text("Home", exact=True).first
