from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class UptimeKumaAddMonitorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.friendly_name_input = self.page.get_by_role("textbox", name="Friendly Name")
        self.url_input = self.page.get_by_role("textbox", name="URL")
        self.save_button = self.page.get_by_role("button", name="Save")

    def add_monitor(self, friendly_name: str, url: str):
        self.friendly_name_input.fill(friendly_name)
        self.url_input.fill(url)
        self.save_button.click()
