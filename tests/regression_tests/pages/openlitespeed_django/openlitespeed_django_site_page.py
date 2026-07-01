from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OpenLitespeedDjangoSitePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.hello_world_text = self.page.get_by_text("Hello, world!")
