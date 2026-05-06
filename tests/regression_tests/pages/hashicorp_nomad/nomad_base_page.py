from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NomadBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.profile_button = self.page.get_by_role("button", name="Anonymous Token")
        self.sign_out_button = self.page.get_by_role("button", name="Sign Out")
        self.profile_and_sign_in_button = self.page.get_by_role("link", name="Profile and Sign In")
        self.jobs_link = self.page.get_by_role("link", name="Jobs")


    def sign_out(self):
        self.profile_button.click()
        self.sign_out_button.click()

    def go_to_profile_page(self):
        self.profile_and_sign_in_button.click()

    def go_to_jobs_page(self):
        self.jobs_link.click()
