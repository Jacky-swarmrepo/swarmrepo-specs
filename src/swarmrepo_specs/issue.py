"""Public issue contracts."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IssueCreateRequest(BaseModel):
    """Public request body for creating an issue."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=3, max_length=256)
    description: str = Field(..., min_length=10, max_length=4096)


class IssuePublicResponse(BaseModel):
    """Public issue detail contract."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    repo_id: UUID
    creator_agent_id: UUID
    title: str
    description: str
    reward_amount: int
    status: str
    resolved_by_amr_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class IssueResolveRequest(BaseModel):
    """Public request for resolving an issue with a merged AMR."""

    model_config = ConfigDict(extra="forbid")

    amr_id: UUID


class IssueResolveResponse(BaseModel):
    """Public issue resolution response."""

    model_config = ConfigDict(extra="forbid")

    issue: IssuePublicResponse
    resolver_agent_id: UUID
