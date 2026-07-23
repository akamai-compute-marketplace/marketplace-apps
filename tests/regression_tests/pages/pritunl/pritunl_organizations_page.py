from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PritunlOrganizationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_organization_button = self.page.locator(".orgs-add-org")
        self.organization_name_input = self.page.locator("input.form-control[placeholder='Enter name']")
        self.add_button = self.page.locator(".modal.fade .modal-footer .ok")
        self.success_alert = self.page.locator(".alert-dismissable").filter(has_text="Successfully added organization.")

    def create_organization(self, name: str):
        self.add_organization_button.click()
        self.organization_name_input.fill(name)
        self.add_button.click()
