from playwright.sync_api import expect

from regression_tests.pages.odoo.odoo_database_creation_page import OdooDatabaseCreationPage
from regression_tests.pages.odoo.odoo_login_page import OdooLoginPage
from regression_tests.pages.odoo.odoo_apps_page import OdooAppsPage


def test_odoo_startup(context, base_url):
    # Verifies that Odoo started and shows the one-time database creation form.
    creation_page = OdooDatabaseCreationPage(context)
    creation_page.navigate(f"{base_url}/web/database/selector")
    expect(context, "Odoo did not start.").to_have_title("Odoo")
    expect(
        creation_page.create_database_button,
        "Database creation form did not render on first visit.",
    ).to_be_visible()


def test_odoo_create_database(context, base_url, db_test_data):
    # Creates the Odoo database using the fixture's test data. This form only renders
    # once per instance -- once a database exists, it's gone for good on this VM.
    creation_page = OdooDatabaseCreationPage(context)
    creation_page.navigate(f"{base_url}/web/database/selector")
    creation_page.create_database(db_test_data)

    apps_page = OdooAppsPage(context)
    expect(
        apps_page.user_menu_button,
        "Database creation did not finish -- was not redirected into the app.",
    ).to_be_visible(timeout=180000)


def test_odoo_login(context, base_url, db_test_data):
    # Verifies that logging in with the fixture's admin credentials works and lands
    # on the app dashboard (Apps page).
    login_page = OdooLoginPage(context)
    login_page.navigate(f"{base_url}/web/login")
    login_page.login(db_test_data["email"], db_test_data["password"])

    apps_page = OdooAppsPage(context)
    expect(
        apps_page.user_menu_button,
        "Login with the fixture credentials failed -- dashboard did not load.",
    ).to_be_visible()
