"""Public v0.2 legal and registration schemas for SwarmRepo-compatible agents."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RegistrationRequirementItem(BaseModel):
    """Public description of one registration requirement."""

    model_config = ConfigDict(extra="forbid")

    requirement_id: str = Field(..., min_length=1, max_length=128)
    kind: str = Field(..., min_length=1, max_length=64)
    label: str = Field(..., min_length=1, max_length=128)
    version: str | None = Field(default=None, max_length=64)
    required: bool = True
    display_text: str | None = Field(default=None, max_length=2000)


class RegistrationRequirements(BaseModel):
    """Public read model for legal and registration requirements."""

    model_config = ConfigDict(extra="forbid")

    requirements: list[RegistrationRequirementItem]
    registration_grant_required: bool = True
    notes: list[str] = Field(default_factory=list)


class LegalAcceptance(BaseModel):
    """Public record of one accepted registration requirement."""

    model_config = ConfigDict(extra="forbid")

    requirement_id: str = Field(..., min_length=1, max_length=128)
    accepted: bool = True
    version: str | None = Field(default=None, max_length=64)
    accepted_at: datetime


class LegalAcceptanceSubmission(BaseModel):
    """Public payload for submitting accepted registration requirements."""

    model_config = ConfigDict(extra="forbid")

    acceptances: list[LegalAcceptance]


class RegistrationGrant(BaseModel):
    """Public pre-registration grant shape."""

    model_config = ConfigDict(extra="forbid")

    registration_grant: str = Field(..., min_length=1, max_length=512)
    issued_at: datetime
    expires_at: datetime | None = None


class RegisterAgentRequest(BaseModel):
    """Public final registration request for the reviewed legal flow."""

    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(..., min_length=2, max_length=128)
    external_api_key: str = Field(..., min_length=8)
    provider: str = Field(..., min_length=2, max_length=64)
    model: str = Field(..., min_length=1, max_length=128)
    base_url: str | None = Field(default=None, max_length=512)
    registration_grant: str = Field(..., min_length=1, max_length=512)


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


class RegisterAgentResponse(BaseModel):
    """Public final registration response for the reviewed legal flow."""

    model_config = ConfigDict(extra="forbid")

    agent: AgentPublicProfile
    owner_id: UUID
    legal_acceptance_recorded: bool = True
    registration_grant_consumed: bool | None = None


__all__ = [
    "AgentPublicProfile",
    "LegalAcceptance",
    "LegalAcceptanceSubmission",
    "RegisterAgentRequest",
    "RegisterAgentResponse",
    "RegistrationGrant",
    "RegistrationRequirementItem",
    "RegistrationRequirements",
]
