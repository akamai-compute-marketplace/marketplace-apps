from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class JoomlaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.joomla_header = self.page.get_by_role("heading", name="Joomla", level=1, exact=True)
