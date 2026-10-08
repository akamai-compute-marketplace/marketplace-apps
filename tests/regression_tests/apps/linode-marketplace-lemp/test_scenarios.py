from playwright.sync_api import expect

from regression_tests.pages.lemp.lemp_home_page import LempHomePage
from regression_tests.pages.lemp.lemp_tech_docs_page import LempTechDocsPage


def test_lemp_startup(context, base_url):
    # Verifies the app started and the LEMP Stack landing page is served by Nginx.
    home_page = LempHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LEMP Stack is not started: page title not found.").to_have_title(
        "LEMP Stack - Powered by Akamai Cloud Compute Marketplace"
    )
    expect(home_page.heading, "LEMP Stack heading did not render.").to_be_visible()
    expect(home_page.what_is_lemp_heading, "What is LEMP? heading did not render.").to_be_visible()


def test_lemp_tech_docs(context, techdocs_url):
    """Verify that the LEMP Stack tech docs page is accessible."""
    tech_docs_page = LempTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "LEMP Stack tech docs page did not load.").to_have_title("LEMP Stack")
    expect(tech_docs_page.lemp_header, "LEMP Stack tech docs header did not render.").to_be_visible()
