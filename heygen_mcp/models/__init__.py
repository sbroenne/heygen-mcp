"""HeyGen API models package."""

from .avatar import (
    Avatar,
    AvatarDetails,
    AvatarDetailsResponse,
    AvatarsInGroupData,
    AvatarsInGroupResponse,
    AvatarsV2Data,
    AvatarsV2Response,
    AvatarV2,
    MCPAvatarDetailsResponse,
    MCPAvatarsInGroupResponse,
    MCPListAvatarsResponse,
)
from .avatar_group import (
    AvatarGroup,
    AvatarGroupListData,
    AvatarGroupListResponse,
    MCPAvatarGroupResponse,
)
from .base import BaseHeyGenResponse
from .template import (
    MCPListTemplatesResponse,
    MCPTemplateDetailsResponse,
    MCPTemplateVideoGenerateResponse,
    Template,
    TemplateDetails,
    TemplateDetailsResponse,
    TemplateScene,
    TemplatesData,
    TemplatesResponse,
    TemplateVariable,
    TemplateVideoGenerateData,
    TemplateVideoGenerateRequest,
    TemplateVideoGenerateResponse,
)
from .user import (
    MCPGetCreditsResponse,
    MCPUserInfoResponse,
    QuotaDetails,
    RemainingQuota,
    RemainingQuotaResponse,
    UserInfo,
    UserInfoData,
    UserInfoResponse,
)
from .video import (
    Character,
    Dimension,
    MCPVideoGenerateResponse,
    MCPVideoStatusResponse,
    VideoGenerateRequest,
    VideoGenerateResponse,
    VideoInput,
    VideoStatusData,
    VideoStatusError,
    VideoStatusResponse,
    Voice,
)
from .voice import (
    MCPVoicesResponse,
    VoiceInfo,
    VoicesData,
    VoicesResponse,
)

__all__ = [
    # Base
    "BaseHeyGenResponse",
    # Voice
    "VoiceInfo",
    "VoicesData",
    "VoicesResponse",
    "MCPVoicesResponse",
    # Avatar
    "Avatar",
    "AvatarV2",
    "AvatarDetails",
    "AvatarsInGroupData",
    "AvatarsInGroupResponse",
    "AvatarsV2Data",
    "AvatarsV2Response",
    "AvatarDetailsResponse",
    "MCPAvatarsInGroupResponse",
    "MCPListAvatarsResponse",
    "MCPAvatarDetailsResponse",
    # Avatar Group
    "AvatarGroup",
    "AvatarGroupListData",
    "AvatarGroupListResponse",
    "MCPAvatarGroupResponse",
    # Video
    "Character",
    "Voice",
    "VideoInput",
    "Dimension",
    "VideoGenerateRequest",
    "VideoGenerateResponse",
    "VideoStatusError",
    "VideoStatusData",
    "VideoStatusResponse",
    "MCPVideoGenerateResponse",
    "MCPVideoStatusResponse",
    # Template
    "Template",
    "TemplateVariable",
    "TemplateScene",
    "TemplateDetails",
    "TemplatesData",
    "TemplatesResponse",
    "TemplateDetailsResponse",
    "TemplateVideoGenerateRequest",
    "TemplateVideoGenerateData",
    "TemplateVideoGenerateResponse",
    "MCPListTemplatesResponse",
    "MCPTemplateDetailsResponse",
    "MCPTemplateVideoGenerateResponse",
    # User
    "QuotaDetails",
    "RemainingQuota",
    "RemainingQuotaResponse",
    "UserInfo",
    "UserInfoData",
    "UserInfoResponse",
    "MCPGetCreditsResponse",
    "MCPUserInfoResponse",
]
