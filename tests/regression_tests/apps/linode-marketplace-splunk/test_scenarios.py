from playwright.sync_api import expect

from regression_tests.pages.splunk.splunk_login_page import SplunkLoginPage
from regression_tests.pages.splunk.splunk_home_page import SplunkHomePage


def test_splunk_startup(context, base_url):
    """Verifies that Splunk started and the login page loads successfully."""
    login_page = SplunkLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Splunk login page did not load.").to_have_title("Login | Splunk")
    expect(login_page.username_input, "Splunk login form did not render.").to_be_visible()
    expect(login_page.password_input, "Splunk login form did not render.").to_be_visible()


def test_splunk_login(context, base_url, app_credentials):
    """Verifies that the admin user can log in to the Splunk web UI."""
    username = app_credentials["splunk user"]
    password = app_credentials["splunk admin password"]
    login_page = SplunkLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = SplunkHomePage(context)
    expect(context, "Splunk home page did not load after login.").to_have_title("Home")
    expect(home_page.welcome_heading, "Welcome heading not visible after login.").to_be_visible()
    expect(home_page.administrator_button, "Administrator nav button not visible after login.").to_be_visible()
