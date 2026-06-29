from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoplinDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Joplin Server admin dashboard")
        self.logout_button = self.page.get_by_role("button", name="Logout")
