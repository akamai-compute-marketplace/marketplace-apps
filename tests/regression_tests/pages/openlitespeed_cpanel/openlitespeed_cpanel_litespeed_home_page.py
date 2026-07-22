from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenlitespeedCpanelLitespeedHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_heading = self.page.get_by_role("heading", name="Home", level=2)
        self.log_off_link = self.page.get_by_role("link", name="Log Off")
