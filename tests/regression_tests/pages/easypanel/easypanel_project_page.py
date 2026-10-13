from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class EasypanelProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_service_button = self.page.get_by_role("link", name="Service", exact=True)
        self.select_app_button = self.page.get_by_role("button", name="App", exact=True)
        self.service_name_input = self.page.locator('input[name="serviceName"]')
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)

    def create_service(self, name: str):
        self.create_service_button.click()
        self.select_app_button.click()
        self.service_name_input.fill(name)
        self.create_button.click()
