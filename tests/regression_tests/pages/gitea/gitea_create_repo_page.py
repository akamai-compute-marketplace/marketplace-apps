from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GiteaCreateRepoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.repo_name_input = self.page.locator("#repo_name")
        self.create_button = self.page.get_by_role("button", name="Create Repository")

    def create_repo(self, repo_name: str):
        self.repo_name_input.fill(repo_name)
        self.create_button.click()
