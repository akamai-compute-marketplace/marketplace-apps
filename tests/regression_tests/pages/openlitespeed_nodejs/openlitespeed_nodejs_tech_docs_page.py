from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenLitespeedNodejsTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.openlitespeed_nodejs_header = self.page.get_by_role(
            "heading", name="OpenLiteSpeed Node.js", level=1, exact=True
        )
