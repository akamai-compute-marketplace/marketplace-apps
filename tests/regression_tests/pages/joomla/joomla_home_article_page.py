from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaHomeArticlePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.article_title = self.page.get_by_role("heading", level=1)
        self.article_text = self.page.locator(".com-content-article__body")
