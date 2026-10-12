import uuid
from playwright.sync_api import expect
from regression_tests.pages.openbao.openbao_tech_docs_page import OpenBaoTechDocsPage
from regression_tests.services.openbao.openbao_service import OpenBaoService


def test_openbao_up(remote_exec):
    # Verifies that OpenBao is active and its API answers a seal-status request.
    service = OpenBaoService(remote_exec)
    assert service.unit_active() == "active", "openbao unit is not active"
    fields = service.status_fields()
    assert fields, "bao status returned no parseable seal status"
    assert fields.get("Initialized") == "true", f"openbao was not initialized by the deploy: {fields}"


def test_openbao_listens_on_configured_address(remote_exec):
    # Verifies that OpenBao listens on 8200 at the address the deploy configured, not a wildcard.
    service = OpenBaoService(remote_exec)
    api_address = service.api_address()
    assert api_address.startswith("https://"), f"api_addr is not an https endpoint: {api_address}"
    host = api_address.removeprefix("https://").split(":")[0]
    assert host != "0.0.0.0", (
        "openbao is configured on the wildcard address; raft cannot unseal with an "
        f"unspecified cluster address: {api_address}"
    )
    listener = service.port_listener()
    assert f"{host}:8200" in listener, f"openbao is not listening on {host}:8200: {listener}"


def test_openbao_credentials_contain_unseal_material(app_credentials):
    # Verifies that the deploy recorded the init output needed to unseal the vault.
    for key in ("Unseal Key 1", "Unseal Key 2", "Unseal Key 3"):
        assert app_credentials.get(key), f"{key} missing from the credentials file"
    assert app_credentials.get("Initial Root Token"), "Initial Root Token missing from credentials"


def test_openbao_unseals_with_key_threshold(remote_exec, app_credentials):
    # Verifies that two of the three unseal keys are enough to unseal the vault.
    service = OpenBaoService(remote_exec)
    out, err, code = service.unseal(app_credentials["Unseal Key 1"])
    assert code == 0, f"first unseal key was rejected (exit {code}): {err or out}"
    out, err, code = service.unseal(app_credentials["Unseal Key 2"])
    assert code == 0, f"second unseal key was rejected (exit {code}): {err or out}"
    assert service.status_fields().get("Sealed") == "false", "vault did not unseal at the threshold"


def test_openbao_secret_roundtrip(remote_exec, app_credentials):
    # Verifies that a secret written to a kv-v2 mount can be read back with its value intact.
    service = OpenBaoService(remote_exec)
    token = app_credentials["Initial Root Token"]
    service.unseal(app_credentials["Unseal Key 1"])
    service.unseal(app_credentials["Unseal Key 2"])

    mount = f"smoke{uuid.uuid4().hex[:12]}"
    value = f"roundtrip-{uuid.uuid4().hex[:12]}"
    out, err, code = service.enable_kv(mount, token)
    assert code == 0, f"enabling a kv-v2 mount failed (exit {code}): {err or out}"

    out, err, code = service.kv_put(f"{mount}/probe", token, "value", value)
    assert code == 0, f"writing a secret failed (exit {code}): {err or out}"

    out, err, code = service.kv_get_field(f"{mount}/probe", token, "value")
    assert code == 0, f"reading the secret back failed (exit {code}): {err or out}"
    assert out == value, f"secret did not round-trip, expected {value}: {out}"


def test_openbao_tech_docs(context, techdocs_url):
    """Verify that the OpenBao tech docs page is accessible."""
    tech_docs_page = OpenBaoTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenBao tech docs title did not match.").to_have_title("OpenBao")
    expect(tech_docs_page.openbao_header, "OpenBao tech docs header did not render.").to_be_visible()
