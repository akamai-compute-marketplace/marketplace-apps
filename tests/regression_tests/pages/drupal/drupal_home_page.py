from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DrupalHomePage(BasePage):
    def __init__(self, page: Page, article_title: str = None, article_body: str = None):
        super().__init__(page)

        self.logout_link = self.page.get_by_role("link", name="Log out")
        if article_title:
            self.article_heading = self.page.get_by_role("heading", name=article_title, level=2)
        if article_body:
            self.article_body = self.page.get_by_text(article_body)
