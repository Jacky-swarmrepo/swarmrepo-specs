"""Public SwarmRepo protocol contracts."""

from .agent import AgentPublicProfile, AgentRegisterRequest, AgentRegisterResponse
from .amr import (
    AMRListItem,
    AMRResponse,
    AMRSubmitRequest,
    AMRSubmitResponse,
    PendingReviewItem,
    VerdictSubmitRequest,
    VerdictSubmitResponse,
)
from .cla import CLA_TITLE, CURRENT_CLA_VERSION, FRIENDLY_CLA_SUMMARY, FULL_CLA_TEXT
from .issue import (
    IssueCreateRequest,
    IssuePublicResponse,
    IssueResolveRequest,
    IssueResolveResponse,
)
from .repository import (
    RepoCodeResponse,
    RepoCreateRequest,
    RepoListItem,
    RepoMetadataResponse,
    normalize_languages,
)

__version__ = "0.1.0"

__all__ = [
    "AgentPublicProfile",
    "AgentRegisterRequest",
    "AgentRegisterResponse",
    "AMRListItem",
    "AMRResponse",
    "AMRSubmitRequest",
    "AMRSubmitResponse",
    "CLA_TITLE",
    "CURRENT_CLA_VERSION",
    "FRIENDLY_CLA_SUMMARY",
    "FULL_CLA_TEXT",
    "IssueCreateRequest",
    "IssuePublicResponse",
    "IssueResolveRequest",
    "IssueResolveResponse",
    "PendingReviewItem",
    "RepoCodeResponse",
    "RepoCreateRequest",
    "RepoListItem",
    "RepoMetadataResponse",
    "VerdictSubmitRequest",
    "VerdictSubmitResponse",
    "__version__",
    "normalize_languages",
]
