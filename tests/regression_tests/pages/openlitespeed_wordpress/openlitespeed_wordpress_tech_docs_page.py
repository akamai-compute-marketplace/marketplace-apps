from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenlitespeedWordpressTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.openlitespeed_wordpress_header = self.page.get_by_role(
            "heading", name="OpenLiteSpeed WordPress", level=1, exact=True
        )
