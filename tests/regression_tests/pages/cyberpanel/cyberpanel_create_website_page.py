from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class CyberPanelCreateWebsitePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.package_select = self.page.locator("select[ng-model='packageForWebsite']")
        self.owner_select = self.page.locator("select[ng-model='websiteOwner']")
        self.domain_input = self.page.locator("input[name='dom']")
        self.email_input = self.page.locator("input[name='email']")
        self.php_select = self.page.locator("select[ng-model='phpSelection']")
        self.create_button = self.page.get_by_role("button", name="Create Website")
        self.success_alert = self.page.locator(".alert.alert-success")

    def create_website(self, domain: str, email: str, package: str = "Default", owner: str = "admin", php_version: str = "PHP 8.1"):
        self.package_select.select_option(package)
        self.owner_select.select_option(owner)
        self.domain_input.fill(domain)
        self.email_input.fill(email)
        self.php_select.select_option(php_version)
        self.create_button.click()
