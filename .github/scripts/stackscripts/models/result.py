from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Self


class Status(StrEnum):

    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    MISSING_ID = "MISSING_ID"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"

    UPDATED = "UPDATED"
    FAILED = "FAILED"

    @property
    def needs_attention(self) -> bool:
        return self not in (Status.MATCH, Status.UPDATED)


@dataclass(frozen=True)
class Result:
    """Outcome of validating or updating one app's StackScript."""

    app: str
    stackscript_id: int | None
    status: Status
    detail: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            app=data["app"],
            stackscript_id=data["stackscript_id"],
            status=Status(data["status"]),
            detail=data["detail"],
        )
