from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PeppermintIssuesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def issue_link(self, title: str):
        return self.page.get_by_role("link", name=title)
