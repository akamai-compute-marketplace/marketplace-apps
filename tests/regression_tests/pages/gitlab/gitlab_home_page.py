from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GitLabHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_new_button = self.page.get_by_role("button", name="Create new…")
