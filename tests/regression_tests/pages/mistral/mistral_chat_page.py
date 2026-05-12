from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class MistralChatPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.model_selector_input = self.page.locator("#model-selector-0-button")
        self.chat_input = self.page.locator("#chat-input")
        self.send_prompt_button = self.page.locator("#send-message-button")
        self.edit_prompt_button = self.page.locator("button[aria-label='Edit']")
        self.prompt_response_field = self.page.locator("#response-content-container")
        self.release_notes_proceed_button = self.page.locator("//button[contains(., \"Okay, Let's Go!\")]")

    def hide_release_notes(self):
        try:
            self.release_notes_proceed_button.wait_for(state="visible", timeout=5000)
            self.release_notes_proceed_button.click()
        except Exception:
            pass

    def send_prompt(self, prompt: str):
        self.chat_input.fill(prompt)
        self.send_prompt_button.click()