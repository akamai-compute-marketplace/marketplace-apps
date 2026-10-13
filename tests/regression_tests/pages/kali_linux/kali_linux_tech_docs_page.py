from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class KaliLinuxTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.kali_linux_header = self.page.get_by_role("heading", name="Kali Linux", level=1, exact=True)
