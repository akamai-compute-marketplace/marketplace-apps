from playwright.sync_api import Page

from regression_tests.pages.base_page import BasePage


class MinecraftTechDocsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.minecraft_header = self.page.get_by_role("heading", name="Minecraft Game Server – Java Edition", level=1, exact=True)
