from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class GPTTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.gpt_oss_header = self.page.get_by_role("heading", name="GPT-OSS", level=1, exact=True)
