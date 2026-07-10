from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.active_live_streams_label = self.page.locator("div.numbers").filter(has_text="Active Live Streams")
