from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GiteaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.gitea_header = self.page.get_by_role("heading", name="Gitea", level=1, exact=True)
