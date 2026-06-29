from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class HarborProjectsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.projects_heading = self.page.get_by_role("heading", name="Projects", level=2)
        self.new_project_button = self.page.get_by_role("button", name="New Project")
        self.project_name_input = self.page.locator("#create_project_name")
        self.ok_button = self.page.get_by_role("button", name="OK")

    def create_project(self, name: str):
        self.new_project_button.click()
        self.project_name_input.fill(name)
        self.ok_button.click()

    def get_project_link(self, name: str):
        return self.page.get_by_role("link", name=name, exact=True)
