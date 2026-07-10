from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CyberPanelDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_menu_item = self.page.locator("a.menu-item.active", has_text="Dashboard")
