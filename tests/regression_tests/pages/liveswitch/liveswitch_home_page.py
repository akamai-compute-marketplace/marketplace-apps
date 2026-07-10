from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class LiveswitchHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logo = self.page.get_by_role("img", name="LiveSwitch Configuration Console")
        self.next_button = self.page.get_by_role("button", name="Next")
