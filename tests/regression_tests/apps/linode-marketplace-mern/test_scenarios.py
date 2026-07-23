import uuid

from regression_tests.services.mern.mern_service import MernService


def test_mern_api_up(remote_exec, http_session, base_url):
    # Verifies that the Express backend is active and its API answers over the public nginx proxy.
    service = MernService(remote_exec=remote_exec, http_session=http_session, base_url=base_url)
    assert service.unit_active("express") == "active", "express unit is not active"
    response = service.api_get("/api/")
    assert response.status_code == 200, f"API returned {response.status_code}: {response.text}"
    assert response.json()["message"] == "API is running!", f"unexpected API body: {response.text}"


def test_mern_mongodb_up(remote_exec, app_credentials):
    # Verifies that MongoDB is active and answers an authenticated ping.
    service = MernService(remote_exec=remote_exec)
    assert service.unit_active("mongod") == "active", "mongod unit is not active"
    out, err, code = service.mongo_eval(
        app_credentials["MongoDB Admin User"],
        app_credentials["MongoDB Admin Password"],
        "admin",
        "db.runCommand({ping: 1}).ok",
    )
    assert code == 0, f"mongo ping failed (exit {code}): {err or out}"
    assert out.strip() == "1", f"mongo ping did not return ok: {out}"


def test_mern_mongodb_loopback(remote_exec):
    # Verifies MongoDB's firewall posture: bound to loopback only, not exposed publicly.
    service = MernService(remote_exec=remote_exec)
    ports = service.listening_ports()
    assert "127.0.0.1:27017" in ports, f"MongoDB is not bound to loopback 127.0.0.1:27017: {ports}"


def test_mern_mongodb_roundtrip(remote_exec, app_credentials):
    # Verifies that a document written to MongoDB can be read back with its value intact.
    service = MernService(remote_exec=remote_exec)
    collection = f"smoke_{uuid.uuid4().hex}"
    script = (
        f'db.getCollection("{collection}").insertOne({{k: "{collection}", val: 42}}); '
        f'print(db.getCollection("{collection}").findOne({{k: "{collection}"}}).val);'
    )
    out, err, code = service.mongo_eval(
        app_credentials["MongoDB Admin User"],
        app_credentials["MongoDB Admin Password"],
        "smoke_test",
        script,
    )
    assert code == 0, f"mongo round-trip failed (exit {code}): {err or out}"
    assert "42" in out, f"document value did not round-trip: {out}"


def test_mern_mongodb_auth_enforced(remote_exec):
    # Verifies that MongoDB rejects unauthenticated privileged commands.
    service = MernService(remote_exec=remote_exec)
    out, err, code = service.mongo_eval_unauthenticated("db.adminCommand({listDatabases: 1}).ok")
    assert "requires authentication" in (out + err), \
        f"MongoDB did not enforce authentication: {out or err}"
