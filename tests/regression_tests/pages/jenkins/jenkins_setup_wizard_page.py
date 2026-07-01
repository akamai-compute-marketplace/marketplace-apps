from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class JenkinsSetupWizardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.install_suggested_button = self.page.get_by_role("button", name="Install suggested plugins")
        self.skip_admin_button = self.page.get_by_text("Skip and continue as admin")
        self.save_and_finish_button = self.page.get_by_role("button", name="Save and Finish")
        self.jenkins_ready_heading = self.page.get_by_role("heading", name="Jenkins is ready!")
        self.start_using_button = self.page.get_by_role("button", name="Start using Jenkins")
