from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MilvusBrowserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.acknowledge_button = self.page.get_by_role("button", name="Acknowledge")
        # First "Create Bucket" is the persistent sidebar button; the second appears in the open drawer.
        self.create_bucket_button = self.page.get_by_role("button", name="Create Bucket").first
        self.bucket_name_input = self.page.get_by_role("textbox", name="Bucket Name*")
        self.create_bucket_submit = self.page.locator("#create-bucket")

    def bucket_heading(self, name: str):
        return self.page.get_by_role("heading", name=name)

    def create_bucket(self, name: str):
        self.create_bucket_button.click()
        self.bucket_name_input.fill(name)
        self.create_bucket_submit.click()
