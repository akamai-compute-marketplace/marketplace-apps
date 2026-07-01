from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MastodonLandingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_link = self.page.get_by_role("link", name="Login", exact=True)
        self.trending_heading = self.page.get_by_role("heading", name="Trending")
