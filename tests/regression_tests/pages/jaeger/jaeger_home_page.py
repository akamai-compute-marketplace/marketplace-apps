from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JaegerHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.search_nav_link = self.page.get_by_role("menuitem", name="Search")
