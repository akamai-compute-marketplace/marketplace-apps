from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MsAgentFrameworkTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.ms_agent_framework_header = self.page.get_by_role("heading", name="Microsoft Agent Framework", level=1, exact=True)
