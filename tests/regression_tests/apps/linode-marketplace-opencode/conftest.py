import pytest

from regression_tests.services.opencode.opencode_service import OpenCodeService


@pytest.fixture(scope="module")
def opencode_server(remote_exec):
    """
    Starts the OpenCode headless server once for the module.
    """
    OpenCodeService(remote_exec).start_server()
