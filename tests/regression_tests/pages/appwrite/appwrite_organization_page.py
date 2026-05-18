from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class AppwriteOrganizationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.profile_button = self.page.locator("button:has(img[data-avatar])").first
        self.profile_tooltip = self.page.locator("div[role='tooltip']")
        self.create_project_button = self.page.get_by_role('button', name='Create project').first
        self.project_name_input = self.page.locator("#name")
        self.create_button = self.page.locator("button[type='submit']")
        self.menu_bar = self.page.get_by_role('menubar')

    def open_profile_tooltip(self):
        self.profile_button.click()

    def create_project(self, name: str):
        self.create_project_button.click()
        self.project_name_input.clear()
        self.project_name_input.fill(name)
        self.create_button.click()
