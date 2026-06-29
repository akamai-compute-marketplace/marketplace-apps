from playwright.sync_api import expect

from regression_tests.pages.grav.grav_login_page import GravLoginPage
from regression_tests.pages.grav.grav_page_editor_page import GravPageEditorPage
from regression_tests.pages.grav.grav_pages_list_page import GravPagesListPage
from regression_tests.pages.grav.grav_published_page import GravPublishedPage


def test_grav_startup(context, admin_url):
    # Verifies that the app started and the admin login page loads successfully.
    login_page = GravLoginPage(context)
    login_page.navigate(admin_url)
    expect(context, "Grav is not started").to_have_title("Grav Admin Login | Grav")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_grav_login(context, admin_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Grav Admin Username"]
    password = app_credentials["Grav Admin Password"]
    login_page = GravLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(username, password)
    expect(context, "Credentials are invalid or something went wrong.").to_have_title("Dashboard | Grav")


def test_grav_create_page(context, base_url, admin_url, app_credentials):
    # Verifies that an admin can create a page and see it rendered on the public site.
    username = app_credentials["Grav Admin Username"]
    password = app_credentials["Grav Admin Password"]
    page_title = "Test Automation Page"
    body_text = "Test Automation Page Body Content"

    login_page = GravLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(username, password)

    pages_list_page = GravPagesListPage(context)
    pages_list_page.navigate(f"{admin_url}/pages")
    pages_list_page.create_page(page_title)

    editor_page = GravPageEditorPage(context)
    editor_page.set_content(body_text)
    editor_page.save()

    published_page = GravPublishedPage(context, body_text=body_text)
    published_page.navigate(f"{base_url}/test-automation-page")
    expect(published_page.body_text, "Created page is not displayed on the public site.").to_be_visible()
