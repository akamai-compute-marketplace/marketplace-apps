from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OpenlitespeedCpanelDefaultPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.sorry_text = self.page.get_by_text("SORRY!")
