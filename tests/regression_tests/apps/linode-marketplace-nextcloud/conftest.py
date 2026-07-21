import pytest

from regression_tests.pages.nextcloud.nextcloud_aio_setup_page import NextcloudAioSetupPage


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Nextcloud AIO interface.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Nextcloud AIO interface (port 8443).
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:8443"


@pytest.fixture(scope="session")
def aio_passphrase(browser, base_url) -> str:
    """
    Captures the Nextcloud AIO one-time setup passphrase.

    This page (/setup) only ever renders the plaintext passphrase once per instance —
    after a domain is submitted, revisiting it no longer shows it. Captured exactly once
    per session using a dedicated page from the shared `browser` fixture (not the per-test
    `context` fixture, which is function-scoped and would trigger a second, doomed visit).

    Args:
        browser: The shared, session-scoped Chromium browser instance.
        base_url: The base URL of the Nextcloud AIO interface.

    Returns:
        str: The captured setup passphrase.
    """
    page = browser.new_context(ignore_https_errors=True).new_page()
    setup_page = NextcloudAioSetupPage(page)
    setup_page.navigate(base_url)
    passphrase = setup_page.read_passphrase()
    page.context.close()
    return passphrase
