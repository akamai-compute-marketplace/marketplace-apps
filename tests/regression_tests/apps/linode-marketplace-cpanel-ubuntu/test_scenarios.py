from playwright.sync_api import expect

from regression_tests.pages.cpanel.cpanel_login_page import CpanelLoginPage
from regression_tests.pages.cpanel.cpanel_trial_page import CpanelTrialPage


def test_cpanel_startup(context, base_url):
    """Verifies that WHM started and the login page loads successfully."""
    login_page = CpanelLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "WHM login page did not load — app may not have started.").to_have_title("WHM Login")
    expect(login_page.username_input, "Username input was not visible on the WHM login page.").to_be_visible()
    expect(login_page.password_input, "Password input was not visible on the WHM login page.").to_be_visible()


def test_cpanel_login(context, base_url, app_credentials):
    """Verifies that the root user can log in to WHM with provided credentials."""
    username = app_credentials["username"]
    password = app_credentials["password"]

    login_page = CpanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    # After login on a fresh VM, WHM redirects to the trial-activation setup wizard.
    # Waiting for the 'Log in to cPanel Store' button confirms a successful login and redirect.
    trial_page = CpanelTrialPage(context)
    expect(trial_page.proceed_to_store_button,
           "WHM trial-activation page did not load after login — login may have failed.",
           ).to_be_visible(timeout=30000)
