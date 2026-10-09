from playwright.sync_api import expect
from regression_tests.pages.simplex_chat.simplex_chat_tech_docs_page import SimplexChatTechDocsPage
from regression_tests.services.simplex_chat.simplex_chat_service import SimplexChatService


def test_simplex_containers_running(remote_exec, ssh_credentials):
    # Verifies that both server containers are running.
    host, _, _ = ssh_credentials
    service = SimplexChatService(remote_exec, host)

    smp = service.container_status(SimplexChatService.SMP_CONTAINER)
    xftp = service.container_status(SimplexChatService.XFTP_CONTAINER)

    assert smp == "running", f"smp-server container is not running: {smp}"
    assert xftp == "running", f"xftp-server container is not running: {xftp}"


def test_simplex_server_advertises_its_fingerprint(remote_exec, ssh_credentials):
    # Verifies that the server initialized and serves the identity stored on disk.
    host, _, _ = ssh_credentials
    service = SimplexChatService(remote_exec, host)

    fingerprint = service.fingerprint()
    address = service.advertised_address()

    assert fingerprint, "no fingerprint was generated; clients would have no address to connect to"
    assert fingerprint in address, (
        f"running server does not advertise the stored fingerprint: {address!r}"
    )


def test_simplex_ports_reachable(remote_exec, ssh_credentials):
    # Verifies that both server ports accept connections from outside the VM.
    host, _, _ = ssh_credentials
    service = SimplexChatService(remote_exec, host)

    smp_up, smp_error = service.tcp_connect(SimplexChatService.SMP_PORT)
    xftp_up, xftp_error = service.tcp_connect(SimplexChatService.XFTP_PORT)

    assert smp_up, f"SMP port {SimplexChatService.SMP_PORT} is not reachable: {smp_error}"
    assert xftp_up, f"XFTP port {SimplexChatService.XFTP_PORT} is not reachable: {xftp_error}"


def test_simplex_chat_tech_docs(context, techdocs_url):
    """Verify that the SimpleX Chat tech docs page is accessible."""
    tech_docs_page = SimplexChatTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "SimpleX Chat tech docs page title is incorrect.").to_have_title("SimpleX Chat")
    expect(tech_docs_page.simplex_chat_header, "SimpleX Chat tech docs header did not render.").to_be_visible()
