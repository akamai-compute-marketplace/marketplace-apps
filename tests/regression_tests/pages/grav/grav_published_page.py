from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GravPublishedPage(BasePage):
    def __init__(self, page: Page, body_text: str = None):
        super().__init__(page)

        if body_text:
            self.body_text = self.page.get_by_text(body_text)
