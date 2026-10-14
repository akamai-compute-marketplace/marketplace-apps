import re
from pathlib import Path

from stackscripts.models import DeployScript


class DeployScriptReader:
    """Reads deploy scripts from `deployment_scripts/linode-marketplace-<app>/<app>-deploy.sh`."""

    APP_DIR_PREFIX = "linode-marketplace-"
    STACKSCRIPT_ID_PATTERN = re.compile(r"^# STACKSCRIPT_ID:\s*(\d+)", re.MULTILINE)

    def __init__(self, deployment_dir: Path) -> None:
        self._deployment_dir = deployment_dir

    def read(self, apps: list[str] | None = None) -> list[DeployScript]:
        scripts = []
        for app_dir in sorted(self._deployment_dir.glob(f"{self.APP_DIR_PREFIX}*")):
            app = app_dir.name.removeprefix(self.APP_DIR_PREFIX)
            path = app_dir / f"{app}-deploy.sh"
            if path.is_file() and (apps is None or app in apps):
                scripts.append(self._read_script(app, path))
        return scripts

    def _read_script(self, app: str, path: Path) -> DeployScript:
        with path.open(encoding="utf-8", newline="") as file:
            content = file.read()

        match = self.STACKSCRIPT_ID_PATTERN.search(content)
        stackscript_id = int(match.group(1)) if match else None
        return DeployScript(app=app, path=path, stackscript_id=stackscript_id, content=content)
