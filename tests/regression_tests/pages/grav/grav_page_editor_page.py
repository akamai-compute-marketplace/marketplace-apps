from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GravPageEditorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.content_editor = self.page.locator(".CodeMirror")
        self.save_button = self.page.get_by_role("button", name="Save")

    def set_content(self, text: str):
        # The body field is a CodeMirror editor over a hidden textarea; Playwright can't type
        # into it directly, so the value is set through the CodeMirror instance API.
        self.content_editor.evaluate("(el, text) => el.CodeMirror.setValue(text)", text)

    def save(self):
        self.save_button.click()
