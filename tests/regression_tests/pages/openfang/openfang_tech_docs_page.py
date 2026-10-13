from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenFangTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.openfang_header = self.page.get_by_role("heading", name="OpenFang", level=1, exact=True)
