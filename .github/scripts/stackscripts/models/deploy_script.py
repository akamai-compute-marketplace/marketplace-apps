from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DeployScript:
    """An app's deploy script as stored in the repository."""

    app: str
    path: Path
    stackscript_id: int | None
    content: str
