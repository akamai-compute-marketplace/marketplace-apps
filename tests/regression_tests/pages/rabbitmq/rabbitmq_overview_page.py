from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class RabbitMQOverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.overview_heading = self.page.get_by_role("heading", name="Overview", exact=True)
        self.logout_button = self.page.get_by_role("button", name="Log out")
