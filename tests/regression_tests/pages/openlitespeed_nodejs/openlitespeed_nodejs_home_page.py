from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenLiteSpeedNodeJsHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.welcome_message = self.page.get_by_text("Hello World! From OpenLiteSpeed NodeJS", exact=True)
