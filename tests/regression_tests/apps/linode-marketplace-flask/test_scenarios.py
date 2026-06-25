from playwright.sync_api import expect

from regression_tests.pages.flask.flask_home_page import FlaskHomePage


def test_flask_startup(context, base_url):
    # Verifies that the app started and the home page loads successfully.
    home_page = FlaskHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Flask app is not started").to_have_title("Flask Sample App")
    expect(home_page.heading, "Home page did not render.").to_be_visible()
