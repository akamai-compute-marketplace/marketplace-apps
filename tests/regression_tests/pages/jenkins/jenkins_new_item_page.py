from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JenkinsNewItemPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.item_name_input = self.page.get_by_role("textbox", name="Enter an item name")
        # The SVG icon overlaps the radio input, so click the parent item container instead.
        self.freestyle_option = self.page.locator(".jenkins-choice-list__item").filter(has_text="Freestyle project")
        self.ok_button = self.page.get_by_role("button", name="OK")
