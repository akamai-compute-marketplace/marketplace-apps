from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaCreateArticlePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.article_title_input = self.page.get_by_role("textbox", name="Title", exact=True)
        self.article_save_and_close_button = self.page.get_by_role("button", name="Save & Close", exact=True)
        self.editor_toggle_button = self.page.get_by_role("button", name="Toggle Editor", exact=True)
        self.editor_frame = self.page.frame_locator('#jform_articletext_ifr')
        self.editor_textarea = self.page.locator('#jform_articletext')

    def complete_article_and_save(self, article_title, article_text):
        self.page.wait_for_load_state("networkidle")
        self.article_title_input.fill(article_title)
        self.editor_toggle_button.click()
        self.editor_textarea.fill(article_text)
        self.article_save_and_close_button.click()
