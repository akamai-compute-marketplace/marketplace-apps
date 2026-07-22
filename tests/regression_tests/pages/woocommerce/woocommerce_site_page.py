from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class WooCommerceSitePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        banner = self.page.get_by_role("banner")
        self.site_title_link = banner.get_by_role("link", name="My WP Site")
        self.shop_link = banner.get_by_role("link", name="Shop", exact=True)
