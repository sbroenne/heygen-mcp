"""HeyGen MCP server module providing MCP tools for the HeyGen API."""

import argparse
import logging
import os
import sys
from typing import Literal

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from heygen_mcp.client import HeyGenApiClient
from heygen_mcp.models import (
    Character,
    Dimension,
    MCPAssetDeleteResponse,
    MCPAssetListResponse,
    MCPAssetUploadResponse,
    MCPAvatarDetailsResponse,
    MCPAvatarGroupResponse,
    MCPAvatarsInGroupResponse,
    MCPFolderCreateResponse,
    MCPFolderListResponse,
    MCPFolderRestoreResponse,
    MCPFolderTrashResponse,
    MCPFolderUpdateResponse,
    MCPGetCreditsResponse,
    MCPListAvatarsResponse,
    MCPListTemplatesResponse,
    MCPTemplateDetailsResponse,
    MCPTemplateVideoGenerateResponse,
    MCPUserInfoResponse,
    MCPVideoGenerateResponse,
    MCPVideoStatusResponse,
    MCPVoicesResponse,
    VideoGenerateRequest,
    VideoInput,
    Voice,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("heygen_mcp")

# Load environment variables
load_dotenv()

# Create MCP server instance
mcp = FastMCP("HeyGen MCP")
_api_client: HeyGenApiClient | None = None


async def get_api_client() -> HeyGenApiClient:
    """Get or create the API client singleton.

    Returns:
        HeyGenApiClient instance.

    Raises:
        ValueError: If HEYGEN_API_KEY environment variable is not set.
    """
    global _api_client

    if _api_client is not None:
        return _api_client

    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        raise ValueError("HEYGEN_API_KEY environment variable not set.")

    _api_client = HeyGenApiClient(api_key)
    logger.info("HeyGen API client initialized")
    return _api_client


async def reset_api_client() -> None:
    """Reset the API client singleton. Used for testing."""
    global _api_client
    if _api_client is not None:
        await _api_client.close()
        _api_client = None


# ==================== User Resource ====================


@mcp.tool(
    name="user",
    description=(
        "Manage HeyGen user account. Actions: "
        "'info' - get user profile information; "
        "'credits' - get remaining credits/quota."
    ),
)
async def user(
    action: Literal["info", "credits"],
) -> MCPUserInfoResponse | MCPGetCreditsResponse:
    """Manage user account information and credits."""
    logger.info(f"user action={action}")
    try:
        client = await get_api_client()

        if action == "info":
            return await client.get_user_info()
        elif action == "credits":
            return await client.get_remaining_credits()
        else:
            return MCPUserInfoResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"user action={action} error: {e}")
        if action == "credits":
            return MCPGetCreditsResponse(error=str(e))
        return MCPUserInfoResponse(error=str(e))


# ==================== Voices Resource ====================


@mcp.tool(
    name="voices",
    description=(
        "Manage HeyGen voices. Actions: "
        "'list' - get available voices (max 100, private voices first)."
    ),
)
async def voices(
    action: Literal["list"],
) -> MCPVoicesResponse:
    """Manage voice resources."""
    logger.info(f"voices action={action}")
    try:
        client = await get_api_client()

        if action == "list":
            return await client.get_voices()
        else:
            return MCPVoicesResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"voices action={action} error: {e}")
        return MCPVoicesResponse(error=str(e))


# ==================== Avatars Resource ====================


@mcp.tool(
    name="avatars",
    description=(
        "Manage HeyGen avatars and avatar groups. Actions: "
        "'list' - get all avatars and talking photos; "
        "'get' - get details for a specific avatar (requires avatar_id); "
        "'list_groups' - get avatar groups (set include_public=true for public); "
        "'list_in_group' - get avatars in a specific group (requires group_id)."
    ),
)
async def avatars(
    action: Literal["list", "get", "list_groups", "list_in_group"],
    avatar_id: str | None = None,
    group_id: str | None = None,
    include_public: bool = False,
) -> (
    MCPListAvatarsResponse
    | MCPAvatarDetailsResponse
    | MCPAvatarGroupResponse
    | MCPAvatarsInGroupResponse
):
    """Manage avatar resources."""
    logger.info(f"avatars action={action} avatar_id={avatar_id} group_id={group_id}")
    try:
        client = await get_api_client()

        if action == "list":
            return await client.list_avatars()

        elif action == "get":
            if not avatar_id:
                return MCPAvatarDetailsResponse(
                    error="avatar_id is required for 'get' action"
                )
            return await client.get_avatar_details(avatar_id)

        elif action == "list_groups":
            return await client.list_avatar_groups(include_public)

        elif action == "list_in_group":
            if not group_id:
                return MCPAvatarsInGroupResponse(
                    error="group_id is required for 'list_in_group' action"
                )
            return await client.get_avatars_in_group(group_id)

        else:
            return MCPListAvatarsResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"avatars action={action} error: {e}")
        return MCPListAvatarsResponse(error=str(e))


