from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class CpanelTrialPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.trial_heading = self.page.get_by_role(
            "heading", name="Get Started with a Free cPanel Trial!"
        )
        self.proceed_to_store_button = self.page.locator("#continue")
