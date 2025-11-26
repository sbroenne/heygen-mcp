"""HeyGen MCP server module providing MCP tools for the HeyGen API."""

import argparse
import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from heygen_mcp.client import HeyGenApiClient
from heygen_mcp.models import (
    Character,
    Dimension,
    MCPAvatarDetailsResponse,
    MCPAvatarGroupResponse,
    MCPAvatarsInGroupResponse,
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
    return _api_client


# ==================== Credits & User Tools ====================


@mcp.tool(
    name="get_remaining_credits",
    description="Retrieves the remaining credits in heygen account.",
)
async def get_remaining_credits() -> MCPGetCreditsResponse:
    """Get the remaining quota for the user via HeyGen API."""
    try:
        client = await get_api_client()
        return await client.get_remaining_credits()
    except Exception as e:
        return MCPGetCreditsResponse(error=str(e))


@mcp.tool(
    name="get_voices",
    description=(
        "Retrieves a list of available voices from the HeyGen API. Results truncated "
        "to first 100 voices. Private voices generally will returned 1st."
    ),
)
async def get_voices() -> MCPVoicesResponse:
    """Get the list of available voices via HeyGen API."""
    try:
        client = await get_api_client()
        return await client.get_voices()
    except Exception as e:
        return MCPVoicesResponse(error=str(e))


@mcp.tool(
    name="get_avatar_groups",
    description=(
        "Retrieves a list of HeyGen avatar groups. By default, only private avatar "
        "groups are returned, unless include_public is set to true. Avatar groups "
        "are collections of avatars, avatar group ids cannot be used to generate "
        "videos."
    ),
)
async def get_avatar_groups(include_public: bool = False) -> MCPAvatarGroupResponse:
    """List avatar groups via HeyGen API v2/avatar_group.list endpoint."""
    try:
        client = await get_api_client()
        return await client.list_avatar_groups(include_public)
    except Exception as e:
        return MCPAvatarGroupResponse(error=str(e))


@mcp.tool(
    name="get_avatars_in_avatar_group",
    description="Retrieves a list of avatars in a specific HeyGen avatar group.",
)
async def get_avatars_in_avatar_group(group_id: str) -> MCPAvatarsInGroupResponse:
    """List avatars in a specific HeyGen avatar group via HeyGen API."""
    try:
        client = await get_api_client()
        return await client.get_avatars_in_group(group_id)
    except Exception as e:
        return MCPAvatarsInGroupResponse(error=str(e))


@mcp.tool(
    name="generate_avatar_video",
    description="Generates a new avatar video via the HeyGen API.",
)
async def generate_avatar_video(
    avatar_id: str, input_text: str, voice_id: str, title: str = ""
) -> MCPVideoGenerateResponse:
    """Generate a new avatar video using the HeyGen API."""
    try:
        # Create the request object with default values
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

        client = await get_api_client()
        return await client.generate_avatar_video(request)
    except Exception as e:
        return MCPVideoGenerateResponse(error=str(e))


@mcp.tool(
    name="get_avatar_video_status",
    description=(
        "Retrieves the status of a video generated via the HeyGen API. Video status "
        "make take several minutes to hours depending on length of video and queue "
        "time. If video is not yet complete, status be viewed later by user via "
        "https://app.heygen.com/home"
    ),
)
async def get_avatar_video_status(video_id: str) -> MCPVideoStatusResponse:
    """Retrieve the status of a video generated via the HeyGen API."""
    try:
        client = await get_api_client()
        return await client.get_video_status(video_id)
    except Exception as e:
        return MCPVideoStatusResponse(error=str(e))


@mcp.tool(
    name="list_avatars",
    description=(
        "Retrieves a list of all available avatars and talking photos (Photo Avatars) "
        "from the HeyGen API. This returns avatars independently of their groups."
    ),
)
async def list_avatars() -> MCPListAvatarsResponse:
    """List all available avatars via HeyGen API."""
    try:
        client = await get_api_client()
        return await client.list_avatars()
    except Exception as e:
        return MCPListAvatarsResponse(error=str(e))


@mcp.tool(
    name="get_avatar_details",
    description=(
        "Retrieves detailed information about a specific avatar by its ID. "
        "Includes poses and voice information if available."
    ),
)
async def get_avatar_details(avatar_id: str) -> MCPAvatarDetailsResponse:
    """Get detailed information about a specific avatar."""
    try:
        client = await get_api_client()
        return await client.get_avatar_details(avatar_id)
    except Exception as e:
        return MCPAvatarDetailsResponse(error=str(e))


@mcp.tool(
    name="list_templates",
    description=(
        "Retrieves a list of video templates created under your HeyGen account. "
        "Default templates provided by the platform are not included."
    ),
)
async def list_templates() -> MCPListTemplatesResponse:
    """List all templates via HeyGen API."""
    try:
        client = await get_api_client()
        return await client.list_templates()
    except Exception as e:
        return MCPListTemplatesResponse(error=str(e))


@mcp.tool(
    name="get_user_info",
    description="Retrieves profile information of the currently authenticated HeyGen user.",
)
async def get_user_info() -> MCPUserInfoResponse:
    """Get current user's profile information."""
    try:
        client = await get_api_client()
        return await client.get_user_info()
    except Exception as e:
        return MCPUserInfoResponse(error=str(e))


@mcp.tool(
    name="get_template_details",
    description=(
        "Retrieves detailed information about a specific template by its ID, "
        "including all variables available for replacement. For templates created "
        "in the New AI Studio, scenes with their variables are also returned."
    ),
)
async def get_template_details(template_id: str) -> MCPTemplateDetailsResponse:
    """Get detailed information about a specific template including variables."""
    try:
        client = await get_api_client()
        return await client.get_template_details(template_id)
    except Exception as e:
        return MCPTemplateDetailsResponse(error=str(e))


@mcp.tool(
    name="generate_video_from_template",
    description=(
        "Generates a video based on the specified template with variable values "
        "for replacement. Use get_template_details first to see available variables. "
        "Returns a video_id that can be used with get_avatar_video_status to check progress."
    ),
)
async def generate_video_from_template(
    template_id: str,
    variables: dict | None = None,
    title: str | None = None,
    test: bool = False,
    caption: bool = False,
) -> MCPTemplateVideoGenerateResponse:
    """Generate a video from a template with variable replacements."""
    try:
        client = await get_api_client()
        return await client.generate_video_from_template(
            template_id=template_id,
            variables=variables,
            title=title,
            test=test,
            caption=caption,
        )
    except Exception as e:
        return MCPTemplateVideoGenerateResponse(error=str(e))


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HeyGen MCP Server")
    parser.add_argument(
        "--api-key",
        help=(
            "HeyGen API key. Alternatively, set HEYGEN_API_KEY environment variable."
        ),
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
    return parser.parse_args()


def main():
    """Run the MCP server."""
    args = parse_args()

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

    mcp.run()


if __name__ == "__main__":
    main()
