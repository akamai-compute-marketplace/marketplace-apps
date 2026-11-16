from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CoolifyEnvironmentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.new_resource_link = self.page.get_by_role("link", name="New resource", exact=True)
        self.search_resources_input = self.page.get_by_role("searchbox", name="Search resources", exact=True)
        self.configure_sqlite_button = self.page.get_by_role("button", name="Configure SQLite", exact=True)

    def get_project_link(self, name: str):
        return self.page.get_by_role("main").get_by_role("link", name=name, exact=True)

    def add_sqlite_database(self):
        self.new_resource_link.click()
        self.search_resources_input.fill("sqlite")
        self.configure_sqlite_button.click()
