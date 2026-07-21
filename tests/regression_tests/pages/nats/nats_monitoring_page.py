from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NatsMonitoringPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.health_probe_link = self.page.locator('a[href="./healthz"]')
