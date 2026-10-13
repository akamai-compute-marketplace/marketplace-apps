from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class AntMediaCommunityTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.antmedia_community_header = self.page.get_by_role(
            "heading", name="Ant Media Server - Community Edition", level=1, exact=True
        )
