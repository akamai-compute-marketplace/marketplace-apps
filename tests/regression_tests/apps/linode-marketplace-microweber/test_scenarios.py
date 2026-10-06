import uuid

from playwright.sync_api import expect

from regression_tests.pages.microweber.microweber_dashboard_page import MicroweberDashboardPage
from regression_tests.pages.microweber.microweber_login_page import MicroweberLoginPage
from regression_tests.pages.microweber.microweber_page_editor import MicroweberPageEditor


def test_microweber_startup(context, admin_url):
    """Verify that Microweber started and its admin login page is available."""
    login_page = MicroweberLoginPage(context)
    login_page.navigate(admin_url)

    expect(context, "Microweber login page did not load.").to_have_title("Login")
    expect(login_page.login_button, "Microweber Login button did not render.").to_be_visible()


def test_microweber_login(context, admin_url, app_credentials):
    """Verify that the generated Microweber admin account can log in."""
    login_page = MicroweberLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(
        app_credentials["Microweber Admin Username"],
        app_credentials["Microweber Admin Password"],
    )

    dashboard_page = MicroweberDashboardPage(context)
    expect(dashboard_page.welcome_message,
           "Microweber dashboard did not load after login.").to_be_visible(timeout=30000)


def test_microweber_create_and_open_page(context, base_url, admin_url, app_credentials):
    """Create a page titled like a test and verify its public page opens."""
    page_title = f"test-{uuid.uuid4().hex[:8]}"

    login_page = MicroweberLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(
        app_credentials["Microweber Admin Username"],
        app_credentials["Microweber Admin Password"],
    )

    dashboard_page = MicroweberDashboardPage(context)
    expect(dashboard_page.welcome_message,
        "Microweber dashboard did not load before opening the page editor.",).to_be_visible(timeout=30000)

    dashboard_page.open_new_page()
    editor = MicroweberPageEditor(context)
    editor.create_page(page_title)
    editor.navigate(f"{base_url}/{page_title}")
    expect(context, "The newly created Microweber page did not open.").to_have_title(page_title)
