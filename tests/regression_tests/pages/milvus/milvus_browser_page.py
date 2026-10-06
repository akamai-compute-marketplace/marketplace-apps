from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MilvusBrowserPage(BasePage):
    def __init__(self, page: Page, bucket_name: str = ''):
        super().__init__(page)
        self.bucket_name = bucket_name
        self.create_bucket_button = self.page.get_by_role("button", name="Create Bucket", exact=True)
        self.bucket_name_input = self.page.locator("#bucket-name")
        self.create_bucket_submit = self.page.get_by_role("button", name="Create", exact=True)
        self.bucket_name_label = self.page.get_by_role("link", name=self.bucket_name, exact=True)

    def create_bucket(self):
        self.create_bucket_button.click()
        self.bucket_name_input.fill(self.bucket_name)
        self.create_bucket_submit.click()
