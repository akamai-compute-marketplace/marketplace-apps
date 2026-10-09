from playwright.sync_api import expect
from regression_tests.pages.nextcloud.nextcloud_aio_login_page import NextcloudAioLoginPage
from regression_tests.pages.nextcloud.nextcloud_aio_containers_page import NextcloudAioContainersPage
from regression_tests.pages.nextcloud.nextcloud_tech_docs_page import NextcloudTechDocsPage


def test_nextcloud_startup(aio_passphrase):
    # Verifies that Nextcloud AIO started and a setup passphrase was captured.
    assert aio_passphrase, "Nextcloud AIO did not expose a setup passphrase on first visit."


def test_nextcloud_login(context, base_url, aio_passphrase):
    # Verifies that logging in to the AIO interface with the captured passphrase works.
    login_page = NextcloudAioLoginPage(context)
    login_page.navigate(f"{base_url}/login")
    login_page.login(aio_passphrase)

    containers_page = NextcloudAioContainersPage(context)
    expect(
        containers_page.submit_domain_button,
        "Login with the captured passphrase failed — domain submission form did not render.",
    ).to_be_visible()


def test_nextcloud_tech_docs(context, techdocs_url):
    """Verify that the Nextcloud tech docs page is accessible."""
    tech_docs_page = NextcloudTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Nextcloud tech docs page did not load.").to_have_title("Nextcloud")
    expect(tech_docs_page.nextcloud_header, "Nextcloud tech docs header did not render.").to_be_visible()
