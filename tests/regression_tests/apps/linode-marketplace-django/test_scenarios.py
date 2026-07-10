from playwright.sync_api import expect

from regression_tests.pages.django.django_dashboard_page import DjangoDashboardPage
from regression_tests.pages.django.django_login_page import DjangoLoginPage
from regression_tests.pages.django.django_site_page import DjangoSitePage


def test_django_admin_startup(context, base_url):
    # Verifies that the app started and the admin login page loads successfully.
    login_page = DjangoLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Django admin is not started").to_have_title("Log in | Django site admin")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_django_admin_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Django user"]
    password = app_credentials["Django password"]
    login_page = DjangoLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = DjangoDashboardPage(context)
    expect(dashboard_page.heading, "Credentials are invalid or something went wrong.").to_be_visible()


def test_django_view_site(context, base_url, app_credentials):
    # Verifies that "View site" from the admin dashboard loads the public site.
    username = app_credentials["Django user"]
    password = app_credentials["Django password"]
    login_page = DjangoLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = DjangoDashboardPage(context)
    dashboard_page.view_site()
    site_page = DjangoSitePage(context)
    expect(site_page.heading, "Public site did not load after clicking View site.").to_be_visible()
