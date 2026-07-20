from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class WazuhOverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.breadcrumb = self.page.get_by_role("navigation", name="breadcrumb")
