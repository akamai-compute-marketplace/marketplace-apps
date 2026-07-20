import re

import pytest

from regression_tests.utils.ssh import ssh_connection


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Wazuh server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Wazuh app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Wazuh app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def wazuh_dashboard_credentials(ssh_credentials, credentials_file_path) -> dict:
    """
    Retrieves the Wazuh dashboard admin login from the remote credentials file.

    The file repeats the "indexer_username"/"indexer_password" keys for six different
    service accounts (admin, kibanaserver, kibanaro, logstash, readall, snapshotrestore),
    so the shared app_credentials fixture — which parses "Key: Value" pairs into a flat
    dict — resolves to the last occurrence rather than the dashboard-login "admin" account.
    This fixture re-reads the file and extracts the "admin" pair specifically.

    Args:
        ssh_credentials: host, username, password.
        credentials_file_path: Absolute path to the credentials file on the remote server.

    Returns:
        dict: {"username": ..., "password": ...} for the dashboard "admin" indexer account.
    """
    host, username, password = ssh_credentials
    with ssh_connection(host, username, password) as client:
        _, stdout, _ = client.exec_command(f"cat {credentials_file_path}")
        content = stdout.read().decode()

    match = re.search(
        r"indexer_username:\s*'admin'\s*\n\s*indexer_password:\s*'([^']*)'",
        content,
    )
    if not match:
        raise RuntimeError("Could not find the 'admin' indexer account in the credentials file.")

    return {"username": "admin", "password": match.group(1)}
