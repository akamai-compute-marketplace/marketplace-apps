from playwright.sync_api import expect

from regression_tests.pages.flask.flask_home_page import FlaskHomePage
from regression_tests.pages.flask.flask_tech_docs_page import FlaskTechDocsPage


def test_flask_startup(context, base_url):
    # Verifies that the app started and the home page loads successfully.
    home_page = FlaskHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Flask app is not started").to_have_title("Flask Sample App")
    expect(home_page.heading, "Home page did not render.").to_be_visible()


def test_flask_tech_docs(context, techdocs_url):
    """Verify that the Flask tech docs page is accessible."""
    tech_docs_page = FlaskTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Flask tech docs page did not load.").to_have_title("Flask")
    expect(tech_docs_page.flask_header, "Flask tech docs header did not render.").to_be_visible()
