from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class LangflowTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.langflow_header = self.page.get_by_role("heading", name="Langflow", level=1, exact=True)
