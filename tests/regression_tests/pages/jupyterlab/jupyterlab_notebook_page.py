from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class JupyterlabNotebookPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.run_cell_button = self.page.get_by_role("button", name="Run this cell and advance")
        self.notebook_content = self.page.get_by_role("region", name="notebook content")
        self.active_cell_input = self.page.get_by_role("region", name="notebook content").get_by_role("textbox").first
