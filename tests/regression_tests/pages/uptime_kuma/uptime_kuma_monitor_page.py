from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class UptimeKumaMonitorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.monitor_heading = self.page.get_by_role("heading", level=1)
        self.status_badge = self.page.locator(".d-flex.align-items-center.justify-content-between .badge.bg-primary")
