from playwright.sync_api import expect
from regression_tests.pages.neo4j.neo4j_tech_docs_page import Neo4jTechDocsPage


def test_neo4j_tech_docs(context, techdocs_url):
    """Verify that the Neo4j tech docs page is accessible."""
    tech_docs_page = Neo4jTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Neo4j tech docs page did not load.").to_have_title("Neo4j")
    expect(tech_docs_page.neo4j_header, "Neo4j tech docs header did not render.").to_be_visible()
