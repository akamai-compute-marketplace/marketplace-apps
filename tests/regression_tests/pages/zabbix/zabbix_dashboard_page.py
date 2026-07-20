from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class ZabbixDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.global_view_heading = self.page.get_by_role("heading", name="Global view", level=1)
        self.system_information_heading = self.page.get_by_role("heading", name="System information")
        self.server_running_row = self.page.locator(
            "tr", has=self.page.locator("th", has_text="Zabbix server is running")
        )
        self.server_running_value = self.server_running_row.locator("td").first
