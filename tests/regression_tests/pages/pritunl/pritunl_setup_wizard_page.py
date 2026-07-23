from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PritunlSetupWizardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.modal_title = self.page.locator(".modal.fade .modal-title")
        self.save_button = self.page.locator(".modal.fade .modal-footer .ok")
        self.success_alert = self.page.locator(".alert-dismissable").filter(has_text="Successfully saved settings.")

    def complete_setup(self):
        self.save_button.click()
