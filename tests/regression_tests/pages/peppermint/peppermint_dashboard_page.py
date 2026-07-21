from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PeppermintDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.account_menu_button = self.page.get_by_role("button", name="admin", exact=True)
        self.new_issue_button = self.page.get_by_role("button", name="New Issue c")

    def open_new_issue_dialog(self):
        self.new_issue_button.click()
