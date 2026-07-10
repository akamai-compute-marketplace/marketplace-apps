from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class VaultDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.secrets_engines_link = page.get_by_role("link", name="Secrets", exact=True)

    def open_secrets_engines(self):
        self.secrets_engines_link.click()
