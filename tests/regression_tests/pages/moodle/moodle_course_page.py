from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class MoodleCoursePage(BasePage):
    def __init__(self, page: Page, course_fullname: str):
        super().__init__(page)
        self.course_heading = self.page.get_by_role("heading", name=course_fullname, level=1, exact=True)
