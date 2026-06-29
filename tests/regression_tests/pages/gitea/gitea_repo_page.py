from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GiteaRepoPage(BasePage):
    def __init__(self, page: Page, repo_name: str):
        super().__init__(page)

        self.repo_name_link = self.page.get_by_role("link", name=repo_name, exact=True)
