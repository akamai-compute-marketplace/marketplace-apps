from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PleskTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.plesk_header = self.page.get_by_role("heading", name="Plesk", level=1, exact=True)
