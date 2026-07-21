from playwright.sync_api import expect

from regression_tests.pages.nodejs.nodejs_home_page import NodejsHomePage


def test_nodejs_startup(context, base_url):
    # Verifies that the Node.js app started and serves its default response.
    home_page = NodejsHomePage(context)
    home_page.navigate(base_url)
    expect(
        home_page.app_text,
        "Node.js app did not render its expected startup response.",
    ).to_contain_text("NodeJS App - Powered by Akamai Cloud Compute Marketplace")
