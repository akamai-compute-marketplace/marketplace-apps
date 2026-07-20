from playwright.sync_api import expect

from regression_tests.pages.rocketchat.rocketchat_login_page import RocketchatLoginPage


def test_rocketchat_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = RocketchatLoginPage(context)
    login_page.navigate(f"{base_url}/home")
    expect(context, "Rocket.Chat is not started").to_have_title("Rocket.Chat - Login", timeout=30000)
    expect(login_page.username_input, "Login form did not render.").to_be_visible(timeout=30000)


def test_rocketchat_login(context, base_url, app_credentials):
    # Verifies that the admin can authenticate with valid credentials.
    username = app_credentials["Rocket.Chat Admin Username"]
    password = app_credentials["Rocket.Chat Admin Password"]
    login_page = RocketchatLoginPage(context)
    login_page.navigate(f"{base_url}/home")
    expect(login_page.username_input, "Login form did not render.").to_be_visible(timeout=30000)
    login_page.login(username, password)
    expect(login_page.login_button, "Login failed - login form is still visible.").to_be_hidden(timeout=30000)
