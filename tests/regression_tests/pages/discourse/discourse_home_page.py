from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class DiscourseHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.log_in_button = self.page.get_by_role("button", name="Log In", exact=True)
        self.new_topic_button = self.page.get_by_role("button", name="New Topic", exact=True)
        self.topic_title_input = self.page.get_by_role("textbox", name="Type title, or paste a link here", exact=True)
        self.topic_content_input = self.page.locator('div.ProseMirror[contenteditable="true"]')
        self.create_topic_button = self.page.get_by_role("button", name="Create Topic", exact=True)

    def open_login_page(self):
        self.log_in_button.click()

    def create_new_topic(self, title: str, content: str):
        self.new_topic_button.click()
        self.topic_title_input.fill(title)
        self.topic_content_input.fill(content)
        self.create_topic_button.click()

    def get_topic_link(self, title: str):
        return self.page.locator(f'a.raw-topic-link[href*="{title}"]')
