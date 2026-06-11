from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaMenuItemsPage(BasePage):
    def __init__(self, page: Page, menu_item_title: str):
        super().__init__(page)
        self.menu_item_title = menu_item_title
        self.menu_item_title = self.page.get_by_role("link", name=self.menu_item_title, exact=True)
