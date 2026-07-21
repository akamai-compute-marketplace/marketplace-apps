from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class NextcloudAioSetupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.page.get_by_role("heading", name="All-in-one setup", exact=True)
        self.login_link = self.page.get_by_role("link", name="Open Nextcloud AIO login")

    def read_passphrase(self) -> str:
        body_text = self.page.locator("body").inner_text()
        after_label = body_text.split("Passphrase", 1)[1]
        passphrase = after_label.split("Open Nextcloud AIO login", 1)[0]
        return passphrase.strip()
