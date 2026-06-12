from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CloudronSetupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Domain Setup")
        self.domain_input = page.locator("#domainInput")
