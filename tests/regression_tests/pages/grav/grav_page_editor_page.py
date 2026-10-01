from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GravPageEditorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.content_editor = self.page.locator('div[contenteditable="true"][role="textbox"]')
        self.save_button = self.page.get_by_role("button", name="Save")

    def set_content(self, text: str):
        self.content_editor.fill(text)
        self.save_button.click()
