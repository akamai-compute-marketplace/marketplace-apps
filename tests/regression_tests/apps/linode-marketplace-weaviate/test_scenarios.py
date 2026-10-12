import uuid
from playwright.sync_api import expect
from regression_tests.pages.weaviate.weaviate_tech_docs_page import WeaviateTechDocsPage
from regression_tests.services.weaviate.weaviate_service import WeaviateService

ADMIN_KEY = "Admin API Key"


def test_weaviate_up_and_ready(remote_exec, http_session, base_url):
    # Verifies that both containers run and the readiness endpoint answers without a key.
    service = WeaviateService(remote_exec, http_session, base_url)

    weaviate = service.container_status(WeaviateService.WEAVIATE_CONTAINER)
    transformers = service.container_status(WeaviateService.TRANSFORMERS_CONTAINER)
    ready = service.ready_status()

    assert weaviate == "running", f"weaviate container is not running: {weaviate}"
    assert transformers == "running", f"transformers container is not running: {transformers}"
    assert ready == 200, f"readiness endpoint did not report ready: HTTP {ready}"


def test_weaviate_requires_an_api_key(remote_exec, http_session, base_url, app_credentials):
    # Verifies that the API rejects anonymous reads and accepts the admin key.
    service = WeaviateService(remote_exec, http_session, base_url)

    anonymous = service.meta()
    authenticated = service.meta(app_credentials[ADMIN_KEY])

    assert anonymous.status_code == 401, (
        f"anonymous access to /v1/meta was not rejected: HTTP {anonymous.status_code}"
    )
    assert authenticated.status_code == 200, (
        f"admin key was rejected on /v1/meta: HTTP {authenticated.status_code}"
    )
    assert "version" in authenticated.json(), (
        f"/v1/meta did not return server metadata: {authenticated.text[:200]}"
    )


def test_weaviate_stores_and_retrieves_a_vector(remote_exec, http_session, base_url, app_credentials):
    # Verifies that objects stored with explicit vectors come back from a nearest-neighbour query.
    service = WeaviateService(remote_exec, http_session, base_url)
    api_key = app_credentials[ADMIN_KEY]
    collection = f"Probe{uuid.uuid4().hex[:12]}"

    created = service.create_collection(api_key, collection)
    alpha = service.add_object(api_key, collection, "alpha", [1, 0, 0])
    beta = service.add_object(api_key, collection, "beta", [0, 1, 0])

    assert created.status_code == 200, (
        f"could not create collection {collection}: HTTP {created.status_code} {created.text[:200]}"
    )
    assert alpha.status_code == 200, f"could not store the first object: {alpha.text[:200]}"
    assert beta.status_code == 200, f"could not store the second object: {beta.text[:200]}"

    # Explicit vectors keep the nearest neighbour fixed arithmetic rather than model-dependent.
    assert service.nearest_title(api_key, collection, [0.9, 0.1, 0]) == "alpha", (
        "a query vector closest to alpha did not return alpha"
    )
    assert service.nearest_title(api_key, collection, [0.1, 0.9, 0]) == "beta", (
        "a query vector closest to beta did not return beta"
    )


def test_weaviate_tech_docs(context, techdocs_url):
    """Verify that the Weaviate tech docs page is accessible."""
    tech_docs_page = WeaviateTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Weaviate tech docs page title is incorrect.").to_have_title("Weaviate")
    expect(tech_docs_page.weaviate_header, "Weaviate tech docs header did not render.").to_be_visible()
