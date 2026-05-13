from playwright.sync_api import expect

from regression_tests.pages.appwrite.appwrite_login_page import AppwriteLoginPage
from regression_tests.pages.appwrite.appwrite_organization_page import AppwriteOrganizationPage


def test_appwrite_startup(context, base_url):
    # Verifies that the Appwrite started and login page loads successfully.
    login_page = AppwriteLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Appwrite is not started").to_have_title("Sign in - Appwrite")
    expect(login_page.email_input, "The email input field did not render on the screen.").to_be_visible()


def test_appwrite_login(context, base_url, app_credentials):
    # Verifies that user can loging to Appwrite with provided credentials.
    email = app_credentials["Appwrite Admin Email"]
    password = app_credentials["Appwrite Admin Password"]
    login_page = AppwriteLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    org_page = AppwriteOrganizationPage(context)
    org_page.open_profile_tooltip()
    expect(org_page.profile_tooltip, "Credentials are invalid or something went wrong").to_contain_text(email)


def test_appwrite_create_project(context, base_url, app_credentials):
    # Verifies that user can create a new project in Appwrite.
    email = app_credentials["Appwrite Admin Email"]
    password = app_credentials["Appwrite Admin Password"]
    login_page = AppwriteLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    org_page = AppwriteOrganizationPage(context)
    project_name = "Test Project"
    org_page.create_project(project_name)
    expect(org_page.menu_bar, "Project was not created successfully.").to_contain_text(project_name, timeout=15000)
