from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DjangoDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role("heading", name="Site administration", level=1)
        self.view_site_link = self.page.get_by_role("link", name="View site")

    def view_site(self):
        self.view_site_link.click()
