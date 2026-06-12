from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class AzuracastSetupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.station_name_input = self.page.get_by_role("textbox", name="Name Required")
        self.create_and_continue_button = self.page.get_by_role("button", name="Create and Continue")
        self.site_base_url_input = self.page.get_by_role("textbox", name="Site Base URL Required")
        self.save_and_continue_button = self.page.get_by_role("button", name="Save and Continue")

    def create_station(self, name: str):
        self.station_name_input.fill(name)
        self.create_and_continue_button.click()

    def save_settings(self, base_url: str):
        self.site_base_url_input.fill(base_url)
        self.save_and_continue_button.click()
