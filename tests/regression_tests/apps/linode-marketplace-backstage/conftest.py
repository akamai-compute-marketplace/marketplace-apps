import pytest


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base HTTPS URL for the Backstage app.

    The app runs on port 3000.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Backstage app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:3000"
