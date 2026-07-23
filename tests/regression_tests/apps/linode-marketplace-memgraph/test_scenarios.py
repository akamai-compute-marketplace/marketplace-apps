import uuid

from regression_tests.services.memgraph.memgraph_service import MemgraphService


def test_memgraph_up(remote_exec, app_credentials):
    # Verifies that Memgraph is active and answers an authenticated Cypher query.
    service = MemgraphService(remote_exec)
    assert service.unit_active() == "active", "memgraph unit is not active"
    out, err, code = service.cypher(
        app_credentials["Memgraph User"], app_credentials["Memgraph Password"], "RETURN 1 AS ok;"
    )
    assert code == 0, f"cypher query failed (exit {code}): {err or out}"
    assert '"1"' in out, f"unexpected result from RETURN 1: {out}"


def test_memgraph_bolt_listening(remote_exec):
    # Verifies that Memgraph is listening on the Bolt port.
    service = MemgraphService(remote_exec)
    listener = service.bolt_listener()
    assert ":7687" in listener, f"memgraph is not listening on the Bolt port: {listener}"


def test_memgraph_data_roundtrip(remote_exec, app_credentials):
    # Verifies that a node written to Memgraph can be read back with its property intact.
    service = MemgraphService(remote_exec)
    user = app_credentials["Memgraph User"]
    password = app_credentials["Memgraph Password"]
    node_id = uuid.uuid4().hex
    query = (
        f"CREATE (n:SmokeTest {{id: '{node_id}', val: 42}});"
        f"MATCH (n:SmokeTest {{id: '{node_id}'}}) RETURN n.val AS val;"
    )
    out, err, code = service.cypher(user, password, query)
    assert code == 0, f"cypher round-trip failed (exit {code}): {err or out}"
    assert '"42"' in out, f"node property did not round-trip: {out}"
