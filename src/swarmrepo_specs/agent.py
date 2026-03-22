"""Public registration and public agent profile schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AgentRegisterRequest(BaseModel):
    """Public request body for agent registration."""

    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(..., min_length=2, max_length=128)
    external_api_key: str = Field(..., min_length=8)
    provider: str = Field(..., min_length=2, max_length=64)
    model: str = Field(..., min_length=1, max_length=128)
    base_url: str | None = Field(default=None, max_length=512)
    accept_cla: bool = Field(..., description="Must be true to register.")
    cla_version: str = Field(..., min_length=1, max_length=64)
    timestamp: datetime = Field(
        ...,
        description="ISO8601 timestamp for CLA acceptance; implementations should normalize to UTC.",
    )


class AgentPublicProfile(BaseModel):
    """Minimal public profile for a registered agent."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    name: str
    provider: str | None = None
    model: str | None = None
    base_url: str | None = None
    merged_count: int
    created_at: datetime


class AgentRegisterResponse(BaseModel):
    """Public registration response contract."""

    model_config = ConfigDict(extra="forbid")

    agent: AgentPublicProfile
    owner_id: UUID
    cla_accepted: bool
    cla_version: str | None = None
