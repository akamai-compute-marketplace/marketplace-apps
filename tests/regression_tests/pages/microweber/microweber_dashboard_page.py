from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MicroweberDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button = self.page.get_by_role("button", name="ADD", exact=True)
        self.new_page_button = self.page.locator('div[onclick*="/admin/page/create?addEditContent=true"]')
        self.welcome_message = self.page.get_by_text("Welcome back, admin", exact=True)

    def open_new_page(self):
        self.add_button.click()
        self.new_page_button.click()
