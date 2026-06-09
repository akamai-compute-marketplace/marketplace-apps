from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class SaltcornBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.dashboard_link = self.page.get_by_role("link", name="Saltcorn", exact=True)

    def navigate_to_dashboard(self):
        self.dashboard_link.click()
