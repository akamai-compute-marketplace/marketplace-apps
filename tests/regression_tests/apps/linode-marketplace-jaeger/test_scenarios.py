from playwright.sync_api import expect

from regression_tests.pages.jaeger.jaeger_home_page import JaegerHomePage


def test_jaeger_startup_and_login(context, base_url):
    # Verifies the app is running and accessible with valid HTTP Basic Auth credentials.
    home_page = JaegerHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Jaeger UI is not started").to_have_title("Jaeger UI")
    expect(home_page.search_nav_link, "Jaeger UI did not load after authentication.").to_be_visible()
