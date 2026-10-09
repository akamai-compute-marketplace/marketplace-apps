from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenlitespeedCpanelTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.openlitespeed_cpanel_header = self.page.get_by_role(
            "heading", name="LiteSpeed cPanel", level=1, exact=True
        )
