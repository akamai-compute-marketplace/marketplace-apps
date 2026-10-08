from playwright.sync_api import expect

from regression_tests.pages.mean.mean_home_page import MeanHomePage
from regression_tests.pages.mean.mean_tech_docs_page import MeanTechDocsPage


def test_mean_startup(context, base_url):
    # Verifies the app started and the MEAN Stack default Angular app page is served.
    home_page = MeanHomePage(context)
    home_page.navigate(base_url)
    expect(context, "MEAN Stack is not started: page title not found.").to_have_title("Client")
    expect(home_page.hello_heading, "Hello, client heading did not render.").to_be_visible()
    expect(home_page.running_message, "App running message did not render.").to_be_visible()


def test_mean_tech_docs(context, techdocs_url):
    """Verify that the MEAN Stack tech docs page is accessible."""
    tech_docs_page = MeanTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "MEAN Stack tech docs page did not load.").to_have_title("MEAN Stack")
    expect(tech_docs_page.mean_header, "MEAN Stack tech docs header did not render.").to_be_visible()
