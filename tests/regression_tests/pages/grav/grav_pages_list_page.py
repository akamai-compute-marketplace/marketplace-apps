from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GravPagesListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_button = self.page.get_by_role("button", name="Add Page")
        self.page_title_input = self.page.locator('#page-title')
        self.published_button = self.page.get_by_role("button", name="Published")
        self.continue_button = self.page.get_by_role("button", name="Continue")

    def create_page(self, title: str):
        self.add_button.click()
        self.page_title_input.fill(title)
        self.published_button.click()
        self.continue_button.click()
