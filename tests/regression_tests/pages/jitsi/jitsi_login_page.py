from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JitsiLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="Jitsi Meet")
        self.meeting_name_input = self.page.get_by_role("textbox", name="Meeting name input")
        self.start_meeting_button = self.page.get_by_role("button", name="Start meeting")

    def start_meeting(self, room_name: str):
        self.meeting_name_input.fill(room_name)
        self.start_meeting_button.click()
