from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def open_new_tab(self) -> Page:
        new_tab = self.page.context.new_page()
        return new_tab
