import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """Return the path to the Microweber credentials file on the remote server."""
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """Return the Microweber site URL from the Linode reverse-DNS hostname."""
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def admin_url(base_url) -> str:
    """Return the Microweber admin URL."""
    return f"{base_url}/admin"
