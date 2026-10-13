from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class NetFoundryEdgeRouterTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.netfoundry_edge_router_header = self.page.get_by_role("heading", name="NetFoundry Edge Router", level=1, exact=True)
