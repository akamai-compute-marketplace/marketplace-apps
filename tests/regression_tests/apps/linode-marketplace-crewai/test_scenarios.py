import uuid

from regression_tests.services.crewai.crewai_service import CrewAIService


def test_crewai_up(remote_exec):
    # Verifies that CrewAI is installed and its CLI runs.
    service = CrewAIService(remote_exec)
    out, code = service.version()
    assert code == 0, f"crewai CLI did not run (exit {code}): {out}"
    assert "version" in out.lower(), f"crewai version output unexpected: {out}"


def test_crewai_create_crew_scaffold(remote_exec):
    # Verifies that the CrewAI CLI scaffolds a new crew project.
    service = CrewAIService(remote_exec)
    name = f"regression_{uuid.uuid4().hex[:8]}"
    workdir = f"/tmp/{name}_wd"

    out, err, code = service.create_classic_crew(name, workdir)
    assert code == 0, f"crewai create crew failed (exit {code}): {err or out}"
    assert "created successfully" in out.lower(), f"scaffold did not report success: {out}"

    files = service.list_project_files(workdir, name)
    for expected in [
        "pyproject.toml",
        f"src/{name}/crew.py",
        f"src/{name}/main.py",
        f"src/{name}/config/agents.yaml",
        f"src/{name}/config/tasks.yaml",
    ]:
        assert expected in files, f"scaffolded project missing {expected}\nfound:\n{files}"

    service.remove_workdir(workdir)
