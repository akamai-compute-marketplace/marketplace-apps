from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class MoodleCreateCoursePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.fullname_input = self.page.locator("#id_fullname")
        self.shortname_input = self.page.locator("#id_shortname")
        self.save_and_display_button = self.page.locator("#id_saveanddisplay")

    def create_course(self, fullname: str, shortname: str):
        self.fullname_input.fill(fullname)
        self.shortname_input.fill(shortname)
        self.save_and_display_button.click()
