from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NodejsHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.app_text = self.page.locator("pre")
