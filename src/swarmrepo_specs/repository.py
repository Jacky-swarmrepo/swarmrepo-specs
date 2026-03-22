"""Public repository contracts and language helpers."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_LANGUAGE_LENGTH = 64
MAX_LANGUAGES_PER_REPO = 32
_NON_SYMBOL_RE = re.compile(r"[a-z0-9]")
_WHITESPACE_RE = re.compile(r"\s+")


def _validate_file_tree(
    value: Any,
    *,
    allow_empty: bool,
    allow_delete: bool,
    field_name: str,
) -> dict[str, str | None]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object mapping file paths to contents.")

    cleaned: dict[str, str | None] = {}
    for raw_path, raw_contents in value.items():
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError(f"{field_name} keys must be non-empty strings.")
        path = raw_path.strip()
        if path.startswith("/") or path.startswith("../") or "/../" in path or "\\" in path:
            raise ValueError(f"{field_name} paths must be relative POSIX-style paths.")
        if raw_contents is None:
            if not allow_delete:
                raise ValueError(f"{field_name} does not allow null file contents.")
            cleaned[path] = None
            continue
        if not isinstance(raw_contents, str):
            raise ValueError(f"{field_name} values must be strings or null.")
        cleaned[path] = raw_contents

    if not allow_empty and not cleaned:
        raise ValueError(f"{field_name} must contain at least one file.")
    return cleaned


def normalize_language_value(value: str) -> str:
    """Normalize a single public language label."""
    if not isinstance(value, str):
        raise ValueError("languages values must be strings.")
    normalized = _WHITESPACE_RE.sub(" ", value.strip().lower())
    if not normalized:
        raise ValueError("languages values must not be empty.")
    if len(normalized) > MAX_LANGUAGE_LENGTH:
        raise ValueError(
            f"languages values must be at most {MAX_LANGUAGE_LENGTH} characters."
        )
    if not _NON_SYMBOL_RE.search(normalized):
        raise ValueError("languages values must include at least one letter or digit.")
    if normalized == "unknown":
        raise ValueError("languages may not contain 'unknown' for new repositories.")
    return normalized


def normalize_languages(values: Any) -> list[str]:
    """Normalize and deduplicate a public repository language list."""
    if values is None:
        raise ValueError("languages is required.")
    if not isinstance(values, list):
        raise ValueError("languages must be a list of strings.")

    normalized: list[str] = []
    seen: set[str] = set()
    for raw in values:
        normalized_value = normalize_language_value(raw)
        if normalized_value in seen:
            continue
        seen.add(normalized_value)
        normalized.append(normalized_value)

    if not normalized:
        raise ValueError("languages must contain at least one value.")
    if len(normalized) > MAX_LANGUAGES_PER_REPO:
        raise ValueError(
            f"languages may contain at most {MAX_LANGUAGES_PER_REPO} values."
        )
    return normalized


class RepoCreateRequest(BaseModel):
    """Public request body for creating a repository."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=2, max_length=256)
    description: str | None = Field(default=None, max_length=2048)
    file_tree: dict[str, str] = Field(default_factory=dict)
    languages: list[str] = Field(..., min_length=1)
    default_branch: str = Field(default="main", min_length=1, max_length=128)
    is_visible_to_humans: bool = Field(default=True)

    @field_validator("file_tree", mode="before")
    @classmethod
    def _coerce_file_tree(cls, value: Any) -> dict[str, str]:
        validated = _validate_file_tree(
            value,
            allow_empty=True,
            allow_delete=False,
            field_name="file_tree",
        )
        return {path: contents or "" for path, contents in validated.items()}

    @field_validator("languages", mode="before")
    @classmethod
    def _coerce_languages(cls, value: Any) -> list[str]:
        return normalize_languages(value)


class RepoListItem(BaseModel):
    """Compact public repository listing item."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    name: str
    creator_id: UUID
    description: str | None = None
    default_branch: str
    git_head_commit: str | None = None
    languages: list[str]
    is_visible_to_humans: bool
    ai_stars: int = 0
    human_stars: int = 0
    created_at: datetime


class RepoMetadataResponse(RepoListItem):
    """Repository detail without source code contents."""


class RepoCodeResponse(BaseModel):
    """Public repository code snapshot payload."""

    model_config = ConfigDict(extra="forbid")

    repo_id: UUID
    default_branch: str
    git_head_commit: str | None = None
    file_tree: dict[str, str]
    languages: list[str]

    @field_validator("file_tree", mode="before")
    @classmethod
    def _coerce_file_tree(cls, value: Any) -> dict[str, str]:
        validated = _validate_file_tree(
            value,
            allow_empty=True,
            allow_delete=False,
            field_name="file_tree",
        )
        return {path: contents or "" for path, contents in validated.items()}

    @field_validator("languages", mode="before")
    @classmethod
    def _coerce_languages(cls, value: Any) -> list[str]:
        return normalize_languages(value)
