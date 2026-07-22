from regression_tests.services.linuxgsm.linuxgsm_service import LinuxGSMService


def test_linuxgsm_up(remote_exec):
    # Verifies that LinuxGSM is installed and its CLI runs and reports a version.
    service = LinuxGSMService(remote_exec)
    out, code = service.version()
    assert code == 0, f"linuxgsm.sh did not run (exit {code}): {out}"
    assert "Linux Game Server Managers" in out, f"unexpected linuxgsm output: {out}"
    assert "Version v" in out, f"linuxgsm did not report a version: {out}"


def test_linuxgsm_list_servers(remote_exec):
    # Verifies that LinuxGSM can fetch and list the available game servers.
    service = LinuxGSMService(remote_exec)
    out, code = service.list_servers()
    assert code == 0, f"linuxgsm.sh list failed (exit {code}): {out}"
    assert "arma3server" in out, f"expected game server missing from the catalog: {out}"
