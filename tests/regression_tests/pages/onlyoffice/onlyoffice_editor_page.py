from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class OnlyofficeEditorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.editor_frame = self.page.frame_locator("iframe[name='frameEditor']")
        self.document_name_input = self.editor_frame.locator("#title-doc-name")
        self.document_area = self.editor_frame.locator("#editor_sdk")
        self.page_counter = self.editor_frame.locator("#label-pages")
