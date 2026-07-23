from regression_tests.services.kali_linux.kali_linux_service import KaliLinuxService


def test_kali_up(remote_exec):
    # Verifies that the box is running Kali Linux and systemd reports the system as running.
    service = KaliLinuxService(remote_exec)
    os_release, code = service.os_release()
    assert code == 0, f"could not read /etc/os-release (exit {code}): {os_release}"
    assert "ID=kali" in os_release, f"box is not running Kali Linux: {os_release}"
    assert "kali" in service.kernel()[0], "running kernel is not the Kali kernel"
    assert service.system_running_state() == "running", "systemd does not report the system as running"


def test_kali_version_installed(remote_exec):
    # Verifies that the installed Kali release and the default toolset metapackage are present.
    service = KaliLinuxService(remote_exec)
    os_release, code = service.os_release()
    assert code == 0, f"could not read /etc/os-release (exit {code}): {os_release}"
    assert "VERSION_ID=" in os_release, f"no Kali version reported: {os_release}"
    version, code = service.default_metapackage_version()
    assert code == 0 and version, f"kali-linux-default metapackage is not installed: {version}"
