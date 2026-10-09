from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class RubyRailsTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.ruby_rails_header = self.page.get_by_role("heading", name="Ruby on Rails", level=1, exact=True)
