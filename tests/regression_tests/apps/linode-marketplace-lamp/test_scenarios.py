from playwright.sync_api import expect

from regression_tests.pages.lamp.lamp_home_page import LampHomePage


def test_lamp_startup(context, base_url):
    # Verifies the app started and the LAMP Stack landing page is served by Apache.
    home_page = LampHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LAMP Stack is not started: page title not found.").to_have_title(
        "LAMP Stack - Powered by Akamai Cloud Compute Marketplace"
    )
    expect(home_page.heading, "LAMP Stack heading did not render.").to_be_visible()
    expect(home_page.what_is_lamp_heading, "What is LAMP? heading did not render.").to_be_visible()
