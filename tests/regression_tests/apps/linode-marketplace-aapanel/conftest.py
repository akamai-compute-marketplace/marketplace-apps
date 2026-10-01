import re

import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """Return the path to the aaPanel credentials file on the remote server."""
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(remote_exec) -> str:
    """Return the aaPanel URL from the deployment-generated MOTD."""
    output, error, exit_code = remote_exec("cat /etc/motd")
    if exit_code != 0:
        raise RuntimeError(f"Could not read aaPanel MOTD: {error or output}")

    match = re.search(r"^App URL:\s*(https?://\S+)", output, re.MULTILINE)
    if not match:
        raise RuntimeError(f"aaPanel URL was not found in /etc/motd: {output!r}")
    return match.group(1)
