import shlex
import uuid

from playwright.sync_api import expect
from regression_tests.pages.redis.redis_tech_docs_page import RedisTechDocsPage
from regression_tests.services.redis.redis_service import RedisService


def test_redis_up(remote_exec, app_credentials):
    # Verifies that Redis is active and answers an authenticated TLS PING.
    service = RedisService(remote_exec)
    assert service.unit_active() == "active", "redis-server unit is not active"
    out, err, code = service.cli(app_credentials["Redis Default User Password"], "PING")
    assert code == 0, f"PING failed (exit {code}): {err or out}"
    assert out == "PONG", f"unexpected response to PING: {out!r}"


def test_redis_tls_port_reachable_externally(remote_exec):
    # Verifies that the TLS port is bound beyond loopback and opened by the firewall.
    service = RedisService(remote_exec)
    listener = service.port_listener()
    assert "127.0.0.1:6379" in listener, f"redis is not listening on loopback 6379: {listener}"

    external = [
        line for line in listener.splitlines()
        if "127.0.0.1:" not in line and "[::1]:" not in line
    ]
    assert external, f"redis is not bound on a routable address: {listener}"

    firewall = service.ufw_status()
    assert "6379" in firewall, f"ufw does not open the redis port: {firewall}"


def test_redis_set_get_roundtrip(remote_exec, app_credentials):
    # Verifies that a value written to Redis can be read back intact.
    service = RedisService(remote_exec)
    password = app_credentials["Redis Default User Password"]
    suffix = uuid.uuid4().hex[:12]
    key = f"smoke:{suffix}"
    value = f"roundtrip-{suffix}"

    out, err, code = service.cli(password, f"SET {shlex.quote(key)} {shlex.quote(value)}")
    assert code == 0, f"SET failed (exit {code}): {err or out}"
    assert out == "OK", f"unexpected response to SET: {out!r}"

    out, err, code = service.cli(password, f"GET {shlex.quote(key)}")
    assert code == 0, f"GET failed (exit {code}): {err or out}"
    assert out == value, f"value did not round-trip, expected {value}: {out!r}"

    service.cli(password, f"DEL {shlex.quote(key)}")


def test_redis_tech_docs(context, techdocs_url):
    """Verify that the Redis tech docs page is accessible."""
    tech_docs_page = RedisTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Redis tech docs page title is incorrect.").to_have_title("Redis")
    expect(tech_docs_page.redis_header, "Redis tech docs header did not render.").to_be_visible()
