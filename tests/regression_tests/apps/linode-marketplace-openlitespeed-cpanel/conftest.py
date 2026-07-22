import pytest

from regression_tests.utils.ssh import get_credentials_via_ssh


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the WHM admin interface.
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
def litespeed_base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the LiteSpeed WebAdmin console.
    LiteSpeed WebAdmin is served on port 7080 via the Linode reverse-DNS hostname.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the LiteSpeed WebAdmin console.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:7080"


@pytest.fixture(scope="session")
def http_base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the plain HTTP default web site page (port 80), which
    confirms LiteSpeed - not Apache - is serving traffic.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the port-80 default web site page.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"http://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def app_credentials(ssh_credentials) -> dict:
    """
    Returns WHM/cPanel login credentials.
    WHM uses the system root account directly - there is no generated sudo user or
    separate credentials file for WHM login (see architecture_decisions.md D9).

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        dict: Credentials dict with 'username' and 'password' keys.
    """
    _, user, password = ssh_credentials
    return {
        "username": user,
        "password": password,
    }


@pytest.fixture(scope="session")
def litespeed_credentials(ssh_credentials) -> dict:
    """
    Retrieves the LiteSpeed WebAdmin credentials from /root/.credentials via SSH.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        dict: Credentials dict with the file's 'LiteSpeed WebAdmin Username' /
            'LiteSpeed WebAdmin Password' keys.
    """
    host, username, password = ssh_credentials
    return get_credentials_via_ssh(
        host=host,
        username=username,
        password=password,
        remote_path="/root/.credentials",
    )
