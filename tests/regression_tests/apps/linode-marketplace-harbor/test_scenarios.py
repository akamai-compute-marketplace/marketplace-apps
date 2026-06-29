from playwright.sync_api import expect

from regression_tests.pages.harbor.harbor_login_page import HarborLoginPage
from regression_tests.pages.harbor.harbor_projects_page import HarborProjectsPage


def test_harbor_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = HarborLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Harbor is not started").to_have_title("Harbor")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_harbor_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Harbor user"]
    password = app_credentials["Harbor admin password"]
    login_page = HarborLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    projects_page = HarborProjectsPage(context)
    expect(projects_page.projects_heading, "Projects page did not load after login.").to_be_visible()


def test_harbor_create_project(context, base_url, app_credentials):
    # Verifies that the admin can create a project and it appears in the projects list.
    username = app_credentials["Harbor user"]
    password = app_credentials["Harbor admin password"]
    project = "test-automation-project"
    login_page = HarborLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    projects_page = HarborProjectsPage(context)
    projects_page.projects_heading.wait_for()
    projects_page.create_project(project)
    expect(projects_page.get_project_link(project), "Created project did not appear in the list.").to_be_visible()
