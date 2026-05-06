from playwright.sync_api import Page
from regression_tests.pages.hashicorp_nomad.nomad_base_page import NomadBasePage


class NomadJobsPage(NomadBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.message_label = self.page.locator(".empty-message-headline")
        self.run_job_button = self.page.get_by_role("link", name="Run Job")
        self.job_definition_editor = self.page.locator(".CodeMirror").first
        self.plan_button = self.page.get_by_role("button", name="Plan")
        self.run_button = self.page.get_by_role("button", name="Run")
        self.job_status_badge = self.page.locator(".boxed-section-head h2 .hds-badge__text")

    def setup_and_run_job(self, json_content: str):
        self.run_job_button.click()
        self.job_definition_editor.click()
        self.page.keyboard.type(json_content)
        self.plan_button.click()
        self.run_button.click()
