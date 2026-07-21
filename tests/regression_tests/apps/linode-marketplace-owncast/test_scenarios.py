from playwright.sync_api import expect

from regression_tests.pages.owncast.owncast_admin_page import OwncastAdminPage
from regression_tests.pages.owncast.owncast_home_page import OwncastHomePage


def test_owncast_startup(context, base_url):
    # Verifies that the app started and the public homepage loads successfully.
    home_page = OwncastHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Owncast is not started").to_have_title("New Owncast Server")
    expect(home_page.heading, "Homepage did not render.").to_be_visible()


def test_owncast_admin_login(context, base_url):
    # Verifies that the admin panel is reachable using the HTTP Basic Auth credentials
    # supplied via the http_credentials fixture.
    admin_page = OwncastAdminPage(context)
    admin_page.navigate(f"{base_url}/admin")
    expect(context, "Owncast admin did not load").to_have_title("Owncast Admin")
    expect(admin_page.heading, "Credentials are invalid or something went wrong.").to_be_visible()
