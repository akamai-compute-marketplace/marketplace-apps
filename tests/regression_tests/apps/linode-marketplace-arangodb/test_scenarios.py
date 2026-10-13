from playwright.sync_api import expect

from regression_tests.pages.arangodb.arangodb_login_page import ArangoDBLoginPage
from regression_tests.pages.arangodb.arangodb_collections_page import ArangoDBCollectionsPage
from regression_tests.pages.arangodb.arangodb_tech_docs_page import ArangoDBTechDocsPage


def test_arangodb_startup(context, base_url):
    # Verifies that ArangoDB started and the login page loads successfully.
    login_page = ArangoDBLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "ArangoDB is not started").to_have_title("ArangoDB Web Interface")
    expect(login_page.username_input, "Login form did not render on the screen.").to_be_visible()


def test_arangodb_login(context, base_url, app_credentials):
    # Verifies that the root user can log in with the provided credentials.
    username = "root"
    password = app_credentials["ArangoDB Root Password"]
    login_page = ArangoDBLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    expect(login_page.user_bar, "User bar did not appear after login.").to_be_visible()
    expect(login_page.user_bar, "Logged-in user is not root.").to_contain_text("root")


def test_arangodb_create_collection(context, base_url, app_credentials):
    # Verifies that a new collection can be created in ArangoDB.
    username = "root"
    password = app_credentials["ArangoDB Root Password"]
    login_page = ArangoDBLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    collections_page = ArangoDBCollectionsPage(context)
    collections_page.navigate_to_collections()

    collection_name = "test_playwright_collection"
    collections_page.create_collection(collection_name)

    expect(
        collections_page.collections_content,
        "Newly created collection did not appear in the collections list.",
    ).to_contain_text(collection_name, timeout=15000)


def test_arangodb_tech_docs(context, techdocs_url):
    """Verify that the ArangoDB tech docs page is accessible."""
    tech_docs_page = ArangoDBTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "ArangoDB tech docs page did not load.").to_have_title("ArangoDB")
    expect(tech_docs_page.arangodb_header, "ArangoDB tech docs header did not render.").to_be_visible()
