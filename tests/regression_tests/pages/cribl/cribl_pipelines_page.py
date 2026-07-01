from playwright.sync_api import Page, Locator
from regression_tests.pages.base_page import BasePage


class CriblPipelinesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_pipeline_button = page.locator("button.ant-btn-primary.ant-dropdown-trigger")
        self.add_pipeline_menu_item = page.get_by_role("menuitem", name="Add Pipeline")
        self.pipeline_id_input = page.locator("[id='root.id']")
        self.save_button = page.locator("button.ant-btn-primary", has_text="Save")

    def navigate_to_pipelines(self, base_url: str):
        self.page.goto(f"{base_url}/stream/pipelines")

    def create_pipeline(self, name: str):
        self.add_pipeline_button.click()
        self.add_pipeline_menu_item.click()
        self.pipeline_id_input.fill(name)
        self.save_button.click()

    def pipeline_link(self, name: str) -> Locator:
        return self.page.locator(f"a[href='/stream/pipelines/{name}']")
