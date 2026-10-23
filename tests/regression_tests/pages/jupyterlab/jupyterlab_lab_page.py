import re

from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class JupyterlabLabPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.file_menu = self.page.get_by_role("menuitem", name="File")
        self.new_launcher_button = self.page.get_by_role("button", name=re.compile("New Launcher"))
        self.notebook_python3_button = self.page.get_by_role("tabpanel", name="Launcher").get_by_title("Python 3 (ipykernel)").first
        self.select_kernel_dialog = self.page.get_by_role("dialog").filter(has_text="Select Kernel")
        self.select_kernel_button = self.select_kernel_dialog.get_by_role("button", name="Select Kernel", exact=True)

    def open_new_notebook(self):
        self.new_launcher_button.click()
        self.notebook_python3_button.click()

    def accept_kernel_dialog(self):
        if self.select_kernel_dialog.is_visible():
            self.select_kernel_button.click()
