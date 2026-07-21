import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Owncast server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Owncast app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Owncast app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides HTTP Basic Auth credentials for the Owncast browser context.
    Overrides the default (None) from the global conftest.
    The public homepage doesn't require auth; only /admin is protected by HTTP Basic Auth.
    """
    return {
        "username": app_credentials["Owncast Admin Username"],
        "password": app_credentials["Owncast Admin Password"],
    }
