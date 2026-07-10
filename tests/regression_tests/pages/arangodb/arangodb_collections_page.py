from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class ArangoDBCollectionsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.collections_nav = self.page.locator("#collections")
        self.add_collection_button = self.page.get_by_role("button", name="Add collection")
        self.collection_name_input = self.page.locator("input[name='name']")
        self.create_button = self.page.get_by_role("button", name="Create")
        self.collections_content = self.page.locator("#content-react")

    def navigate_to_collections(self):
        self.collections_nav.click()
        self.page.wait_for_load_state("networkidle")

    def create_collection(self, name: str):
        self.add_collection_button.click()
        self.collection_name_input.fill(name)
        self.create_button.click()
        self.page.wait_for_load_state("networkidle")
