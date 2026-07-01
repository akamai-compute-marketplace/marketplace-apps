from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class LampHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="LAMP Stack", exact=True)
        self.what_is_lamp_heading = self.page.get_by_role("heading", name="What is LAMP?")
