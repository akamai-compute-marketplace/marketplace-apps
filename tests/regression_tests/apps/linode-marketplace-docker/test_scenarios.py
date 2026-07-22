from regression_tests.services.docker.docker_service import DockerService


def test_docker_up(remote_exec):
    # Verifies that the Docker service is active and the daemon responds.
    service = DockerService(remote_exec)
    assert service.unit_active() == "active", "docker unit is not active"
    version, code = service.server_version()
    assert code == 0 and version, f"docker daemon did not respond: {version}"


def test_docker_run_hello_world(remote_exec):
    # Verifies that Docker can pull and run a container.
    service = DockerService(remote_exec)
    out, err, code = service.run_hello_world()
    assert code == 0, f"docker run hello-world failed (exit {code}): {err or out}"
    assert "Hello from Docker!" in out, f"unexpected hello-world output: {out}"
