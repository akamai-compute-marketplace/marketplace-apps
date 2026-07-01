import uuid

from playwright.sync_api import expect

from regression_tests.pages.milvus.milvus_login_page import MilvusLoginPage
from regression_tests.pages.milvus.milvus_browser_page import MilvusBrowserPage


def test_milvus_startup(context, base_url):
    # Verifies the app started and the MinIO Console login page loads.
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "MinIO Console is not started: page title not found.").to_have_title("MinIO Console")
    expect(login_page.username_input, "Username input did not render.").to_be_visible()
    expect(login_page.password_input, "Password input did not render.").to_be_visible()


def test_milvus_minio_login(context, base_url, app_credentials):
    # Verifies admin login and acknowledges the first-run license dialog.
    username = app_credentials["Minio Username"]
    password = app_credentials["Minio Password"]
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    browser_page = MilvusBrowserPage(context)
    expect(browser_page.acknowledge_button, "License acknowledgment dialog did not appear after first login.").to_be_visible()
    browser_page.acknowledge_button.click()
    expect(browser_page.create_bucket_button, "Create Bucket button not visible — login may have failed.").to_be_visible()


def test_milvus_create_bucket(context, base_url, app_credentials):
    # Verifies a new bucket can be created and its heading appears in the main area.
    username = app_credentials["Minio Username"]
    password = app_credentials["Minio Password"]
    login_page = MilvusLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    browser_page = MilvusBrowserPage(context)
    # License dialog appears on every fresh browser session (session-based, not server-side).
    expect(browser_page.acknowledge_button, "License acknowledgment dialog did not appear.").to_be_visible()
    browser_page.acknowledge_button.click()
    bucket_name = f"test-bucket-{uuid.uuid4().hex[:8]}"
    browser_page.create_bucket(bucket_name)
    expect(
        browser_page.bucket_heading(bucket_name),
        f"Bucket '{bucket_name}' heading not visible — bucket creation may have failed.",
    ).to_be_visible()
