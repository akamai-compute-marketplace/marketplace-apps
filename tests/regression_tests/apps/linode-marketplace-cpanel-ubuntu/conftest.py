import pytest


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the cPanel/WHM admin interface.
    WHM is served on port 2087 via the Linode reverse-DNS hostname.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the WHM admin interface.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:2087"


@pytest.fixture(scope="session")
def app_credentials(ssh_credentials) -> dict:
    """
    Returns cPanel/WHM login credentials.
    WHM uses the system root account — no separate credentials file is needed.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        dict: Credentials dict with 'username' and 'password' keys.
    """
    host, user, password = ssh_credentials
    return {
        "username": user,
        "password": password,
    }
