import paramiko
from contextlib import contextmanager


@contextmanager
def ssh_connection(host: str, username: str, password: str, timeout: int = 30):
    """
    Establishes and manages an SSH connection lifecycle.

    Args:
        host (str): The IPv4 address or hostname of the remote server.
        username (str): The SSH username.
        password (str): The SSH password.
        timeout (int, optional): Connection timeout in seconds. Defaults to 30.

    Yields:
        paramiko.SSHClient: An active, authenticated SSH client session.

    Raises:
        paramiko.AuthenticationException: If authentication fails.
        paramiko.SSHException: If there is an error connecting or establishing the SSH session.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, password=password, timeout=timeout)
        yield client
    finally:
        client.close()


def get_credentials_via_ssh(host: str, username: str, password: str, remote_path: str) -> dict:
    """
    Retrieves and parses a credentials file from a Linode via SSH.

    Args:
        host (str): The IPv4 address or hostname of the remote server.
        username (str): The SSH username.
        password (str): The SSH password.
        remote_path (str): The absolute path to the credentials file on the remote server.

    Returns:
        dict: A dictionary mapping the credential keys to their respective values.

    Raises:
        RuntimeError: If the remote file is empty, does not exist, or if the `cat` command fails.
    """
    with ssh_connection(host, username, password) as client:
        _, stdout, stderr = client.exec_command(f"cat {remote_path}")
        content = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if not content:
            raise RuntimeError(
                f"No credentials found at {remote_path} on {host}. "
                f"SSH stderr: {error or '(empty)'}"
            )

        creds = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition(": ")
            creds[key.strip()] = value.strip()

        return creds
