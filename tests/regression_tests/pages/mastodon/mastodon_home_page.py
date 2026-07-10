from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MastodonHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.compose_input = self.page.get_by_role("textbox", name="What's on your mind?")
        self.post_button = self.page.get_by_role("button", name="Post")
        self.home_feed = self.page.get_by_role("region", name="Home")

    def write_post(self, text: str):
        self.compose_input.fill(text)
        self.post_button.click()
