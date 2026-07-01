from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DrupalCreateArticlePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title_input = self.page.locator("#edit-title-0-value")
        self.body_input = self.page.locator(".ck-editor__editable")
        self.save_button = self.page.locator("#node-article-form #edit-submit")

    def create_article(self, title: str, body: str):
        self.title_input.fill(title)
        self.body_input.fill(body)
        self.save_button.click()
