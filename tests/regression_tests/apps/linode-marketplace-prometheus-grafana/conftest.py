import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Prometheus & Grafana server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Grafana UI.
    Built from the VM host so the suite works against any freshly deployed instance.
    Prometheus is served from the same host at '<base_url>/prometheus'.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Grafana app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides HTTP Basic Auth credentials for the browser context.
    Only the '/prometheus' path is protected by Basic Auth; sending these
    credentials on every request is harmless for Grafana, which isn't behind
    Basic Auth itself.
    """
    return {
        "username": app_credentials["Prometheus Username"],
        "password": app_credentials["Prometheus Password"],
    }
