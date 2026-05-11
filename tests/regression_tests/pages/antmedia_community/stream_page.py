from playwright.sync_api import FrameLocator, Page
from regression_tests.pages.base_page import BasePage


class StreamPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        frame_locator = self.page.frame_locator("#webrtc-publish-frame")
        self.stream_frame = self.StreamFrame(frame_locator)


    class StreamFrame:
        def __init__(self, frame_locator: FrameLocator):
            self.frame = frame_locator
            self.start_publish_button = self.frame.locator("#start_publish_button")
            self.status_offline_label = self.frame.locator("#offlineInfo")
            self.status_online_label = self.frame.locator("#broadcastingInfo")

        def start_publishing(self):
            self.start_publish_button.click()
