from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CoolifyDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.projects_nav_link = self.page.get_by_role("navigation").get_by_role("link", name="Projects", exact=True)
        self.new_project_button = self.page.get_by_role("button", name="New project", exact=True)
        self.project_name_input = self.page.get_by_role("textbox", name="Your project name", exact=True)
        self.create_project_button = self.page.get_by_role("button", name="Create project", exact=True)

    def create_project(self, name: str):
        self.new_project_button.click()
        self.project_name_input.fill(name)
        self.create_project_button.click()
