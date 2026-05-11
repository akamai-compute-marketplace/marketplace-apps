from playwright.sync_api import Page
from regression_tests.pages.hashicorp_nomad.nomad_base_page import NomadBasePage


class NomadProfilePage(NomadBasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.secret_id_field = self.page.locator("#token-input")
        self.sign_in_button = self.page.get_by_role("button", name="Sign in with secret")
        self.auth_success_message = self.page.get_by_text("Token Authenticated!")

    def sign_in_with_secret(self, secret_id: str):
        self.secret_id_field.fill(secret_id)
        self.sign_in_button.click()
