from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.content_link = self.page.get_by_role("link", name="Content", exact=True)
        self.create_article_button = self.page.get_by_role("link", name="Add Article", exact=True).first
        self.menus_link = self.page.get_by_role("link", name="Menus", exact=True)
        self.create_menu_item_button = self.page.get_by_role("link", name="Add Site Menu Item", exact=True)
        self.guided_tour_dialog = self.page.get_by_role("dialog")
        self.guided_tour_hide_forever_button = self.guided_tour_dialog.get_by_role("button", name="Hide Forever")

    def dismiss_guided_tour(self):
        self.guided_tour_hide_forever_button.click()

    def create_article(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.content_link.click()
        self.create_article_button.click()

    def create_menu_item(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.menus_link.click()
        self.create_menu_item_button.click()
