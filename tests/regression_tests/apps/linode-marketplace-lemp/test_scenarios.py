from playwright.sync_api import expect

from regression_tests.pages.lemp.lemp_home_page import LempHomePage


def test_lemp_startup(context, base_url):
    # Verifies the app started and the LEMP Stack landing page is served by Nginx.
    home_page = LempHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LEMP Stack is not started: page title not found.").to_have_title(
        "LEMP Stack - Powered by Akamai Cloud Compute Marketplace"
    )
    expect(home_page.heading, "LEMP Stack heading did not render.").to_be_visible()
    expect(home_page.what_is_lemp_heading, "What is LEMP? heading did not render.").to_be_visible()
