import os
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Config:
    deployment_dir: Path
    run_url: str
    slack_webhook_url: str
    stackscript_api_token: str
    github_output_path: Path | None

    @classmethod
    def from_env(cls) -> "Config":
        server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        repository = os.environ.get("GITHUB_REPOSITORY", "akamai-compute-marketplace/marketplace-apps")
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        github_output = os.environ.get("GITHUB_OUTPUT")

        return cls(
            deployment_dir=REPOSITORY_ROOT / "deployment_scripts",
            run_url=f"{server_url}/{repository}/actions/runs/{run_id}",
            slack_webhook_url=os.environ.get("SLACK_WEBHOOK_URL", ""),
            stackscript_api_token=os.environ.get("STACKSCRIPT_API_TOKEN", ""),
            github_output_path=Path(github_output) if github_output else None,
        )