# ==================== Videos Resource ====================


@mcp.tool(
    name="videos",
    description=(
        "Manage HeyGen video generation. Actions: "
        "'generate' - create a new avatar video (requires avatar_id, input_text, "
        "voice_id; optional title); "
        "'status' - check video status (requires video_id). "
        "Note: Video processing may take minutes to hours."
    ),
)
async def videos(
    action: Literal["generate", "status"],
    video_id: str | None = None,
    avatar_id: str | None = None,
    input_text: str | None = None,
    voice_id: str | None = None,
    title: str = "",
) -> MCPVideoGenerateResponse | MCPVideoStatusResponse:
    """Manage video generation and status."""
    logger.info(f"videos action={action} video_id={video_id} avatar_id={avatar_id}")
    try:
        client = await get_api_client()

        if action == "generate":
            if not avatar_id:
                return MCPVideoGenerateResponse(
                    error="avatar_id is required for 'generate' action"
                )
            if not input_text:
                return MCPVideoGenerateResponse(
                    error="input_text is required for 'generate' action"
                )
            if not voice_id:
                return MCPVideoGenerateResponse(
                    error="voice_id is required for 'generate' action"
                )

            request = VideoGenerateRequest(
                title=title,
                video_inputs=[
                    VideoInput(
                        character=Character(avatar_id=avatar_id),
                        voice=Voice(input_text=input_text, voice_id=voice_id),
                    )
                ],
                dimension=Dimension(width=1280, height=720),
            )
            return await client.generate_avatar_video(request)

        elif action == "status":
            if not video_id:
                return MCPVideoStatusResponse(
                    error="video_id is required for 'status' action"
                )
            return await client.get_video_status(video_id)

        else:
            return MCPVideoGenerateResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"videos action={action} error: {e}")
        if action == "status":
            return MCPVideoStatusResponse(error=str(e))
        return MCPVideoGenerateResponse(error=str(e))


# ==================== Templates Resource ====================


@mcp.tool(
    name="templates",
    description=(
        "Manage HeyGen video templates. Actions: "
        "'list' - get all templates in your account; "
        "'get' - get template details including variables (requires template_id); "
        "'generate' - create video from template (requires template_id; optional "
        "variables dict, title, test mode, caption)."
    ),
)
async def templates(
    action: Literal["list", "get", "generate"],
    template_id: str | None = None,
    variables: dict | None = None,
    title: str | None = None,
    test: bool = False,
    caption: bool = False,
) -> (
    MCPListTemplatesResponse
    | MCPTemplateDetailsResponse
    | MCPTemplateVideoGenerateResponse
):
    """Manage template resources and template-based video generation."""
    logger.info(f"templates action={action} template_id={template_id}")
    try:
        client = await get_api_client()

        if action == "list":
            return await client.list_templates()

        elif action == "get":
            if not template_id:
                return MCPTemplateDetailsResponse(
                    error="template_id is required for 'get' action"
                )
            return await client.get_template_details(template_id)

        elif action == "generate":
            if not template_id:
                return MCPTemplateVideoGenerateResponse(
                    error="template_id is required for 'generate' action"
                )
            return await client.generate_video_from_template(
                template_id=template_id,
                variables=variables,
                title=title,
                test=test,
                caption=caption,
            )

        else:
            return MCPListTemplatesResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"templates action={action} error: {e}")
        return MCPListTemplatesResponse(error=str(e))


# ==================== Assets Resource ====================


