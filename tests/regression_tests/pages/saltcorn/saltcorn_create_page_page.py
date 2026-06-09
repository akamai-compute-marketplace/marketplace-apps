from playwright.sync_api import Page

from regression_tests.pages.saltcorn.saltcorn_base_page import SaltcornBasePage


class SaltcornCreatePagePage(SaltcornBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.page_name_input = self.page.locator('#inputname')
        self.create_page_button = self.page.get_by_role("button", name="Save", exact=True)


    def create_page(self, page_name: str):
        self.page_name_input.fill(page_name)
        self.create_page_button.click()
