from playwright.sync_api import expect

from regression_tests.pages.docker.docker_tech_docs_page import DockerTechDocsPage
from regression_tests.services.node_exporter.node_exporter_service import NodeExporterService
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


def test_node_exporter_alive(remote_exec):
    # Verifies that the node_exporter add-on runs as an enabled service under the prometheus user.
    exporter = NodeExporterService(remote_exec)
    assert exporter.unit_active() == "active", "node_exporter unit is not active"
    assert exporter.unit_enabled() == "enabled", "node_exporter unit is not enabled"
    assert exporter.process_user() == "prometheus", "node_exporter is not running as prometheus"


def test_node_exporter_reports_this_host(remote_exec):
    # Verifies that the exported metrics describe this host, not just any answer on the port.
    exporter = NodeExporterService(remote_exec)
    hostname, _, _ = remote_exec("hostname")
    uname = exporter.line("node_uname_info{")
    assert uname and f'nodename="{hostname}"' in uname, f"nodename does not match hostname {hostname}: {uname}"
    mem_kb, _, _ = remote_exec("awk '/^MemTotal:/ {print $2}' /proc/meminfo")
    assert exporter.value("node_memory_MemTotal_bytes") == float(mem_kb) * 1024, "MemTotal does not match /proc/meminfo"


def test_node_exporter_sees_docker(remote_exec):
    # Verifies that the exporter observes the Docker bridge interface.
    exporter = NodeExporterService(remote_exec)
    assert exporter.value('node_network_receive_bytes_total{device="docker0"}') is not None, "docker0 not reported"


def test_docker_tech_docs(context, techdocs_url):
    """Verify that the Docker tech docs page is accessible."""
    tech_docs_page = DockerTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Docker tech docs page did not load.").to_have_title("Docker")
    expect(tech_docs_page.docker_header, "Docker tech docs header did not render.").to_be_visible()
