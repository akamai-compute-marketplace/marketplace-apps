from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OpenVPNStatusPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role("heading", name="Status", level=1)
        self.account_menu_button = self.page.get_by_role("button", name="Account menu")
