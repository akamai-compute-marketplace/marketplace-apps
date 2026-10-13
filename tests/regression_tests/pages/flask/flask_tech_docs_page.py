from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class FlaskTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.flask_header = self.page.get_by_role("heading", name="Flask", level=1, exact=True)
