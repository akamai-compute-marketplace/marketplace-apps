from playwright.sync_api import Page, expect
from regression_tests.pages.base_page import BasePage


class PritunlServersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_server_button = self.page.locator(".servers-add-server")
        self.attach_organization_button = self.page.locator(".servers-attach-org")
        self.server_name_input = self.page.locator("input.form-control[placeholder='Enter name']")
        self.modal_ok_button = self.page.locator(".modal.fade .modal-footer .ok")
        self.organization_select = self.page.locator(".modal.fade .form-group:has(label:has-text('Select an organization')) select")
        self.server_select = self.page.locator(".modal.fade .form-group:has(label:has-text('Select a server')) select")
        self.dashboard_servers_status = self.page.locator(".servers-status")
        self.server_added_alert = self.page.locator(".alert-dismissable").filter(has_text="Successfully added server.")
        self.organization_attached_alert = self.page.locator(".alert-dismissable").filter(
            has_text="Successfully attached organization."
        )

    def create_server(self, name: str):
        self.add_server_button.click()
        self.server_name_input.fill(name)
        self.modal_ok_button.click()
        expect(self.server_added_alert, "Server was not created successfully.").to_be_visible(timeout=30000)
        self.reload()

    def attach_organization(self, organization_name: str, server_name: str):
        self.attach_organization_button.click()
        self.organization_select.select_option(label=organization_name)
        self.server_select.select_option(label=server_name)
        self.modal_ok_button.click()
        expect(
            self.organization_attached_alert, "Organization was not attached to the server successfully."
        ).to_be_visible(timeout=30000)
        self.reload()

    def server_container(self, server_name: str):
        return self.page.locator("div.server").filter(has_text=server_name)

    def start_server_button(self, server_name: str):
        return self.server_container(server_name).locator(".server-start")

    def server_status(self, server_name: str):
        return self.server_container(server_name).locator(".server-status")

    def start_server(self, server_name: str):
        self.start_server_button(server_name).click()
