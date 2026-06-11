from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaCreateMenuItemPage(BasePage):
    def __init__(self, page: Page, article_title: str, menu_item_title: str):
        super().__init__(page)
        self.page.wait_for_load_state("domcontentloaded")
        self.article_title = article_title
        self.menu_item_title = menu_item_title

        self.menu_item_title_input = self.page.get_by_role("textbox", name="Title", exact=True)
        self.menu_item_type_button = self.page.get_by_role("button", name="Select", exact=True)
        self.modal_frame = self.page.frame_locator('.iframe-content')
        self.modal_frame_articles_section = self.modal_frame.get_by_role("button", name=" Articles ")
        self.modal_frame_single_article_section = self.modal_frame.get_by_role("link", name="Single Article")
        self.select_article_button = self.page.locator('button[data-modal-config*="Select an Article"]')
        self.article_frame = self.page.frame_locator('.joomla-dialog-container iframe')
        self.article_link = self.article_frame.get_by_role("link", name=self.article_title, exact=True)
        self.save_and_close_button = self.page.get_by_role("button", name="Save & Close", exact=True)


    def complete_menu_item_and_save(self):
        self.menu_item_title_input.fill(self.menu_item_title)
        self.menu_item_type_button.click()
        self.page.wait_for_load_state("networkidle")
        self.modal_frame_articles_section.click()
        self.modal_frame_single_article_section.click()
        self.select_article_button.click()
        self.article_link.click()
        self.save_and_close_button.click()
