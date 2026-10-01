from playwright.sync_api import expect

from regression_tests.pages.akaunting.akaunting_dashboard_page import AkauntingDashboardPage
from regression_tests.pages.akaunting.akaunting_login_page import AkauntingLoginPage


def test_akaunting_startup(context, base_url):
    """Verify that Akaunting started and its login page is available."""

    login_page = AkauntingLoginPage(context)
    login_page.navigate(base_url)

    expect(context, "Akaunting login page did not load.").to_have_title("Login")
    expect(login_page.login_button, "Akaunting Login button did not render.").to_be_visible()


def test_akaunting_login(context, base_url, app_credentials):
    """Verify that the generated Akaunting admin account can log in."""

    login_page = AkauntingLoginPage(context)
    login_page.navigate(f"{base_url}/auth/login")
    login_page.login(
        app_credentials["Akaunting Admin Email"],
        app_credentials["Akaunting Admin Password"],
    )

    dashboard_page = AkauntingDashboardPage(context)
    expect(dashboard_page.dashboard_navigation,
           "Akaunting Dashboard navigation did not appear after login.").to_be_visible(timeout=15000)
    expect(dashboard_page.welcome_heading,
           "Akaunting Welcome heading did not appear after login.").to_be_visible(timeout=15000)
