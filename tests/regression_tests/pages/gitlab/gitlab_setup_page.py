from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class GitLabSetupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.skip_link = self.page.get_by_role("link", name="Skip")
        self.skip_profile_button = self.page.get_by_test_id("skip-button")

    def skip_setup_if_present(self):
        if "/admin/registrations/groups/new" not in self.page.url:
            return
        self.skip_link.click()
        self.page.wait_for_url("**/admin/registrations/profile/new")
        self.skip_profile_button.click()
