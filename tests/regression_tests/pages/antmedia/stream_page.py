from playwright.sync_api import FrameLocator, Page, expect
from regression_tests.pages.base_page import BasePage


class StreamPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        frame_locator = self.page.frame_locator("#webrtc-publish-frame")
        self.stream_frame = self.StreamFrame(self, frame_locator)


    class StreamFrame:
        def __init__(self, stream_page: "StreamPage", frame_locator: FrameLocator):
            self.stream_page = stream_page
            self.frame = frame_locator
            self.start_publish_button = self.frame.locator("#start_publish_button")
            self.status_offline_label = self.frame.locator("#offlineInfo")
            self.status_online_label = self.frame.locator("#broadcastingInfo")

        def start_publishing(self, timeout: int = 10000, retries: int = 3):
            for attempt in range(retries):
                try:
                    expect(self.start_publish_button).to_be_enabled(timeout=timeout)
                    self.start_publish_button.click()
                    return
                except Exception:
                    if attempt < retries - 1:
                        print("Reloading page")
                        self.stream_page.page.reload()
                    else:
                        raise
