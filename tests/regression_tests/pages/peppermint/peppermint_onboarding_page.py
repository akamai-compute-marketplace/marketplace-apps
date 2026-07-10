from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from regression_tests.pages.base_page import BasePage


class PeppermintOnboardingPage(BasePage):
    """
    One-time welcome/onboarding screen shown right after the very first admin login on a fresh
    instance. Once dismissed, it never reappears for that instance.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.to_dashboard_button = self.page.get_by_role("button", name="To Dashboard")

    def complete_if_present(self, timeout: int = 30000):
        try:
            self.to_dashboard_button.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            return
        self.to_dashboard_button.click()
