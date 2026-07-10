from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class AirflowDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.dag_runs_header = self.page.get_by_role("heading", name="DAGs")
