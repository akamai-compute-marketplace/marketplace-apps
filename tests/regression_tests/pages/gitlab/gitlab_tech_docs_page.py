from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GitLabTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.gitlab_header = self.page.get_by_role("heading", name="GitLab", level=1, exact=True)
