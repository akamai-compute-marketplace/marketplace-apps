from playwright.sync_api import Page
from regression_tests.pages.base_page import BasePage


class MoodleCourseManagementPage(BasePage):
    def __init__(self, page: Page, course_fullname: str):
        super().__init__(page)
        self.course_link = self.page.get_by_role("link", name=course_fullname, exact=True)
