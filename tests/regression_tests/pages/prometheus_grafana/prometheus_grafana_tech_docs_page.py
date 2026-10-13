from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PrometheusGrafanaTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.prometheus_grafana_header = self.page.get_by_role(
            "heading", name="Prometheus & Grafana", level=1, exact=True
        )
