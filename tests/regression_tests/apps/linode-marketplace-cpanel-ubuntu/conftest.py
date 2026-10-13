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


@pytest.fixture(scope="session")
def cpanel_techdocs_url(remote_exec) -> str:
    """
    Reads the tech docs link from /etc/motd.sh on the VM.
    cPanel uses a dynamic MOTD script (run from root's .bash_profile) instead of
    /etc/motd, so the line has the form: echo "Documentation: <url>"

    Args:
        remote_exec: Callable that runs a command on the VM over SSH.

    Returns:
        str: The documentation URL, e.g. https://techdocs.akamai.com/quick-deploy-apps/docs/cpanel

    Raises:
        RuntimeError: If /etc/motd.sh cannot be read or has no 'Documentation:' link.
    """
    motd, err, code = remote_exec("cat /etc/motd.sh")
    if code != 0:
        raise RuntimeError(f"Failed to read /etc/motd.sh (exit code {code}): {err}")

    prefix = 'echo "Documentation:'
    for line in motd.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().rstrip('"')
    raise RuntimeError("No Documentation link found in /etc/motd.sh")
