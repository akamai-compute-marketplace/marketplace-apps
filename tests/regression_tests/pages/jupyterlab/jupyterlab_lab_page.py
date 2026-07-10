import re

from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class JupyterlabLabPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.file_menu = self.page.get_by_role("menuitem", name="File")
        self.new_launcher_button = self.page.get_by_role("button", name=re.compile("New Launcher"))
        # Scoped to the Launcher tabpanel so open notebook kernel buttons don't shadow it.
        # First within the Launcher is the Notebook section card; second is Console.
        self.notebook_python3_button = self.page.get_by_role("tabpanel", name="Launcher").get_by_title("Python 3 (ipykernel)").first
