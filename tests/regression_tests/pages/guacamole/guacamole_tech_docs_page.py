from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GuacamoleTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.apache_guacamole_header = self.page.get_by_role("heading", name="Apache Guacamole", level=1, exact=True)
