import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Jaeger server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Jaeger app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Jaeger app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides HTTP Basic Auth credentials for the Jaeger browser context.
    Overrides the default (None) from the global conftest.
    """
    return {
        "username": app_credentials["Jaeger Username"],
        "password": app_credentials["Jaeger Password"],
    }
