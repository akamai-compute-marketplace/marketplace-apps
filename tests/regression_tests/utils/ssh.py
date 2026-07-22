import logging
import paramiko
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class _StrictHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    """
    A host key policy that verifies the server's host key against an expected key.
    Raises an SSHException if the key does not match, preventing man-in-the-middle attacks.
    """

    def __init__(self, expected_host_key: paramiko.PKey):
        self._expected = expected_host_key

    def missing_host_key(self, client: paramiko.SSHClient, hostname: str, key: paramiko.PKey) -> None:
        if key.get_fingerprint() != self._expected.get_fingerprint():
            raise paramiko.SSHException(
                f"Host key verification failed for {hostname}. "
                "The server's host key does not match the expected key."
            )


def _scan_host_key(host: str, port: int = 22, timeout: int = 30) -> paramiko.PKey:
    """
    Retrieves the remote server's host key without authenticating (Trust On First Use).

    Args:
        host (str): The IPv4 address or hostname of the remote server.
        port (int, optional): The SSH port. Defaults to 22.
        timeout (int, optional): Socket timeout in seconds. Defaults to 30.

    Returns:
        paramiko.PKey: The host key presented by the server.

    Raises:
        paramiko.SSHException: If the transport handshake fails.
    """
    transport = paramiko.Transport((host, port))
    transport.banner_timeout = timeout
    try:
        transport.connect()
        key = transport.get_remote_server_key()
    finally:
        transport.close()

    logger.warning(
        "TOFU: pinning %s host key for %s (fingerprint: %s)",
        key.get_name(),
        host,
        key.get_fingerprint().hex(),
    )
    return key


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
        paramiko.SSHException: If there is an error connecting, establishing the SSH session,
            or if the server's host key cannot be verified.
    """
    host_key = _scan_host_key(host, timeout=timeout)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(_StrictHostKeyPolicy(host_key))
    try:
        client.connect(hostname=host, username=username, password=password, timeout=timeout)
        yield client
    finally:
        client.close()


def run_remote_command(host: str, username: str, password: str, command: str,
                       timeout: int = 30) -> tuple[str, str, int]:
    """
    Runs a single command on the remote Linode over SSH and returns its result.

    Args:
        host (str): The IPv4 address or hostname of the remote server.
        username (str): The SSH username.
        password (str): The SSH password.
        command (str): The command to execute on the VM.
        timeout (int, optional): Command/connection timeout in seconds. Defaults to 30.

    Returns:
        tuple[str, str, int]: (stdout, stderr, exit_code), with stdout/stderr stripped.
    """
    with ssh_connection(host, username, password, timeout=timeout) as client:
        _, stdout, stderr = client.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        return out, err, exit_code


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
            if ": " in line:
                key, _, value = line.partition(": ")
            elif "=" in line:
                key, _, value = line.partition("=")
            else:
                continue
            creds[key.strip()] = value.strip()

        return creds
