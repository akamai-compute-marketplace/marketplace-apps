from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PleskSetupWizardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = self.page.locator("#contactInfo-email")
        self.new_admin_password_input = self.page.locator("#password-password")
        self.trial_license_label = self.page.locator("label[for='license-licenseType-trial']")
        self.eula_agreement_checkbox_span = self.page.locator("#eula-eulaAgreement + span")
        self.enter_plesk_button = self.page.get_by_role("button", name="Enter Plesk")

    def complete_setup_with_trial_license(self, email: str, new_admin_password: str):
        self.email_input.fill(email)
        self.new_admin_password_input.fill(new_admin_password)
        self.trial_license_label.click()
        self.eula_agreement_checkbox_span.click()
        self.enter_plesk_button.click()

