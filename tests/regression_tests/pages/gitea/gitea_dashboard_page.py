from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GiteaDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.new_repository_link = self.page.get_by_role("link", name="New Repository")
