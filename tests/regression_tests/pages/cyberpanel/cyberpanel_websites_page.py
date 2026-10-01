from playwright.sync_api import Locator

from regression_tests.pages.base_page import BasePage


class CyberPanelWebsitesPage(BasePage):

    def wait_for_websites_to_load(self, timeout: int = 30000):
        self.page.wait_for_timeout(timeout)
        self.reload()

    def website_name(self, domain: str) -> Locator:
        return self.page.locator("span.domain", has_text=domain)
