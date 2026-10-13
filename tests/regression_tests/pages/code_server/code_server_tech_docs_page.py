from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class CodeServerTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.code_server_header = self.page.get_by_role("heading", name="VS Code Server", level=1, exact=True)
