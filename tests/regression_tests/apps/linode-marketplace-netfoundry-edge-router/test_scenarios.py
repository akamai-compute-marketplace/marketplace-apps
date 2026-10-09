from playwright.sync_api import expect
from regression_tests.pages.netfoundry_edge_router.netfoundry_edge_router_tech_docs_page import NetFoundryEdgeRouterTechDocsPage
from regression_tests.services.netfoundry_edge_router.netfoundry_edge_router_service import (
    NetFoundryEdgeRouterService,
)


def test_netfoundry_registration_tool_runs(remote_exec):
    # Verifies that the router registration entrypoint is installed and executes.
    service = NetFoundryEdgeRouterService(remote_exec)
    out, err, code = service.registration_tool_help()
    assert code == 0, f"router-registration --help failed (exit {code}): {err or out}"
    assert "registration_key" in out, f"unexpected router-registration usage output: {out}"


def test_netfoundry_bootstrap_binaries_installed(remote_exec):
    # Verifies that the NetFoundry bootstrap tools are present and executable.
    service = NetFoundryEdgeRouterService(remote_exec)
    for name in ("router-registration", "zt-upgrade", "vm-support-bundle"):
        mode = service.file_mode(f"{NetFoundryEdgeRouterService.INSTALL_DIR}/{name}")
        assert mode == "755", f"{name} is missing or not executable, mode was {mode!r}"


def test_netfoundry_salt_minion_staged_for_registration(remote_exec):
    # Verifies that salt-minion is installed at the pinned major version but left stopped.
    service = NetFoundryEdgeRouterService(remote_exec)
    version = service.salt_minion_version()
    assert version.startswith("salt-minion 3006."), f"salt-minion is not pinned to 3006: {version}"
    active, enabled = service.unit_state(NetFoundryEdgeRouterService.SALT_UNIT)
    assert active == "inactive", f"salt-minion should be stopped until registration, got {active}"
    assert enabled == "disabled", f"salt-minion should be disabled until registration, got {enabled}"
    assert not service.minion_id_exists(), "/etc/salt/minion_id should be removed before registration"


def test_netfoundry_login_help_installed(remote_exec):
    # Verifies that the NetFoundry login help script is installed for interactive shells.
    service = NetFoundryEdgeRouterService(remote_exec)
    mode = service.file_mode(NetFoundryEdgeRouterService.LOGIN_HELP)
    assert mode == "755", f"nfhelp.sh is missing or not executable, mode was {mode!r}"


def test_netfoundry_firewall_allows_ssh_only(remote_exec):
    # Verifies that UFW is active and opens SSH alone.
    service = NetFoundryEdgeRouterService(remote_exec)
    status = service.ufw_status()
    assert "Status: active" in status, f"ufw is not active: {status}"
    assert "22/tcp" in status, f"ufw does not allow SSH: {status}"
    assert "Default: deny (incoming)" in status, f"ufw does not deny inbound by default: {status}"


def test_netfoundry_exposes_no_service_port(remote_exec):
    # Verifies that an unregistered router binds no listening port beyond SSH and the local resolver.
    service = NetFoundryEdgeRouterService(remote_exec)
    listeners = service.listening_tcp_ports()
    unexpected = [
        line for line in listeners.splitlines()
        if ":22" not in line and ":53" not in line
    ]
    assert not unexpected, f"unexpected listening tcp ports before registration: {unexpected}"


def test_netfoundry_edge_router_tech_docs(context, techdocs_url):
    """Verify that the NetFoundry Edge Router tech docs page is accessible."""
    tech_docs_page = NetFoundryEdgeRouterTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "NetFoundry Edge Router tech docs page did not load.").to_have_title("NetFoundry Edge Router")
    expect(tech_docs_page.netfoundry_edge_router_header, "NetFoundry Edge Router tech docs header did not render.").to_be_visible()
