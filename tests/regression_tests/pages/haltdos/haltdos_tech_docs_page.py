from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class HaltdosTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.haltdos_header = self.page.get_by_role("heading", name="Haltdos Community WAF", level=1, exact=True)
