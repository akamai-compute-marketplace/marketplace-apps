from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenlitespeedCpanelWhmInitialSetupPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.legal_documents_heading = self.page.get_by_role("heading", name="Legal Documents")
