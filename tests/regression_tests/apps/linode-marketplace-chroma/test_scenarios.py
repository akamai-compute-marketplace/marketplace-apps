import uuid

from regression_tests.services.chroma.chroma_service import ChromaService


def test_chroma_service_active(remote_exec):
    # Verifies nginx is running and the Chroma docker container is up.
    service = ChromaService(remote_exec=remote_exec)
    assert service.nginx_active() == "active", "nginx unit is not active"
    assert "Up" in service.container_status(), "Chroma container is not running"


def test_chroma_port_posture(remote_exec):
    # Verifies the intended firewall posture: Chroma bound to loopback, nginx public on 443.
    service = ChromaService(remote_exec=remote_exec)
    ports = service.listening_ports()
    assert "127.0.0.1:8000" in ports, "Chroma API is not bound to loopback 127.0.0.1:8000"
    assert "0.0.0.0:443" in ports, "nginx is not listening on public 443"


def test_chroma_local_heartbeat(remote_exec):
    # Verifies the container serves the API on the loopback port
    service = ChromaService(remote_exec=remote_exec)
    assert "nanosecond heartbeat" in service.local_heartbeat_body(), \
        "Chroma loopback heartbeat did not return a valid response"


def test_chroma_public_requires_auth(http_session, base_url):
    # Verifies the public nginx surface rejects unauthenticated requests
    service = ChromaService(http_session=http_session, base_url=base_url)
    response = service.heartbeat(authenticated=False)
    assert response.status_code == 401, \
        f"expected 401 without credentials, got {response.status_code}"


def test_chroma_public_authenticated_heartbeat(http_session, base_url, app_credentials):
    # Verifies the public API answers the heartbeat when authenticated end to end.
    auth = (app_credentials["Chroma Username"], app_credentials["Chroma Password"])
    service = ChromaService(http_session=http_session, base_url=base_url, auth=auth)
    response = service.heartbeat(authenticated=True)
    assert response.status_code == 200, \
        f"expected 200 with credentials, got {response.status_code}"
    assert "nanosecond heartbeat" in response.text, \
        "authenticated heartbeat body missing expected field"


def test_chroma_collection(http_session, base_url, app_credentials):
    # End-to-end vector-store check via the authenticated public API
    auth = (app_credentials["Chroma Username"], app_credentials["Chroma Password"])
    service = ChromaService(http_session=http_session, base_url=base_url, auth=auth)
    name = f"regression-test-{uuid.uuid4().hex[:8]}"

    collection = service.create_collection(name)
    assert collection.status_code == 200, \
        f"collection create failed: {collection.status_code} {collection.text}"
    collection_id = collection.json()["id"]

    names = [c["name"] for c in service.list_collections().json()]
    assert name in names, f"created collection {name} not found in collection list"

    add = service.add_records(
        collection_id,
        ids=["near", "far"],
        embeddings=[[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]],
        documents=["document about pineapple", "document about spaceships"],
        metadatas=[{"topic": "fruit"}, {"topic": "scifi"}],
    )
    assert add.status_code == 201, f"add records failed: {add.status_code} {add.text}"
    assert service.count(collection_id).json() == 2, "collection did not report 2 stored records"

    result = service.query(collection_id, query_embeddings=[[1.0, 2.0, 3.1]], n_results=2)
    assert result.status_code == 200, f"query failed: {result.status_code} {result.text}"
    body = result.json()
    ids = body["ids"][0]
    documents = body["documents"][0]
    distances = body["distances"][0]
    assert ids[0] == "near", f"expected 'near' as closest match, got order {ids}"
    assert documents[0] == "document about pineapple", "closest match returned the wrong document"
    assert distances[0] < distances[1], "distances are not ordered nearest-first"
