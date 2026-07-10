from playwright.sync_api import expect

from regression_tests.pages.guacamole.guacamole_login_page import GuacamoleLoginPage
from regression_tests.pages.guacamole.guacamole_home_page import GuacamoleHomePage


def test_guacamole_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = GuacamoleLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Guacamole is not started").to_have_title("Apache Guacamole")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_guacamole_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Guacamole Admin Username"]
    password = app_credentials["Guacamole Admin Password"]
    login_page = GuacamoleLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = GuacamoleHomePage(context)
    expect(home_page.recent_connections_heading, "Dashboard did not load after login.").to_be_visible()
