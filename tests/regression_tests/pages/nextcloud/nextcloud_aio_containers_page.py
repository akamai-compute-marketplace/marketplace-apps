from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NextcloudAioContainersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.submit_domain_button = self.page.get_by_role("button", name="Submit domain", exact=True)
