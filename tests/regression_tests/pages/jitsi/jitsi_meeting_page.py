from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JitsiMeetingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.toolbar_heading = self.page.get_by_role("heading", name="Toolbar")
        self.leave_meeting_button = self.page.get_by_role("button", name="Leave the meeting")
