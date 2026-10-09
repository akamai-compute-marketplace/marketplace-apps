from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class RabbitMQTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.rabbitmq_header = self.page.get_by_role("heading", name="RabbitMQ", level=1, exact=True)
