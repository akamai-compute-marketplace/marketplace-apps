from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class AaPanelLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_input = self.page.get_by_placeholder("Account", exact=True)
        self.password_input = self.page.get_by_placeholder("Password", exact=True)
        self.login_button = self.page.get_by_role("button", name="Login", exact=True)

    def login(self, username: str, password: str):
        self.account_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def complete_first_login_setup(self):
        """Complete aaPanel's one-time post-login dialogs without installing software."""
        installation_dialog = self.page.get_by_role("dialog").filter(
            has_text="The installation was successful"
        ).first
        if installation_dialog.is_visible():
            installation_dialog.get_by_role("button", name="Finish", exact=True).click()

        software_dialog = self.page.get_by_role("dialog").filter(
            has_text="Project creation"
        ).first
        if software_dialog.is_visible():
            software_dialog.get_by_role("button", name="Skip", exact=True).click()
