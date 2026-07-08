from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OdooAppsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.apps_menuitem = self.page.get_by_role("menuitem", name="Apps", exact=True)
        self.user_menu_button = self.page.get_by_role("button", name="User", exact=True)
