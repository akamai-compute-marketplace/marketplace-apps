import uuid
from playwright.sync_api import expect
from regression_tests.pages.valkey.valkey_tech_docs_page import ValkeyTechDocsPage
from regression_tests.services.valkey.valkey_service import ValkeyService

DEFAULT_USER = "default"
DEFAULT_USER_PASSWORD_KEY = 'Valkey "default" User Password'


def test_valkey_up_and_answers_ping(remote_exec, app_credentials):
    # Verifies that the unit is active and the default user can authenticate and get a reply.
    service = ValkeyService(remote_exec)

    state = service.unit_state()
    out, err, code = service.cli(
        DEFAULT_USER, app_credentials[DEFAULT_USER_PASSWORD_KEY], "ping"
    )

    assert state == "active", f"valkey unit is not active: {state}"
    assert code == 0, f"valkey-cli ping failed with exit code {code}: {err}"
    assert out == "PONG", f"valkey did not answer ping as the default user: {out!r} {err}"


def test_valkey_is_reachable_only_over_tls_on_loopback(remote_exec, sudo_user_credentials):
    # Verifies that the data port is bound to loopback, closed in the firewall, and refuses plaintext.
    user, password = sudo_user_credentials
    service = ValkeyService(remote_exec)

    sockets = service.listening_sockets()
    rules = service.firewall_rules()
    _, _, plaintext_code = service.cli(user, password, "ping", tls=False)

    assert f"127.0.0.1:{ValkeyService.TLS_PORT}" in sockets, (
        f"valkey is not listening on loopback port {ValkeyService.TLS_PORT}: {sockets!r}"
    )
    assert f"0.0.0.0:{ValkeyService.TLS_PORT}" not in sockets, (
        f"valkey is listening on all interfaces, expected loopback only: {sockets!r}"
    )
    assert str(ValkeyService.TLS_PORT) not in rules, (
        f"firewall exposes the valkey port, expected only 22: {rules!r}"
    )
    assert plaintext_code != 0, (
        "a plaintext client connected; valkey is configured TLS-only (port 0)"
    )


def test_valkey_stores_and_returns_a_value(remote_exec, sudo_user_credentials):
    # Verifies that a value written by the sudo user is read back unchanged.
    user, password = sudo_user_credentials
    service = ValkeyService(remote_exec)
    key = f"regression:{uuid.uuid4().hex}"
    value = uuid.uuid4().hex

    written, _, _ = service.cli(user, password, f"set {key} {value}")
    read, err, code = service.cli(user, password, f"get {key}")

    assert written == "OK", f"valkey did not accept the write: {written!r}"
    assert code == 0, f"valkey-cli get failed with exit code {code}: {err}"
    assert read == value, f"valkey returned a different value than it stored: {read!r}"


def test_valkey_expires_a_key(remote_exec, sudo_user_credentials):
    # Verifies that a key written with a TTL is tracked as expiring, the caching primitive.
    user, password = sudo_user_credentials
    service = ValkeyService(remote_exec)
    key = f"regression:{uuid.uuid4().hex}"
    ttl_seconds = 120

    written, _, _ = service.cli(user, password, f"set {key} cached EX {ttl_seconds}")
    remaining, err, code = service.cli(user, password, f"ttl {key}")

    assert written == "OK", f"valkey did not accept the write with a TTL: {written!r}"
    assert code == 0, f"valkey-cli ttl failed with exit code {code}: {err}"
    assert remaining.isdigit(), f"valkey did not report a numeric TTL: {remaining!r} {err}"
    assert 0 < int(remaining) <= ttl_seconds, (
        f"valkey reported a TTL outside the requested window: {remaining}"
    )


def test_valkey_tech_docs(context, techdocs_url):
    """Verify that the Valkey tech docs page is accessible."""
    tech_docs_page = ValkeyTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Valkey tech docs page title is incorrect.").to_have_title("Valkey")
    expect(tech_docs_page.valkey_header, "Valkey tech docs header did not render.").to_be_visible()
