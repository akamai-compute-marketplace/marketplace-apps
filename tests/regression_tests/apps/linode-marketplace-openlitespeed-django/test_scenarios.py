from playwright.sync_api import expect

from regression_tests.pages.openlitespeed_django.openlitespeed_django_dashboard_page import (
    OpenLitespeedDjangoDashboardPage,
)
from regression_tests.pages.openlitespeed_django.openlitespeed_django_login_page import (
    OpenLitespeedDjangoLoginPage,
)
from regression_tests.pages.openlitespeed_django.openlitespeed_django_site_page import (
    OpenLitespeedDjangoSitePage,
)


def test_openlitespeed_django_admin_startup(context, base_url):
    # Verifies that the app started and the admin login page loads successfully.
    login_page = OpenLitespeedDjangoLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Django admin is not started").to_have_title("Log in | Django site admin")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_openlitespeed_django_admin_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Django admin user"]
    password = app_credentials["Django admin password"]
    login_page = OpenLitespeedDjangoLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = OpenLitespeedDjangoDashboardPage(context)
    expect(dashboard_page.heading, "Credentials are invalid or something went wrong.").to_be_visible()


def test_openlitespeed_django_view_site(context, base_url, app_credentials):
    # Verifies that "View site" from the admin dashboard loads the public sample site.
    username = app_credentials["Django admin user"]
    password = app_credentials["Django admin password"]
    login_page = OpenLitespeedDjangoLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = OpenLitespeedDjangoDashboardPage(context)
    dashboard_page.view_site()
    site_page = OpenLitespeedDjangoSitePage(context)
    expect(site_page.hello_world_text, "Public site did not load after clicking View site.").to_be_visible()
