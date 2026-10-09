import random
from playwright.sync_api import expect
from regression_tests.pages.secure_your_server.secure_your_server_tech_docs_page import SecureYourServerTechDocsPage
from regression_tests.services.secure_your_server.secure_your_server_service import SecureYourServerService

BLOCKED_PORT = 8080


def test_secure_your_server_firewall_blocks_unlisted_port(remote_exec, ssh_credentials):
    # Verifies that the firewall drops traffic to a port it does not allow, while SSH stays reachable.
    host, _, _ = ssh_credentials
    service = SecureYourServerService(remote_exec, host)

    service.start_listener(BLOCKED_PORT)
    assert service.listener_bound(BLOCKED_PORT), (
        f"test listener never bound to port {BLOCKED_PORT}; the block below would prove nothing"
    )

    blocked_reachable, blocked_error = service.tcp_connect(BLOCKED_PORT)
    ssh_reachable, ssh_error = service.tcp_connect(SecureYourServerService.SSH_PORT)
    service.stop_listener()

    assert ssh_reachable, f"SSH port is not reachable from the test runner: {ssh_error}"
    assert not blocked_reachable, (
        f"port {BLOCKED_PORT} is reachable from outside; the firewall is not blocking it"
    )


def test_secure_your_server_fail2ban_bans_and_unbans_ip(remote_exec, ssh_credentials):
    # Verifies that the sshd jail applies a ban to the live firewall and lifts it again.
    host, _, _ = ssh_credentials
    service = SecureYourServerService(remote_exec, host)
    banned_ip = f"203.0.113.{random.randint(2, 254)}"

    service.ban_ip(banned_ip)
    jail_after_ban = service.jail_banned_ips()
    firewall_after_ban = service.nft_ban_set()
    service.unban_ip(banned_ip)
    jail_after_unban = service.jail_banned_ips()

    assert banned_ip in jail_after_ban, f"{banned_ip} missing from the jail ban list: {jail_after_ban}"
    assert banned_ip in firewall_after_ban, (
        f"{banned_ip} was not applied to the nftables ban set: {firewall_after_ban}"
    )
    assert banned_ip not in jail_after_unban, (
        f"{banned_ip} still banned after unban: {jail_after_unban}"
    )


def test_secure_your_server_sudo_user_password_authenticates(
    remote_exec, ssh_credentials, app_credentials
):
    # Verifies that the generated password in the credentials file logs the sudo user in over SSH.
    host, _, _ = ssh_credentials
    service = SecureYourServerService(remote_exec, host)
    username = app_credentials["Sudo Username"]

    out, err, code = service.ssh_password_auth(
        username, app_credentials["Sudo Password"], "id -un"
    )

    assert code == 0, f"command failed as {username} (exit {code}): {err or out}"
    assert out == username, f"expected to be logged in as {username}, got: {out}"


def test_secure_your_server_sudo_user_has_root_privilege(
    remote_exec, ssh_credentials, app_credentials
):
    # Verifies that the sudo user can actually escalate to root with its own password.
    host, _, _ = ssh_credentials
    service = SecureYourServerService(remote_exec, host)

    out, err, code = service.sudo_command(
        app_credentials["Sudo Username"], app_credentials["Sudo Password"], "id -un"
    )

    assert code == 0, f"sudo failed (exit {code}): {err or out}"
    assert out == "root", f"expected sudo to run as root, got: {out}"


def test_secure_your_server_tech_docs(context, techdocs_url):
    """Verify that the Secure Your Server tech docs page is accessible."""
    tech_docs_page = SecureYourServerTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Secure Your Server tech docs page title is incorrect.").to_have_title("Secure Your Server")
    expect(tech_docs_page.secure_your_server_header, "Secure Your Server tech docs header did not render.").to_be_visible()
