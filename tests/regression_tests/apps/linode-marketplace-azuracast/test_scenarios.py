from playwright.sync_api import expect

from regression_tests.pages.azuracast.azuracast_login_page import AzuracastLoginPage
from regression_tests.pages.azuracast.azuracast_setup_page import AzuracastSetupPage


def test_azuracast_startup(context, base_url):
    # Verifies that AzuraCast started and the login page loads successfully.
    login_page = AzuracastLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "AzuraCast is not started — login page title mismatch.").to_have_title(
        "Log In - AzuraCast"
    )
    expect(login_page.email_input, "Email input field did not render on the login page.").to_be_visible()


def test_azuracast_login(context, base_url, app_credentials):
    # Verifies that on first run after deployment, login redirects to the setup wizard.
    email = app_credentials["Azuracast Admin Email"]
    password = app_credentials["Azuracast Admin Password"]
    login_page = AzuracastLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    setup_page = AzuracastSetupPage(context)
    expect(context, "Setup wizard did not appear after login on fresh deployment.").to_have_title(
        "Create a New Radio Station - AzuraCast"
    )
    expect(
        setup_page.station_name_input, "Station name input not visible on setup wizard."
    ).to_be_visible()


def test_azuracast_radio_station_creation(context, base_url, app_credentials):
    # Verifies that a radio station can be created through the setup wizard on first deployment.
    email = app_credentials["Azuracast Admin Email"]
    password = app_credentials["Azuracast Admin Password"]
    station = "Regression test station"
    login_page = AzuracastLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)

    setup_page = AzuracastSetupPage(context)
    setup_page.create_station(station)
    expect(context, "System Settings page did not load after creating station.").to_have_title(
        "System Settings - AzuraCast"
    )
    setup_page.save_settings(base_url)
    expect(context, "Dashboard did not load after completing setup wizard.").to_have_title(
        "Dashboard - AzuraCast", timeout=15000
    )
    expect(
        context.get_by_role("cell", name=station, exact=False),
        f"Station '{station}' was not found in the dashboard after wizard completion.",
    ).to_be_visible()
