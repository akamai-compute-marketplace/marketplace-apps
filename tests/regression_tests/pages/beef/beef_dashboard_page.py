from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class BeefDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logout_link = page.get_by_role("link", name="Logout")
