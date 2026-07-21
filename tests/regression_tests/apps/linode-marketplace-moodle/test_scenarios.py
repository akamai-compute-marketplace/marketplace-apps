import urllib.parse

from playwright.sync_api import expect

from regression_tests.pages.moodle.moodle_login_page import MoodleLoginPage
from regression_tests.pages.moodle.moodle_dashboard_page import MoodleDashboardPage
from regression_tests.pages.moodle.moodle_create_course_page import MoodleCreateCoursePage
from regression_tests.pages.moodle.moodle_course_page import MoodleCoursePage
from regression_tests.pages.moodle.moodle_course_management_page import MoodleCourseManagementPage


def test_moodle_startup(context, base_url):
    # Verifies that Moodle started and the login page loads successfully.
    login_page = MoodleLoginPage(context)
    login_page.navigate(f"{base_url}/login/index.php")
    expect(context, "Moodle is not started").to_have_title("Log in to the site | moodle")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_moodle_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in to Moodle with the provided credentials.
    username = app_credentials["Moodle Admin Username"]
    password = app_credentials["Moodle Admin Password"]
    login_page = MoodleLoginPage(context)
    login_page.navigate(f"{base_url}/login/index.php")
    login_page.login(username, password)
    dashboard_page = MoodleDashboardPage(context)
    expect(dashboard_page.dashboard_heading, "Credentials are invalid or something went wrong").to_be_visible()


def test_moodle_create_course(context, base_url, app_credentials):
    # Verifies that the admin user can create a new course and it appears in course management.
    username = app_credentials["Moodle Admin Username"]
    password = app_credentials["Moodle Admin Password"]
    course_fullname = "QA Regression Test Course"
    course_shortname = "qa-regression-course"

    login_page = MoodleLoginPage(context)
    login_page.navigate(f"{base_url}/login/index.php")
    login_page.login(username, password)

    create_course_page = MoodleCreateCoursePage(context)
    create_course_page.navigate(f"{base_url}/course/edit.php?category=1")
    create_course_page.create_course(course_fullname, course_shortname)

    course_page = MoodleCoursePage(context, course_fullname)
    expect(course_page.course_heading, "Failed to create a new course.").to_be_visible()

    management_page = MoodleCourseManagementPage(context, course_fullname)
    management_page.navigate(
        f"{base_url}/course/management.php?search={urllib.parse.quote(course_fullname)}"
    )
    expect(management_page.course_link, "New course does not appear in course management listing.").to_be_visible()
