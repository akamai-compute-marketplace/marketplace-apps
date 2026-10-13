from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OwncastTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.owncast_header = self.page.get_by_role("heading", name="Owncast", level=1, exact=True)
