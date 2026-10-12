from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class SecureYourServerTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.secure_your_server_header = self.page.get_by_role("heading", name="Secure Your Server", level=1, exact=True)
