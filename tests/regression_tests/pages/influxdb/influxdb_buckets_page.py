from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class InfluxDBBucketsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_bucket_button = self.page.get_by_test_id("Create Bucket")
        self.bucket_name_input = self.page.get_by_test_id("bucket-form-name")
        self.bucket_form_submit = self.page.get_by_test_id("bucket-form-submit")

    def create_bucket(self, name: str):
        self.create_bucket_button.click()
        self.bucket_name_input.fill(name)
        self.bucket_form_submit.click()

    def get_bucket_item(self, name: str):
        return self.page.get_by_text(name, exact=True)
