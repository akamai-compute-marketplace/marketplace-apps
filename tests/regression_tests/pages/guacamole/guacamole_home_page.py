from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GuacamoleHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.recent_connections_heading = self.page.get_by_role("heading", name="Recent Connections")
