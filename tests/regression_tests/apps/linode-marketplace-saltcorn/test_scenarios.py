from playwright.sync_api import expect

from regression_tests.pages.saltcorn.saltcorn_create_page_page import SaltcornCreatePagePage
from regression_tests.pages.saltcorn.saltcorn_create_table_page import SaltcornCreateTablePage
from regression_tests.pages.saltcorn.saltcorn_dashboard_page import SaltcornDashboardPage
from regression_tests.pages.saltcorn.saltcorn_login_page import SaltcornLoginPage


def test_saltcorn_startup(context, base_url):
    # Verifies that the Saltcorn is started
    login_page = SaltcornLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Saltcorn is not started").to_have_title("Login")
    expect(login_page.email_input, "Email input field is not rendered").to_be_visible()


def test_saltcorn_login(context, base_url, app_credentials):
    # Verifies that user can log in
    email = app_credentials["Saltcorn Admin Email"]
    password = app_credentials["Saltcorn Admin Password"]
    login_page = SaltcornLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    dashboard_page = SaltcornDashboardPage(context)
    expect(dashboard_page.create_table_button, "Can't login with provided credentials").to_be_visible()


def test_saltcorn_create_table(context, base_url, app_credentials):
    # Verifies that a table is created
    email = app_credentials["Saltcorn Admin Email"]
    password = app_credentials["Saltcorn Admin Password"]
    test_table_name = "test-table"
    login_page = SaltcornLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    dashboard_page = SaltcornDashboardPage(context)
    dashboard_page.navigate_to_create_table()
    create_table_page = SaltcornCreateTablePage(context)
    create_table_page.create_table(test_table_name)
    create_table_page.navigate_to_dashboard()
    expect(dashboard_page.tables_card, "Table can't be created").to_contain_text(test_table_name)


def test_saltcorn_create_page(context, base_url, app_credentials):
    # Verifies that a page is created
    email = app_credentials["Saltcorn Admin Email"]
    password = app_credentials["Saltcorn Admin Password"]
    test_page_name = "test-page"
    login_page = SaltcornLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    dashboard_page = SaltcornDashboardPage(context)
    dashboard_page.navigate_to_create_page()
    create_page_page = SaltcornCreatePagePage(context)
    create_page_page.create_page(test_page_name)
    create_page_page.navigate_to_dashboard()
    expect(dashboard_page.pages_card, "Page can't be created").to_contain_text(test_page_name)
