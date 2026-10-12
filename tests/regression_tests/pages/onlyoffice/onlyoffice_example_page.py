from playwright.sync_api import Locator, Page

from regression_tests.pages.base_page import BasePage


class OnlyofficeExamplePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_document_link = self.page.get_by_role("link", name="Document", exact=True)
        self.sample_content_checkbox = self.page.locator("#createSample")
        self.stored_list = self.page.locator(".stored-list")

    def create_document(self, with_sample_content: bool = False) -> Page:
        self.sample_content_checkbox.set_checked(with_sample_content)
        with self.page.context.expect_page() as editor_tab:
            self.create_document_link.click()
        return editor_tab.value

    def stored_file(self, file_name: str) -> Locator:
        return self.stored_list.get_by_role("link", name=file_name, exact=True)
