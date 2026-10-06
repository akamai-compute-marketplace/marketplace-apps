import uuid

from regression_tests.services.mysql.mysql_service import MysqlService
from regression_tests.services.mysqld_exporter.mysqld_exporter_service import MysqldExporterService


def test_mysql_up(remote_exec, app_credentials):
    # Verifies that the database unit is active and answers an authenticated query.
    service = MysqlService(remote_exec)
    assert service.unit_active() == "active", "mariadb unit is not active"
    out, err, code = service.query(app_credentials["MySQL Root Password"], "SELECT 1;")
    assert code == 0, f"SELECT 1 failed (exit {code}): {err or out}"
    assert out == "1", f"unexpected result from SELECT 1: {out}"


def test_mysql_port_listening_on_loopback(remote_exec):
    # Verifies that the server listens on 3306 and stays bound to loopback only.
    service = MysqlService(remote_exec)
    listener = service.port_listener()
    assert "127.0.0.1:3306" in listener, f"mysql is not listening on loopback port 3306: {listener}"
    assert "0.0.0.0:3306" not in listener, f"mysql is exposed on all interfaces: {listener}"


def test_mysql_data_roundtrip(remote_exec, app_credentials):
    # Verifies that a row written to a new database can be read back with its value intact.
    service = MysqlService(remote_exec)
    password = app_credentials["MySQL Root Password"]
    suffix = uuid.uuid4().hex[:12]
    database = f"smoke_{suffix}"
    label = f"roundtrip-{suffix}"
    out, err, code = service.query(
        password,
        f"CREATE DATABASE {database};"
        f"CREATE TABLE {database}.items (id INT PRIMARY KEY, label VARCHAR(64));"
        f"INSERT INTO {database}.items (id, label) VALUES (1, '{label}');"
        f"SELECT label FROM {database}.items WHERE id = 1;",
    )
    assert code == 0, f"write/read round-trip failed (exit {code}): {err or out}"
    assert out == label, f"row did not round-trip, expected {label}: {out}"
    service.query(password, f"DROP DATABASE {database};")


def test_mysql_rejects_invalid_password(remote_exec):
    # Verifies that the database refuses a connection made with a wrong password.
    service = MysqlService(remote_exec)
    out, err, code = service.query("invalid-" + uuid.uuid4().hex, "SELECT 1;")
    assert code != 0, f"authentication with an invalid password unexpectedly succeeded: {out}"
    assert "Access denied" in err, f"unexpected error for an invalid password: {err or out}"


def test_mysqld_exporter_alive(remote_exec):
    # Verifies the add-on unit is active, enabled at boot and runs as the unprivileged prometheus user.
    exporter = MysqldExporterService(remote_exec)
    assert exporter.unit_active() == "active", "mysqld_exporter unit is not active"
    assert exporter.unit_enabled() == "enabled", "mysqld_exporter is not enabled at boot"
    user = exporter.process_user()
    assert user == "prometheus", f"mysqld_exporter runs as unexpected user: {user}"


def test_mysqld_exporter_connected_to_database(remote_exec):
    # Verifies the exporter authenticates to MariaDB and reports its version.
    exporter = MysqldExporterService(remote_exec)
    assert exporter.value("mysql_up") == 1, "mysql_up is not 1 - exporter cannot log in to the database"
    version = exporter.line("mysql_version_info{")
    assert version and "MariaDB" in version, f"unexpected version info: {version}"


def test_mysqld_exporter_tracks_database_activity(remote_exec, app_credentials):
    # Verifies that real INSERTs are reflected in the exported command counters.
    service = MysqlService(remote_exec)
    exporter = MysqldExporterService(remote_exec)
    password = app_credentials["MySQL Root Password"]
    database = f"exporter_{uuid.uuid4().hex[:12]}"
    rows = 5
    insert_counter = 'mysql_global_status_commands_total{command="insert"}'
    before = exporter.value(insert_counter)
    assert before is not None, "insert command counter is not exported"
    out, err, code = service.query(
        password,
        f"CREATE DATABASE {database};"
        f"CREATE TABLE {database}.items (id INT);"
        + "".join(f"INSERT INTO {database}.items VALUES ({i});" for i in range(rows)),
    )
    assert code == 0, f"database workload failed (exit {code}): {err or out}"
    after = exporter.value(insert_counter)
    assert after is not None, "insert command counter disappeared after the workload"
    assert after - before >= rows, f"insert counter did not grow by {rows}: {before} -> {after}"
