from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GrafanaDataSourcePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.prometheus_type_button = page.get_by_role("button", name="Prometheus", exact=True)
        self.url_input = page.get_by_placeholder("http://localhost:9090")
        self.save_and_test_button = page.get_by_role("button", name="Save & test")
        self.success_message = page.get_by_role("status").filter(
            has_text="Successfully queried the Prometheus API."
        )

    def add_new_prometheus_data_source(self):
        self.prometheus_type_button.click()

    def set_url(self, url: str):
        self.url_input.fill(url)

    def save_and_test(self):
        self.save_and_test_button.click()
