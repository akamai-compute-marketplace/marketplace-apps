from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JoomlaArticlesPage(BasePage):
    def __init__(self, page: Page, article_title: str):
        super().__init__(page)
        self.article_title = article_title
        self.article_title_link = self.page.get_by_role("link", name=self.article_title, exact=True)
