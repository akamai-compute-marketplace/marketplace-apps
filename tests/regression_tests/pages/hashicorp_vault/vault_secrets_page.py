from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class VaultSecretsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Engine locators
        self.enable_new_engine_button = page.get_by_role("link", name="Enable new engine")
        self.kv_engine_label = page.get_by_label("KV - enabled engine type")
        self.engine_path_input = page.locator('input[name="path"]')
        self.enable_engine_button = page.get_by_role("button", name="Enable engine")

        # Secrets locators
        self.create_secret_button = page.get_by_role("link", name="Create secret")
        self.secret_path_input = page.locator('input[name="path"]')
        self.secret_key_input = page.get_by_role("textbox", name="Key")
        self.secret_value_input = page.locator('textarea.masked-value.masked-font')
        self.secret_add_button = page.get_by_role("button", name="Add")
        self.secret_save_button = page.get_by_role("button", name="Save")

        # Secret details locators
        self.secret_details_link = page.get_by_role("link", name="Secret", exact=True)
        self.secret_unmask_button = page.get_by_role("button", name="show value")
        self.secret_data_row = page.locator('[data-test-component="info-table-row"]')

    def create_new_engine(self, engine_name: str):
        self.enable_new_engine_button.click()
        self.kv_engine_label.click()
        self.engine_path_input.clear()
        self.engine_path_input.fill(engine_name)
        self.enable_engine_button.click()

    def create_new_secret(self, secret_path: str, secret_key: str, secret_value: str):
        self.create_secret_button.click()
        self.secret_path_input.fill(secret_path)
        self.secret_key_input.fill(secret_key)
        self.secret_value_input.fill(secret_value)
        self.secret_add_button.click()
        self.secret_save_button.click()

    def get_secret_data(self):
        self.secret_details_link.click()
        self.secret_unmask_button.click()
