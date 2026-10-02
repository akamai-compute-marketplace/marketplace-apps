from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MicroweberPageEditor(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.empty_page_card = self.page.locator('a[href*="layout=clean.php"]')
        self.page_title_input = self.page.locator('input[name="title"]')
        self.save_button = self.page.get_by_role("button", name="SAVE", exact=True)

    def create_page(self, title: str):
        self.empty_page_card.click()
        self.page_title_input.fill(title)
        self.save_button.click()
        self.page.wait_for_url("**/admin/page/*/edit", timeout=30000)
