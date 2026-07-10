from playwright.sync_api import Page
from regression_tests.pages.saltcorn.saltcorn_base_page import SaltcornBasePage


class SaltcornDashboardPage(SaltcornBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_table_button = self.page.get_by_role("link", name="Create table", exact=True)
        self.create_page_button = self.page.get_by_role("link", name="Create page", exact=True)
        self.tables_card = self.page.locator('.welcome-page-entity-list').filter(has=page.locator('a[href="/table"]'))
        self.pages_card = self.page.locator('.welcome-page-entity-list').filter(has=page.locator('a[href="/pageedit"]'))

    def navigate_to_create_table(self):
        self.create_table_button.click()

    def navigate_to_create_page(self):
        self.create_page_button.click()
