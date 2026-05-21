from playwright.sync_api import Page

from regression_tests.pages.saltcorn.saltcorn_base_page import SaltcornBasePage


class SaltcornCreateTablePage(SaltcornBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.table_name_input = self.page.locator('#inputname')
        self.create_table_button = self.page.get_by_role("button", name="Create", exact=True)


    def create_table(self, table_name: str):
        self.table_name_input.fill(table_name)
        self.create_table_button.click()
