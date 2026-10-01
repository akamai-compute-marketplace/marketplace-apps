import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """Return the path to the Akaunting credentials file on the remote server."""

    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """Return the Akaunting URL from the Linode reverse-DNS hostname."""

    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"
