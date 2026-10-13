from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class LiveswitchTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.liveswitch_header = self.page.get_by_role("heading", name="LiveSwitch", level=1, exact=True)
