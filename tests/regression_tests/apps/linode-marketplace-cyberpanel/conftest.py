import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the CyberPanel admin credentials file on the remote server.
    Note: CyberPanel stores its admin password at /root/.litespeed_password in key=value format.

    Returns:
        str: Absolute path to the CyberPanel credentials file.
    """
    return "/root/.litespeed_password"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the CyberPanel app.
    CyberPanel is served on port 8090 via the Linode reverse-DNS hostname.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the CyberPanel admin interface.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:8090"
