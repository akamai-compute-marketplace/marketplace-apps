from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GemmaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.gemma_header = self.page.get_by_role("heading", name="Gemma3", level=1, exact=True)
