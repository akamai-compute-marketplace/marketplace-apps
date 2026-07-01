from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PeppermintCreateIssuePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title_input = self.page.get_by_role("textbox", name="Issue title")
        self.name_input = self.page.get_by_role("textbox", name="Name")
        self.email_input = self.page.get_by_role("textbox", name="Email")
        self.description_editor = self.page.locator(".ProseMirror[contenteditable='true']")
        self.create_ticket_button = self.page.get_by_role("button", name="Create Ticket")

    def create_issue(self, title: str, name: str, email: str, description: str):
        self.title_input.fill(title)
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.description_editor.fill(description)
        self.create_ticket_button.click()
