import uuid
from playwright.sync_api import expect
from regression_tests.pages.shadowsocks.shadowsocks_tech_docs_page import ShadowsocksTechDocsPage
from regression_tests.services.shadowsocks.shadowsocks_service import ShadowsocksService

ORIGIN_PORT = 9000
CLIENT_PORT = 1080


def test_shadowsocks_up(remote_exec, ssh_credentials):
    # Verifies that the shadowsocks unit is active and accepts connections on its proxy port.
    host, _, _ = ssh_credentials
    service = ShadowsocksService(remote_exec, host)

    assert service.unit_active() == "active", "shadowsocks-libev unit is not active"
    connected, error = service.tcp_connect(ShadowsocksService.SERVER_PORT)
    assert connected, (
        f"proxy port {ShadowsocksService.SERVER_PORT} did not accept a connection: {error}"
    )


def test_shadowsocks_proxies_traffic_end_to_end(remote_exec, ssh_credentials, app_credentials):
    # Verifies that traffic sent through the SOCKS5 proxy reaches its destination and returns intact.
    host, _, _ = ssh_credentials
    service = ShadowsocksService(remote_exec, host)
    run_id = uuid.uuid4().hex[:8]
    origin_unit, client_unit = f"ss-origin-{run_id}", f"ss-client-{run_id}"
    token = f"shadowsocks-{run_id}"

    service.start_origin_server(origin_unit, ORIGIN_PORT, token)
    service.start_client(client_unit, CLIENT_PORT, app_credentials["Shadowsocks Password"])
    client_state = service.transient_unit_active(client_unit)
    out, err, code = service.fetch_through_proxy(CLIENT_PORT, ORIGIN_PORT)
    service.stop_units(client_unit, origin_unit)

    assert client_state == "active", f"ss-local client did not start: {client_state}"
    assert code == 0, f"fetch through the proxy failed (curl exit {code}): {err or out}"
    assert out == token, f"expected {token} back through the proxy, got: {out!r}"


def test_shadowsocks_tech_docs(context, techdocs_url):
    """Verify that the Shadowsocks tech docs page is accessible."""
    tech_docs_page = ShadowsocksTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Shadowsocks tech docs page title is incorrect.").to_have_title("Shadowsocks")
    expect(tech_docs_page.shadowsocks_header, "Shadowsocks tech docs header did not render.").to_be_visible()
