"""Video generation and status models for the HeyGen API."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseHeyGenResponse


class Character(BaseModel):
    """Character configuration for video generation."""

    type: str = "avatar"
    avatar_id: str
    avatar_style: str = "normal"
    scale: float = 1.0


class Voice(BaseModel):
    """Voice configuration for video generation."""

    type: str = "text"
    input_text: str
    voice_id: str


class VideoInput(BaseModel):
    """Input configuration for a video scene."""

    character: Character
    voice: Voice


class Dimension(BaseModel):
    """Video dimension configuration."""

    width: int = 1280
    height: int = 720


class VideoGenerateRequest(BaseModel):
    """Request model for video generation."""

    title: str = ""
    video_inputs: List[VideoInput]
    test: bool = False
    callback_id: Optional[str] = None
    dimension: Dimension = Field(default_factory=lambda: Dimension())
    aspect_ratio: Optional[str] = None
    caption: bool = False


class VideoGenerateResponse(BaseHeyGenResponse):
    """API response for video generation."""

    data: Optional[Dict[str, Any]] = None


class VideoStatusError(BaseModel):
    """Error information for video status."""

    code: Optional[int] = None
    detail: Optional[str] = None
    message: Optional[str] = None


class VideoStatusData(BaseModel):
    """Video status data from API."""

    callback_id: Optional[str] = None
    caption_url: Optional[str] = None
    created_at: Optional[int] = None
    duration: Optional[float] = None
    error: Optional[VideoStatusError] = None
    gif_url: Optional[str] = None
    id: str
    status: str  # Values: "waiting", "pending", "processing", "completed", "failed"
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    video_url_caption: Optional[str] = None


class VideoStatusResponse(BaseModel):
    """API response for video status (v1 endpoint)."""

    code: int
    data: VideoStatusData
    message: str


class MCPVideoGenerateResponse(BaseHeyGenResponse):
    """MCP response wrapper for video generation."""

    video_id: Optional[str] = None
    task_id: Optional[str] = None
    video_url: Optional[str] = None
    status: Optional[str] = None


class MCPVideoStatusResponse(BaseHeyGenResponse):
    """MCP response wrapper for video status."""

    video_id: Optional[str] = None
    status: Optional[str] = None
    duration: Optional[float] = None
    video_url: Optional[str] = None
    gif_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[int] = None
    error_details: Optional[Dict[str, Any]] = None
