from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CoolifyDatabasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.start_button = self.page.get_by_role("button", name="Start", exact=True)
        self.startup_logs_dialog = self.page.get_by_role("dialog", name="Database Startup Logs")
        self.startup_logs_finished_status = self.startup_logs_dialog.get_by_role("status")
        self.startup_logs_close_button = self.startup_logs_dialog.get_by_role("button", name="Close", exact=True)
        self.running_status_button = self.page.get_by_role("button", name="Running", exact=True)
        self.healthcheck_healthy_item = self.page.get_by_role("menuitem", name="Healthcheck Healthy", exact=True)

    def start(self):
        self.start_button.click()

    def close_startup_logs(self):
        self.startup_logs_close_button.click()

    def open_status_menu(self):
        self.running_status_button.click()
