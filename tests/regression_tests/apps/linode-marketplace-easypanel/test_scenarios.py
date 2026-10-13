from uuid import uuid4

from playwright.sync_api import expect

from regression_tests.pages.easypanel.easypanel_home_page import EasypanelHomePage
from regression_tests.pages.easypanel.easypanel_login_page import EasypanelLoginPage
from regression_tests.pages.easypanel.easypanel_project_page import EasypanelProjectPage
from regression_tests.pages.easypanel.easypanel_tech_docs_page import EasypanelTechDocsPage


def test_easypanel_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = EasypanelLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Easypanel is not started").to_have_title("Easypanel")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_easypanel_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Easypanel Admin Email"]
    password = app_credentials["Easypanel Admin Password"]
    login_page = EasypanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = EasypanelHomePage(context)
    expect(home_page.create_project_button, "Credentials are invalid or something went wrong.").to_be_visible()


def test_easypanel_create_project(context, base_url, app_credentials):
    # Verifies that an admin can create a Project and see it published on the dashboard.
    username = app_credentials["Easypanel Admin Email"]
    password = app_credentials["Easypanel Admin Password"]
    random_suffix = uuid4().hex[:8]
    project_name = f"test-project-{random_suffix}"
    service_name = f"test-service-{random_suffix}"
    login_page = EasypanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = EasypanelHomePage(context)
    home_page.create_project(project_name)
    project_page = EasypanelProjectPage(context)
    project_page.create_service(service_name)
    home_page.navigate(base_url)
    expect(home_page.get_project_label(project_name), "Project was not created successfully.").to_be_visible()
    expect(home_page.get_service_label(service_name), "Service was not created successfully.").to_be_visible()


def test_easypanel_tech_docs(context, techdocs_url):
    """Verify that the Easypanel tech docs page is accessible."""
    tech_docs_page = EasypanelTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Easypanel tech docs page did not load.").to_have_title("Easypanel")
    expect(tech_docs_page.easypanel_header, "Easypanel tech docs header did not render.").to_be_visible()
