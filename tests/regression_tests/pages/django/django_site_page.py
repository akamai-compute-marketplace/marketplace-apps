from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DjangoSitePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = self.page.get_by_role(
            "heading", name="The install worked successfully! Congratulations!", level=1
        )
