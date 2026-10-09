from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class Neo4jTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.neo4j_header = self.page.get_by_role("heading", name="Neo4j", level=1, exact=True)