@mcp.tool(
    name="assets",
    description=(
        "Manage HeyGen media assets. Actions: "
        "'list' - get all assets (images, videos, audios); "
        "'upload' - upload a media file (requires file_path), returns asset_id; "
        "'delete' - remove an asset (requires asset_id)."
    ),
)
async def assets(
    action: Literal["list", "upload", "delete"],
    file_path: str | None = None,
    asset_id: str | None = None,
) -> MCPAssetListResponse | MCPAssetUploadResponse | MCPAssetDeleteResponse:
    """Manage media asset resources."""
    logger.info(f"assets action={action} file_path={file_path} asset_id={asset_id}")
    try:
        client = await get_api_client()

        if action == "list":
            return await client.list_assets()

        elif action == "upload":
            if not file_path:
                return MCPAssetUploadResponse(
                    error="file_path is required for 'upload' action"
                )
            return await client.upload_asset(file_path)

        elif action == "delete":
            if not asset_id:
                return MCPAssetDeleteResponse(
                    error="asset_id is required for 'delete' action",
                    success=False,
                )
            return await client.delete_asset(asset_id)

        else:
            return MCPAssetListResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"assets action={action} error: {e}")
        if action == "upload":
            return MCPAssetUploadResponse(error=str(e))
        if action == "delete":
            return MCPAssetDeleteResponse(error=str(e), success=False)
        return MCPAssetListResponse(error=str(e))


# ==================== Folders Resource ====================


@mcp.tool(
    name="folders",
    description=(
        "Manage HeyGen folders for organizing videos and assets. Actions: "
        "'list' - get all folders in your account; "
        "'create' - create a new folder (requires name); "
        "'rename' - rename an existing folder (requires folder_id and name); "
        "'trash' - move a folder to trash (requires folder_id); "
        "'restore' - restore a folder from trash (requires folder_id)."
    ),
)
async def folders(
    action: Literal["list", "create", "rename", "trash", "restore"],
    folder_id: str | None = None,
    name: str | None = None,
) -> (
    MCPFolderListResponse
    | MCPFolderCreateResponse
    | MCPFolderUpdateResponse
    | MCPFolderTrashResponse
    | MCPFolderRestoreResponse
):
    """Manage folder resources for organizing content."""
    logger.info(f"folders action={action} folder_id={folder_id} name={name}")
    try:
        client = await get_api_client()

        if action == "list":
            return await client.list_folders()

        elif action == "create":
            if not name:
                return MCPFolderCreateResponse(
                    error="name is required for 'create' action"
                )
            return await client.create_folder(name)

        elif action == "rename":
            if not folder_id:
                return MCPFolderUpdateResponse(
                    error="folder_id is required for 'rename' action",
                    success=False,
                )
            if not name:
                return MCPFolderUpdateResponse(
                    error="name is required for 'rename' action",
                    success=False,
                )
            return await client.update_folder(folder_id, name)

        elif action == "trash":
            if not folder_id:
                return MCPFolderTrashResponse(
                    error="folder_id is required for 'trash' action",
                    success=False,
                )
            return await client.trash_folder(folder_id)

        elif action == "restore":
            if not folder_id:
                return MCPFolderRestoreResponse(
                    error="folder_id is required for 'restore' action",
                    success=False,
                )
            return await client.restore_folder(folder_id)

        else:
            return MCPFolderListResponse(error=f"Unknown action: {action}")

    except Exception as e:
        logger.error(f"folders action={action} error: {e}")
        if action == "create":
            return MCPFolderCreateResponse(error=str(e))
        if action == "rename":
            return MCPFolderUpdateResponse(error=str(e), success=False)
        if action == "trash":
            return MCPFolderTrashResponse(error=str(e), success=False)
        if action == "restore":
            return MCPFolderRestoreResponse(error=str(e), success=False)
        return MCPFolderListResponse(error=str(e))


# ==================== CLI ====================


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HeyGen MCP Server")
    parser.add_argument(
        "--api-key",
        help="HeyGen API key. Or set HEYGEN_API_KEY environment variable.",
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind the server to."
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to."
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser.parse_args()


def main():
    """Run the MCP server."""
    args = parse_args()

    # Configure debug logging if requested
    if args.debug:
        logging.getLogger("heygen_mcp").setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Check if API key is provided or in environment
    if args.api_key:
        os.environ["HEYGEN_API_KEY"] = args.api_key

    # Verify API key is set
    if not os.getenv("HEYGEN_API_KEY"):
        print("ERROR: HeyGen API key not provided.")
        print(
            "Please set it using --api-key or the HEYGEN_API_KEY environment variable."
        )
        sys.exit(1)

    logger.info("Starting HeyGen MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
