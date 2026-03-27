"""Public agent profile plus legacy CLA-first compatibility schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .registration import (
    AgentPublicProfile,
    LegalAcceptance,
    LegalAcceptanceSubmission,
    RegisterAgentRequest,
    RegisterAgentResponse,
    RegistrationGrant,
    RegistrationRequirementItem,
    RegistrationRequirements,
)


class AgentRegisterRequest(BaseModel):
    """Deprecated phase-1 CLA-first registration request."""

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


class AgentRegisterResponse(BaseModel):
    """Deprecated phase-1 CLA-first registration response contract."""

    model_config = ConfigDict(extra="forbid")

    agent: AgentPublicProfile
    owner_id: UUID
    cla_accepted: bool
    cla_version: str | None = None
