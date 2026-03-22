"""Public AMR and verdict contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _validate_file_changes(value: Any) -> dict[str, str | None]:
    if value is None or not isinstance(value, dict):
        raise ValueError("proposed_file_changes must be an object mapping file paths to contents.")

    cleaned: dict[str, str | None] = {}
    for raw_path, raw_contents in value.items():
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError("proposed_file_changes keys must be non-empty strings.")
        path = raw_path.strip()
        if path.startswith("/") or path.startswith("../") or "/../" in path or "\\" in path:
            raise ValueError("proposed_file_changes paths must be relative POSIX-style paths.")
        if raw_contents is not None and not isinstance(raw_contents, str):
            raise ValueError("proposed_file_changes values must be strings or null.")
        cleaned[path] = raw_contents

    if not cleaned:
        raise ValueError("proposed_file_changes must contain at least one file.")
    return cleaned


class AMRSubmitRequest(BaseModel):
    """Public request body for creating an AMR."""

    model_config = ConfigDict(extra="forbid")

    provider: str | None = Field(default=None, min_length=2, max_length=64)
    model_version: str | None = Field(default=None, min_length=1, max_length=128)
    proposed_file_changes: dict[str, str | None] = Field(..., min_length=1)
    issue_id: UUID | None = None
    test_cases: dict | list | str | None = None

    @field_validator("proposed_file_changes", mode="before")
    @classmethod
    def _coerce_file_changes(cls, value: Any) -> dict[str, str | None]:
        return _validate_file_changes(value)


class AMRResponse(BaseModel):
    """Public AMR detail contract."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    repo_id: UUID
    contributor_id: UUID
    provider: str
    model_version: str
    proposed_file_changes: dict[str, str | None]
    issue_id: UUID | None = None
    status: str
    score: float | None = None
    created_at: datetime

    @field_validator("proposed_file_changes", mode="before")
    @classmethod
    def _coerce_file_changes(cls, value: Any) -> dict[str, str | None]:
        return _validate_file_changes(value)


class AMRListItem(BaseModel):
    """Compact public AMR listing item."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    repo_id: UUID
    contributor_id: UUID
    status: str
    score: float | None = None
    created_at: datetime


class AMRSubmitResponse(BaseModel):
    """Public AMR submission response."""

    model_config = ConfigDict(extra="forbid")

    amr: AMRResponse
    reward: int


class PendingReviewItem(BaseModel):
    """Public AMR review-queue item."""

    model_config = ConfigDict(extra="forbid")

    amr_id: UUID
    repo_id: UUID
    contributor_id: UUID
    status: str
    verdict_count: int
    created_at: datetime


class VerdictSubmitRequest(BaseModel):
    """Public verdict submission request."""

    model_config = ConfigDict(extra="forbid")

    score: float = Field(..., ge=0, le=100)
    comment: str = Field(..., min_length=2, max_length=4000)


class VerdictSubmitResponse(BaseModel):
    """Public verdict submission response."""

    model_config = ConfigDict(extra="forbid")

    amr_id: UUID
    status: str
    verdict_count: int
    required_verdicts: int
    consensus_progress: str
