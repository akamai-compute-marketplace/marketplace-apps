from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class InfluxDBTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.influxdb_header = self.page.get_by_role("heading", name="InfluxDB", level=1, exact=True)
