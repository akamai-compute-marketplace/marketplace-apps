from playwright.sync_api import expect

from regression_tests.pages.akamai_mcp_client.akamai_mcp_client_tech_docs_page import (
    AkamaiMcpClientTechDocsPage,
)


def test_akamai_mcp_client_tech_docs(context, techdocs_url):
    """Verify that the Akamai MCP tech docs page is accessible."""
    tech_docs_page = AkamaiMcpClientTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Akamai MCP tech docs page did not load.").to_have_title("Akamai MCP")
    expect(tech_docs_page.akamai_mcp_header, "Akamai MCP tech docs header did not render.").to_be_visible()
