from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from regression_tests.pages.base_page import BasePage


class OpenVPNLicenseAgreementPage(BasePage):
    """
    One-time License Agreement dialog shown on first admin login after a fresh deploy.
    Once accepted, it never reappears for that instance.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role("heading", name="License Agreement")
        self.agree_button = self.page.get_by_role("button", name="Agree")
        self.decline_button = self.page.get_by_role("button", name="I Do Not Accept")

    def accept_if_present(self, timeout: int = 5000):
        try:
            self.heading.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            return
        self.agree_button.click()
