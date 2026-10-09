from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class QwenTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.qwen_header = self.page.get_by_role("heading", name="Qwen", level=1, exact=True)
