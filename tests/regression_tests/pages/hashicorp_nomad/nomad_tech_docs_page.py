from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class NomadTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.hashicorp_nomad_header = self.page.get_by_role("heading", name="HashiCorp Nomad", level=1, exact=True)
