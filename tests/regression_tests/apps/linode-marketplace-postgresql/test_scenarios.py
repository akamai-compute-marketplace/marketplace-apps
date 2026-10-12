import uuid
from playwright.sync_api import expect
from regression_tests.pages.postgresql.postgresql_tech_docs_page import PostgresqlTechDocsPage
from regression_tests.services.postgresql.postgresql_service import PostgresqlService
from regression_tests.services.newrelic.newrelic_service import NewrelicService


def test_postgresql_up(remote_exec, app_credentials):
    # Verifies that the Postgres cluster is running and answers an authenticated query.
    service = PostgresqlService(remote_exec)
    unit, active, sub = service.cluster_unit_state()
    assert unit, "no postgresql@<version>-main cluster unit was found"
    assert active == "active", f"{unit} is not active: {active}"
    assert sub == "running", f"{unit} is not running: {sub}"

    ready, code = service.is_ready()
    assert code == 0, f"pg_isready reported the cluster not accepting connections: {ready}"

    out, err, code = service.query(app_credentials["Postgresql Password"], "SELECT 1;")
    assert code == 0, f"SELECT 1 failed (exit {code}): {err or out}"
    assert out == "1", f"unexpected result from SELECT 1: {out}"


def test_postgresql_listens_on_loopback(remote_exec):
    # Verifies that Postgres listens on 5432 and stays bound to loopback only.
    service = PostgresqlService(remote_exec)
    listener = service.port_listener()
    assert "127.0.0.1:5432" in listener, f"postgres is not listening on loopback 5432: {listener}"
    assert "0.0.0.0:5432" not in listener, f"postgres is exposed on all interfaces: {listener}"


def test_postgresql_data_roundtrip(remote_exec, app_credentials):
    # Verifies that a row written to a new table can be read back with its value intact.
    service = PostgresqlService(remote_exec)
    password = app_credentials["Postgresql Password"]
    suffix = uuid.uuid4().hex[:12]
    table = f"smoke_{suffix}"
    label = f"roundtrip-{suffix}"

    out, err, code = service.query(
        password,
        f"CREATE TABLE {table} (id int PRIMARY KEY, label text);"
        f"INSERT INTO {table} (id, label) VALUES (1, '{label}');",
    )
    assert code == 0, f"seeding the table failed (exit {code}): {err or out}"

    out, err, code = service.query(password, f"SELECT label FROM {table} WHERE id = 1;")
    assert code == 0, f"reading the row back failed (exit {code}): {err or out}"
    assert out == label, f"row did not round-trip, expected {label}: {out!r}"

    service.query(password, f"DROP TABLE {table};")


def test_newrelic_cli_installed(remote_exec):
    # Verifies the New Relic CLI is installed root-owned and executable, and actually runs.
    newrelic = NewrelicService(remote_exec)
    assert newrelic.file_mode_owner(newrelic.CLI) == "755 root:root", "newrelic CLI has unexpected mode or owner"
    code, output = newrelic.cli_version()
    assert code == 0 and "newrelic" in output.lower(), f"newrelic CLI did not run (exit {code}): {output}"


def test_newrelic_first_login_script_ready(remote_exec):
    # Verifies the first-login setup script is staged, valid, and still waiting for a user to run it.
    newrelic = NewrelicService(remote_exec)
    assert newrelic.file_mode_owner(newrelic.LOGIN_SCRIPT) == "755 root:root", "login script has unexpected mode or owner"
    error = newrelic.login_script_syntax_error()
    assert error is None, f"login script has a syntax error: {error}"
    assert not newrelic.login_script_completed(), "login script already ran; expected it to wait for the first login"


def test_postgresql_tech_docs(context, techdocs_url):
    """Verify that the PostgreSQL tech docs page is accessible."""
    tech_docs_page = PostgresqlTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "PostgreSQL tech docs page title is incorrect.").to_have_title("PostgreSQL")
    expect(tech_docs_page.postgresql_header, "PostgreSQL tech docs header did not render.").to_be_visible()
