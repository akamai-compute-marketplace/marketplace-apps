from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class AntMediaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.antmedia_header = self.page.get_by_role(
            "heading", name="Ant Media Server - Enterprise Edition", level=1, exact=True
        )
