from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class CodeServerMainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.view_switcher = self.page.get_by_role("tablist", name="Active View Switcher")
        self.status_bar = self.page.locator(".statusbar")
