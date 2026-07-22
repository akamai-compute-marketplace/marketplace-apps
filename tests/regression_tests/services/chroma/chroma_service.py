class ChromaService:
    """
    Service actions for Chroma, over two vantages, with NO assertions (those live in tests):
      - SSH (remote_exec): on-box liveness, port posture, and the loopback API that is
        bound to 127.0.0.1:8000 and firewalled (ufw), so it is unreachable from the runner.
      - HTTP (http_session): the public API served by nginx on 443 behind HTTP Basic Auth.
    """

    CONTAINER_FILTER = "compose-server"
    LOCAL_API = "http://127.0.0.1:8000"
    COLLECTIONS_PATH = "/api/v2/tenants/default_tenant/databases/default_database/collections"
    HEARTBEAT_PATH = "/api/v2/heartbeat"

    def __init__(self, remote_exec=None, http_session=None, base_url=None, auth=None):
        self._run = remote_exec
        self._http = http_session
        self._base = base_url.rstrip("/") if base_url else None
        self._auth = auth

    def nginx_active(self) -> str:
        out, _, _ = self._run("systemctl is-active nginx")
        return out

    def container_status(self) -> str:
        out, _, _ = self._run(
            f"docker ps --filter name={self.CONTAINER_FILTER} --format '{{{{.Status}}}}'"
        )
        return out

    def listening_ports(self) -> str:
        out, _, _ = self._run("ss -tlnH")
        return out

    def local_heartbeat_body(self) -> str:
        out, _, _ = self._run(f"curl -s {self.LOCAL_API}{self.HEARTBEAT_PATH}")
        return out

    def heartbeat(self, authenticated: bool):
        auth = self._auth if authenticated else None
        return self._http.get(f"{self._base}{self.HEARTBEAT_PATH}", auth=auth, timeout=30)

    def list_collections(self):
        return self._http.get(f"{self._base}{self.COLLECTIONS_PATH}", auth=self._auth, timeout=30)

    def create_collection(self, name: str):
        return self._http.post(
            f"{self._base}{self.COLLECTIONS_PATH}",
            auth=self._auth,
            json={"name": name},
            timeout=30,
        )

    def add_records(self, collection_id, ids, embeddings, documents, metadatas=None):
        payload = {"ids": ids, "embeddings": embeddings, "documents": documents}
        if metadatas is not None:
            payload["metadatas"] = metadatas
        return self._http.post(
            f"{self._base}{self.COLLECTIONS_PATH}/{collection_id}/add",
            auth=self._auth,
            json=payload,
            timeout=30,
        )

    def query(self, collection_id, query_embeddings, n_results):
        return self._http.post(
            f"{self._base}{self.COLLECTIONS_PATH}/{collection_id}/query",
            auth=self._auth,
            json={"query_embeddings": query_embeddings, "n_results": n_results},
            timeout=30,
        )

    def count(self, collection_id):
        return self._http.get(
            f"{self._base}{self.COLLECTIONS_PATH}/{collection_id}/count",
            auth=self._auth,
            timeout=30,
        )
