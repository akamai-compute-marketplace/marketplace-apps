class CrewAIService:
    """
    CLI actions for CrewAI over SSH
    """

    CREWAI = "/root/.env/bin/crewai"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        out, _, code = self._run(f"{self.CREWAI} version")
        return out, code

    def create_classic_crew(self, name, workdir):
        cmd = (
            f"mkdir -p {workdir} && cd {workdir} && "
            f"{self.CREWAI} create crew {name} --classic --skip_provider </dev/null"
        )
        return self._run(cmd)

    def list_project_files(self, workdir, name):
        out, _, _ = self._run(f"find {workdir}/{name} -type f ! -path '*/.git/*'")
        return out

    def remove_workdir(self, workdir):
        return self._run(f"rm -rf {workdir}")
