from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GravPagesListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_button = self.page.get_by_role("button", name="Add")
        self.page_title_input = self.page.locator('#new-page input[name="data[title]"]')
        self.continue_button = self.page.get_by_role("button", name="Continue")

    def create_page(self, title: str):
        self.add_button.click()
        self.page_title_input.fill(title)
        self.continue_button.click()
