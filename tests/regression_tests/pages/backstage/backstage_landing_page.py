from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class BackstageLandingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.app_heading = self.page.get_by_role("heading", name="Scaffolded Backstage App", level=1)
        self.guest_enter_button = self.page.get_by_role("button", name="Enter")
