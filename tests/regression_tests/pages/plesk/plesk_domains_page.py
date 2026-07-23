from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class PleskDomainsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.websites_domains_heading = self.page.get_by_role("heading", name="Websites & Domains")
        self.add_domain_link = self.page.locator("#buttonAddDomain")
        self.blank_website_option = self.page.locator(
            "div.pul-item-list__item:has(h4:has-text('Blank website'))"
        )
        self.domain_name_input = self.page.locator("input[placeholder='domain.name']")
        self.add_domain_submit_button = self.page.locator(
            "button.pul-form__additional-button:has-text('Add Domain')"
        )
        self.domain_status = self.page.locator("span.pul-status--success").filter(has_text="Active")

    def create_blank_website_domain(self, domain_name: str):
        self.add_domain_link.click()
        self.blank_website_option.click()
        self.domain_name_input.fill(domain_name)
        self.add_domain_submit_button.click()

    def domain_heading(self, domain_name: str):
        return self.page.get_by_role("heading", name=domain_name, exact=True)

