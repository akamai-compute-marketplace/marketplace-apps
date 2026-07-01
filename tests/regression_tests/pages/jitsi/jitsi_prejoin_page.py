from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JitsiPrejoinPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Join meeting")
        self.display_name_input = self.page.get_by_role("textbox", name="Enter your name")
        # data-testid is the most stable selector here — role-based click resolves to this attribute.
        self.join_meeting_button = self.page.get_by_test_id("prejoin.joinMeeting")

    def join(self, display_name: str):
        self.display_name_input.fill(display_name)
        self.join_meeting_button.click()
