from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class CloudronTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cloudron_header = self.page.get_by_role("heading", name="Cloudron", level=1, exact=True)
