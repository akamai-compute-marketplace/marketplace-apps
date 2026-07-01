from playwright.sync_api import expect

from regression_tests.pages.mean.mean_home_page import MeanHomePage


def test_mean_startup(context, base_url):
    # Verifies the app started and the MEAN Stack default Angular app page is served.
    home_page = MeanHomePage(context)
    home_page.navigate(base_url)
    expect(context, "MEAN Stack is not started: page title not found.").to_have_title("Client")
    expect(home_page.hello_heading, "Hello, client heading did not render.").to_be_visible()
    expect(home_page.running_message, "App running message did not render.").to_be_visible()
