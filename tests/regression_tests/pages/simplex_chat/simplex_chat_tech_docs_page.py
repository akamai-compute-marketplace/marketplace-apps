from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class SimplexChatTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.simplex_chat_header = self.page.get_by_role("heading", name="SimpleX Chat", level=1, exact=True)
