import pytest
import os
import base64
from pytest_html import extras as pytest_html_extras
from playwright.sync_api import sync_playwright
from regression_tests.utils.ssh import get_credentials_via_ssh
from pathlib import Path


@pytest.fixture(scope="session")
def ssh_credentials() -> tuple[str, str, str]:
    """
    Validates and returns SSH credentials from environment variables.

    Returns:
        tuple[str, str, str]: A (host, username, password) tuple.
    """

    linode_ipv4 = os.environ.get("LINODE_IPV4")
    linode_root_user = os.environ.get("LINODE_ROOT_USER", "root")
    linode_root_pass = os.environ.get("LINODE_ROOT_PASS")

    if not linode_ipv4:
        raise ValueError("LINODE_IPV4 env var is required")
    if not linode_root_pass:
        raise ValueError("LINODE_ROOT_PASS env var is required")
    return linode_ipv4, linode_root_user, linode_root_pass


@pytest.fixture(scope="session")
def app_credentials(ssh_credentials, credentials_file_path) -> dict:
    """
    Retrieves application credentials from a remote Linode server via SSH.

    Args:
        ssh_credentials: host, username, password.
        credentials_file_path: Absolute path to the credentials file on the remote server.

    Returns:
        dict: A dictionary mapping credential keys to their respective values.
    """
    print("Retrieving application credentials from remote server...")
    host, username, password = ssh_credentials
    return get_credentials_via_ssh(
        host=host,
        username=username,
        password=password,
        remote_path=credentials_file_path
    )


@pytest.fixture(scope="session")
def browser():
    """
    Launches a shared Chromium browser instance for the entire test session.

    Yields:
        playwright.sync_api.Browser: A Chromium browser instance.
    """
    print("Launching browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
            ])
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """
    Creates a new browser context and page for each test, then closes them on teardown.

    Args:
        browser: The shared Chromium browser instance.

    Yields:
        playwright.sync_api.Page: A fresh page object scoped to the individual test.
    """
    print("Creating new browser context...")
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures a screenshot on test failure and embeds it into the HTML report.

    Args:
        item: The test case being executed.
        call: The result of the test execution phase.
    """

    reports_dir = Path(os.environ.get("REGRESSION_REPORTS_DIR", "reports"))
    screenshots_dir = reports_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page") or item.funcargs.get("context")
    if not page:
        return

    try:
        safe_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
        screenshot_path = screenshots_dir / f"{safe_name}.png"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_path), full_page=True)
        with open(screenshot_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        extras = getattr(report, "extras", [])
        html_content = (
            f'<div>'
            f'<p><strong>Failure Screenshot:</strong></p>'
            f'<img src="data:image/png;base64,{encoded_image}" alt="failure_screenshot" '
            f'style="width:600px; max-width:100%; border:1px solid #ddd; border-radius:4px;">'
            f'</div>'
        )
        extras.append(pytest_html_extras.html(html_content))
        report.extras = extras
    except Exception as e:
        print(f"\n[Hook Error] Failed to capture screenshot for {item.nodeid}: {e}")
