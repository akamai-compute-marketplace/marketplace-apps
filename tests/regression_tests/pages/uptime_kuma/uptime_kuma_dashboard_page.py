from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class UptimeKumaDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_monitor_link = self.page.get_by_role("link", name="Add New Monitor")

    def go_to_add_monitor(self):
        self.add_monitor_link.click()
