from playwright.sync_api import expect
from regression_tests.pages.wireguard_client.wireguard_client_tech_docs_page import WireGuardClientTechDocsPage
from regression_tests.services.wireguard_client.wireguard_client_service import WireGuardClientService


def test_wireguard_client_up_and_interface_present(remote_exec):
    # Verifies that the unit is active and the kernel actually brought the interface up.
    service = WireGuardClientService(remote_exec)

    state = service.unit_state()
    enabled = service.unit_enabled()
    public_key = service.interface_public_key()
    flags = service.link_flags()

    assert state == "active", f"{WireGuardClientService.UNIT} is not active: {state}"
    assert enabled == "enabled", (
        f"{WireGuardClientService.UNIT} is not enabled, so the tunnel would not survive a reboot: {enabled}"
    )
    assert public_key, "the kernel reports no public key for wg0; the interface is not configured"
    assert "UP" in flags, f"wg0 is not up: {flags!r}"


def test_wireguard_client_kernel_uses_the_configured_tunnel_address(remote_exec):
    # Verifies that the tunnel address in the config is the one assigned in the kernel.
    service = WireGuardClientService(remote_exec)

    configured = service.config_value("Address")
    assigned = service.interface_address()

    assert configured, "wg0.conf declares no Address"
    assert assigned == configured, (
        f"kernel assigned {assigned!r} to wg0 but the config declares {configured!r}"
    )


def test_wireguard_client_kernel_registers_the_configured_peer(remote_exec):
    # Verifies that the peer from the config is registered in the kernel with its endpoint and routes.
    service = WireGuardClientService(remote_exec)

    configured_key = service.config_value("PublicKey")
    configured_endpoint = service.config_value("Endpoint")
    configured_allowed_ips = service.config_value("AllowedIPs")

    peers = service.peers()
    endpoint = service.peer_endpoint()
    allowed_ips = service.peer_allowed_ips()

    assert configured_key in peers, (
        f"the configured peer is not registered in the kernel; kernel peers: {peers}"
    )
    assert endpoint == configured_endpoint, (
        f"kernel peer endpoint is {endpoint!r} but the config declares {configured_endpoint!r}"
    )
    for route in configured_allowed_ips.split(","):
        assert route in allowed_ips, (
            f"configured allowed-ip {route!r} is not routed to the peer; kernel has {allowed_ips!r}"
        )


def test_wireguard_client_tech_docs(context, techdocs_url):
    """Verify that the WireGuard tech docs page is accessible."""
    tech_docs_page = WireGuardClientTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "WireGuard tech docs page title is incorrect.").to_have_title("WireGuard")
    expect(tech_docs_page.wireguard_client_header, "WireGuard tech docs header did not render.").to_be_visible()
