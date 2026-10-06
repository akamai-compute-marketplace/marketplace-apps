from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class EasypanelHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_project_button = self.page.get_by_role("button", name="Create Project")
        self.project_name_input = self.page.locator('input[name="name"]')
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)

    def create_project(self, name: str):
        self.create_project_button.click()
        self.project_name_input.fill(name)
        self.create_button.click()

    def get_project_label(self, name: str):
        return self.page.get_by_role("link", name=name, exact=True)

    def get_service_label(self, name: str):
        return self.page.get_by_text(name, exact=True)
