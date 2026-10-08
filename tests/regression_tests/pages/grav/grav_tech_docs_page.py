from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GravTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.grav_header = self.page.get_by_role("heading", name="Grav", level=1, exact=True)
