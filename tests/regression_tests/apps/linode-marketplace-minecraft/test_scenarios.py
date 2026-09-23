from regression_tests.services.minecraft.minecraft_service import MinecraftService


def test_minecraft_service_active(remote_exec):
    # Verifies that the Minecraft LinuxGSM user service is active and running.
    service = MinecraftService(remote_exec)
    output, error, code = service.status()
    status = f"{output}\n{error}"

    assert code == 0, f"mcserver status check failed (exit {code}): {status}"
    assert "Active: active (running)" in status, f"mcserver is not active:\n{status}"


def test_minecraft_ports_listening(remote_exec):
    # Verifies that Minecraft listens on the configured TCP and UDP port.
    service = MinecraftService(remote_exec)
    output, error, code = service.listening_ports()
    ports = f"{output}\n{error}"

    assert code == 0, f"Minecraft port check failed (exit {code}): {ports}"
    assert "tcp" in ports and "LISTEN" in ports and "*:25565" in ports, (
        f"Minecraft TCP port is not listening on *:25565:\n{ports}"
    )
    assert "udp" in ports and "UNCONN" in ports and "*:25565" in ports, (
        f"Minecraft UDP port is not listening on *:25565:\n{ports}"
    )
