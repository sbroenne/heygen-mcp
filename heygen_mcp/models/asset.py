"""HeyGen Asset API models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseHeyGenResponse


class Asset(BaseModel):
    """Represents a HeyGen asset (image, video, or audio)."""

    model_config = {"extra": "ignore"}

    asset_id: str = Field(..., description="Unique identifier for the asset")
    asset_key: Optional[str] = Field(None, description="Asset key/path")
    url: Optional[str] = Field(None, description="URL to access the asset")
    type: Optional[str] = Field(None, description="Asset type (image, video, audio)")
    file_name: Optional[str] = Field(None, description="Original file name")
    file_type: Optional[str] = Field(None, description="File MIME type")
    size: Optional[int] = Field(None, description="File size in bytes")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    width: Optional[int] = Field(None, description="Width in pixels")
    height: Optional[int] = Field(None, description="Height in pixels")
    duration: Optional[float] = Field(None, description="Duration in seconds")


class AssetUploadData(BaseModel):
    """Response data from asset upload."""

    model_config = {"extra": "ignore"}

    asset_id: Optional[str] = Field(None, description="ID of the uploaded asset")
    url: Optional[str] = Field(None, description="URL to access the uploaded asset")


class AssetUploadResponse(BaseModel):
    """API response for asset upload."""

    model_config = {"extra": "ignore"}

    code: Optional[int] = Field(None, description="Response code")
    data: Optional[AssetUploadData] = Field(None, description="Upload response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if any")


class AssetListData(BaseModel):
    """Response data from list assets."""

    model_config = {"extra": "ignore"}

    assets: List[Asset] = Field(default_factory=list, description="List of assets")
    total: Optional[int] = Field(None, description="Total number of assets")
    page: Optional[int] = Field(None, description="Current page number")
    page_size: Optional[int] = Field(None, description="Items per page")


class AssetListResponse(BaseModel):
    """API response for listing assets."""

    model_config = {"extra": "ignore"}

    code: Optional[int] = Field(None, description="Response code")
    data: Optional[AssetListData] = Field(None, description="List response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if any")


class AssetDeleteResponse(BaseModel):
    """API response for deleting an asset."""

    model_config = {"extra": "ignore"}

    code: Optional[int] = Field(None, description="Response code")
    data: Optional[Dict[str, Any]] = Field(None, description="Delete response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if any")


# MCP Response models


class MCPAssetUploadResponse(BaseHeyGenResponse):
    """MCP response for asset upload."""

    asset_id: Optional[str] = Field(None, description="ID of the uploaded asset")
    url: Optional[str] = Field(None, description="URL to access the uploaded asset")


class MCPAssetListResponse(BaseHeyGenResponse):
    """MCP response for listing assets."""

    assets: List[Asset] = Field(default_factory=list, description="List of assets")
    total: Optional[int] = Field(None, description="Total number of assets")


class MCPAssetDeleteResponse(BaseHeyGenResponse):
    """MCP response for deleting an asset."""

    success: bool = Field(False, description="Whether the deletion was successful")
    asset_id: Optional[str] = Field(None, description="ID of the deleted asset")
