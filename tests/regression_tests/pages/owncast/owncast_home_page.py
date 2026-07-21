from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OwncastHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role("heading", name="New Owncast Server", level=1)
