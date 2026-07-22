from playwright.sync_api import expect

from regression_tests.pages.passbolt.passbolt_login_page import PassboltLoginPage


def test_passbolt_startup(context, base_url):
    # Verifies that Passbolt started and the login page loads successfully.
    login_page = PassboltLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Passbolt is not started").to_have_title(
        "Passbolt | Open source password manager for teams"
    )
    expect(login_page.username_input, "Login email field did not render.").to_be_visible(timeout=30000)
