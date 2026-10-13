import uuid

from playwright.sync_api import expect

from regression_tests.pages.milvus.milvus_login_page import MilvusLoginPage
from regression_tests.pages.milvus.milvus_browser_page import MilvusBrowserPage
from regression_tests.pages.milvus.milvus_tech_docs_page import MilvusTechDocsPage


def test_milvus_startup(context, base_url):
    # Verifies the app started and the MinIO Console login page loads.
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "RustFS is not started").to_have_title("RustFS")
    expect(login_page.account_input, "Account input did not render.").to_be_visible()
    expect(login_page.key_input, "Key input did not render.").to_be_visible()


def test_milvus_rustfs_login(context, base_url, app_credentials):
    # Verifies admin login and acknowledges the first-run license dialog.
    username = app_credentials["RustFS Username"]
    password = app_credentials["RustFS Password"]
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    browser_page = MilvusBrowserPage(context)
    expect(browser_page.create_bucket_button, "Create Bucket button not visible — login may have failed.").to_be_visible()


def test_milvus_create_bucket(context, base_url, app_credentials):
    # Verifies a new bucket can be created and its heading appears in the main area.
    username = app_credentials["RustFS Username"]
    password = app_credentials["RustFS Password"]
    bucket_name = f"test-bucket-{uuid.uuid4().hex[:8]}"
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    browser_page = MilvusBrowserPage(context, bucket_name)
    browser_page.create_bucket()
    expect(
        browser_page.bucket_name_label,
        f"Bucket '{bucket_name}' heading not visible — bucket creation may have failed.",
    ).to_be_visible()


def test_milvus_tech_docs(context, techdocs_url):
    """Verify that the Milvus tech docs page is accessible."""
    tech_docs_page = MilvusTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Milvus tech docs page did not load.").to_have_title("Milvus")
    expect(tech_docs_page.milvus_header, "Milvus tech docs header did not render.").to_be_visible()
