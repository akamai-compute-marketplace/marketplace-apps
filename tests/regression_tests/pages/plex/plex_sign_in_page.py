from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PlexSignInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        sign_in_frame = self.page.frame_locator("iframe")
        self.continue_with_email_button = sign_in_frame.get_by_role("button", name="Continue with Email")
