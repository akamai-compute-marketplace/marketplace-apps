from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenclawTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.openclaw_header = self.page.get_by_role("heading", name="OpenClaw", level=1, exact=True)
