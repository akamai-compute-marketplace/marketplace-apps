from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class OdooDatabaseCreationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.database_name_input = self.page.get_by_role("textbox", name="Database Name Database Name")
        self.email_input = self.page.get_by_role("textbox", name="Email Email")
        self.password_input = self.page.get_by_role("textbox", name="Password Password")
        self.phone_input = self.page.get_by_role("textbox", name="Phone Number Phone Number")
        self.language_select = self.page.get_by_label("Language", exact=True)
        self.country_select = self.page.get_by_label("Country", exact=True)
        self.demo_data_checkbox = self.page.get_by_role("checkbox", name="Demo Data Demo Data")
        self.create_database_button = self.page.get_by_role("button", name="Create database", exact=True)

    def create_database(self, test_data: dict):
        self.database_name_input.fill(test_data["database_name"])
        self.email_input.fill(test_data["email"])
        self.password_input.fill(test_data["password"])
        if test_data.get("phone"):
            self.phone_input.fill(test_data["phone"])
        if test_data.get("language"):
            self.language_select.select_option(label=test_data["language"])
        if test_data.get("country"):
            self.country_select.select_option(label=test_data["country"])
        if test_data.get("demo_data"):
            self.demo_data_checkbox.check()
        self.create_database_button.click()
