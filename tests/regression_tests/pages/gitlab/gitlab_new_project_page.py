from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GitLabNewProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_blank_project_link = self.page.locator('a[href="#blank_project"]').first
        self.project_name_input = self.page.get_by_role("textbox", name="Project name Project name")
        self.namespace_button = self.page.get_by_role("button", name="Pick a group or namespace")
        self.create_project_button = self.page.get_by_role("button", name="Create project")

    def create_project(self, name: str):
        self.create_blank_project_link.click()
        self.project_name_input.fill(name)
        self.namespace_button.click()
        self.page.get_by_role("option", name="root").click()
        self.create_project_button.click()
