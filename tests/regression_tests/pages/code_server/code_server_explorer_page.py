from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class CodeServerExplorerPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.trust_yes_button = self.page.get_by_role("button", name="Yes, I trust the authors")
        self.explorer_section = self.page.locator("div[aria-label='Explorer Section: admin'].pane-header")
        self.new_file_button = self.page.locator("[aria-label='New File...']")
        self.filename_input = self.page.locator(".monaco-inputbox input")

    def open_folder(self, base_url: str, folder: str = "/home/admin"):
        self.navigate(f"{base_url}/?folder={folder}")

    def handle_trust_dialog(self):
        try:
            self.trust_yes_button.click(timeout=10000)
        except Exception:
            pass

    def wait_for_explorer(self):
        self.explorer_section.wait_for(state="visible", timeout=15000)

    def create_new_file(self, filename: str):
        self.explorer_section.hover()
        self.new_file_button.click()
        self.filename_input.fill(filename)
        self.filename_input.press("Enter")

    def get_file_item(self, filename: str):
        return self.page.locator(f'.explorer-folders-view [aria-label="~/{filename}"]').first
