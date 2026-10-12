from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class UptimeKumaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.uptime_kuma_header = self.page.get_by_role("heading", name="Uptime Kuma", level=1, exact=True)
