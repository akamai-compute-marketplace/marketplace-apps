from playwright.sync_api import expect
from regression_tests.pages.nodejs.nodejs_home_page import NodejsHomePage
from regression_tests.pages.nodejs.nodejs_tech_docs_page import NodejsTechDocsPage


def test_nodejs_startup(context, base_url):
    # Verifies that the Node.js app started and serves its default response.
    home_page = NodejsHomePage(context)
    home_page.navigate(base_url)
    expect(
        home_page.app_text,
        "Node.js app did not render its expected startup response.",
    ).to_contain_text("NodeJS App - Powered by Akamai Cloud Compute Marketplace")


def test_nodejs_tech_docs(context, techdocs_url):
    """Verify that the Node.js tech docs page is accessible."""
    tech_docs_page = NodejsTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Node.js tech docs title did not match.").to_have_title("Node.js")
    expect(tech_docs_page.nodejs_header, "Node.js tech docs header did not render.").to_be_visible()
