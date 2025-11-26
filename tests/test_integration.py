"""Integration tests for the HeyGen API client.

These tests make real API calls to the HeyGen API.
Requires HEYGEN_API_KEY environment variable to be set.
"""

import pytest

from heygen_mcp.client import HeyGenApiClient
from heygen_mcp.models import (
    MCPAssetListResponse,
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
)


class TestGetRemainingCredits:
    """Integration tests for get_remaining_credits."""

    @pytest.mark.asyncio
    async def test_get_remaining_credits(self, api_client: HeyGenApiClient):
        """Test retrieving remaining credits from the API."""
        result = await api_client.get_remaining_credits()

        assert isinstance(result, MCPGetCreditsResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.remaining_credits is not None
        assert result.remaining_credits >= 0
        print(f"\n  Remaining credits: {result.remaining_credits}")


class TestGetVoices:
    """Integration tests for get_voices."""

    @pytest.mark.asyncio
    async def test_get_voices(self, api_client: HeyGenApiClient):
        """Test retrieving available voices from the API."""
        result = await api_client.get_voices()

        assert isinstance(result, MCPVoicesResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.voices is not None
        assert len(result.voices) > 0
        print(f"\n  Found {len(result.voices)} voices")

        # Check first voice has expected fields
        first_voice = result.voices[0]
        assert first_voice.voice_id is not None
        assert first_voice.name is not None
        assert first_voice.language is not None
        print(f"  First voice: {first_voice.name} ({first_voice.language})")


class TestAvatarGroups:
    """Integration tests for avatar group operations."""

    @pytest.mark.asyncio
    async def test_list_avatar_groups_private(self, api_client: HeyGenApiClient):
        """Test listing private avatar groups."""
        result = await api_client.list_avatar_groups(include_public=False)

        assert isinstance(result, MCPAvatarGroupResponse)
        assert result.error is None, f"API returned error: {result.error}"
        # Private groups may be empty, that's okay
        print(f"\n  Found {result.total_count} private avatar groups")

    @pytest.mark.asyncio
    async def test_list_avatar_groups_with_public(self, api_client: HeyGenApiClient):
        """Test listing avatar groups including public ones."""
        result = await api_client.list_avatar_groups(include_public=True)

        assert isinstance(result, MCPAvatarGroupResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.avatar_groups is not None
        assert result.total_count is not None
        assert result.total_count >= 0
        print(f"\n  Found {result.total_count} total avatar groups (including public)")

        if result.avatar_groups and len(result.avatar_groups) > 0:
            first_group = result.avatar_groups[0]
            assert first_group.id is not None
            assert first_group.name is not None
            print(f"  First group: {first_group.name} (id: {first_group.id})")


class TestAvatarsInGroup:
    """Integration tests for getting avatars in a group."""

    @pytest.mark.asyncio
    async def test_get_avatars_in_group(self, api_client: HeyGenApiClient):
        """Test retrieving avatars from a specific group."""
        # First get a group to use
        groups_result = await api_client.list_avatar_groups(include_public=True)

        if not groups_result.avatar_groups or len(groups_result.avatar_groups) == 0:
            pytest.skip("No avatar groups available to test")

        group_id = groups_result.avatar_groups[0].id
        result = await api_client.get_avatars_in_group(group_id)

        assert isinstance(result, MCPAvatarsInGroupResponse)
        assert result.error is None, f"API returned error: {result.error}"
        avatar_count = len(result.avatars) if result.avatars else 0
        print(f"\n  Found {avatar_count} avatars in group {group_id}")

        if result.avatars and len(result.avatars) > 0:
            first_avatar = result.avatars[0]
            assert first_avatar.avatar_id is not None
            assert first_avatar.avatar_name is not None
            print(f"  First avatar: {first_avatar.avatar_name}")
            print(f"    ID: {first_avatar.avatar_id}")


class TestVideoGeneration:
    """Integration tests for video generation.

    Note: These tests are marked with a special marker because they
    consume API credits. Run with: pytest -m "video_generation"
    """

    @pytest.mark.asyncio
    @pytest.mark.video_generation
    async def test_generate_and_check_video_status(self, api_client: HeyGenApiClient):
        """Test generating a video and checking its status.

        WARNING: This test consumes API credits!
        """
        from heygen_mcp.models import (
            Character,
            Dimension,
            VideoGenerateRequest,
            VideoInput,
            Voice,
        )

        # First, get an avatar and voice to use
        groups_result = await api_client.list_avatar_groups(include_public=True)
        if not groups_result.avatar_groups:
            pytest.skip("No avatar groups available")

        avatars_result = await api_client.get_avatars_in_group(
            groups_result.avatar_groups[0].id
        )
        if not avatars_result.avatars:
            pytest.skip("No avatars available in group")

        voices_result = await api_client.get_voices()
        if not voices_result.voices:
            pytest.skip("No voices available")

        avatar_id = avatars_result.avatars[0].avatar_id
        voice_id = voices_result.voices[0].voice_id

        # Create video generation request
        request = VideoGenerateRequest(
            title="Integration Test Video",
            video_inputs=[
                VideoInput(
                    character=Character(avatar_id=avatar_id),
                    voice=Voice(
                        input_text="Hello, this is an integration test.",
                        voice_id=voice_id,
                    ),
                )
            ],
            dimension=Dimension(width=1280, height=720),
            test=True,  # Use test mode if available
        )

        # Generate video
        generate_result = await api_client.generate_avatar_video(request)

        assert isinstance(generate_result, MCPVideoGenerateResponse)
        err = generate_result.error
        assert err is None, f"API returned error: {err}"
        assert generate_result.video_id is not None
        print(f"\n  Generated video ID: {generate_result.video_id}")

        # Check video status
        status_result = await api_client.get_video_status(generate_result.video_id)

        assert isinstance(status_result, MCPVideoStatusResponse)
        assert status_result.error is None, f"API returned error: {status_result.error}"
        assert status_result.video_id == generate_result.video_id
        assert status_result.status is not None
        print(f"  Video status: {status_result.status}")


class TestVideoStatus:
    """Integration tests for video status checking."""

    @pytest.mark.asyncio
    async def test_get_video_status_invalid_id(self, api_client: HeyGenApiClient):
        """Test getting status for a non-existent video ID."""
        result = await api_client.get_video_status("invalid-video-id-12345")

        assert isinstance(result, MCPVideoStatusResponse)
        # Should return an error or a failed status
        # The API behavior may vary - it might return an error or a specific status
        print("\n  Result for invalid ID:")
        print(f"    status={result.status}, error={result.error}")


class TestListAvatars:
    """Integration tests for listing all avatars."""

    @pytest.mark.asyncio
    async def test_list_avatars(self, api_client: HeyGenApiClient):
        """Test retrieving all available avatars."""
        result = await api_client.list_avatars()

        assert isinstance(result, MCPListAvatarsResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.avatars is not None
        assert result.total_count is not None
        assert result.total_count >= 0
        print(f"\n  Found {result.total_count} total avatars")

        if result.avatars and len(result.avatars) > 0:
            first_avatar = result.avatars[0]
            assert first_avatar.avatar_id is not None
            assert first_avatar.avatar_name is not None
            print(f"  First avatar: {first_avatar.avatar_name}")
            print(f"    ID: {first_avatar.avatar_id}")


class TestAvatarDetails:
    """Integration tests for getting avatar details."""

    @pytest.mark.asyncio
    async def test_get_avatar_details(self, api_client: HeyGenApiClient):
        """Test retrieving details for a specific avatar."""
        # First get an avatar to use
        avatars_result = await api_client.list_avatars()

        if not avatars_result.avatars or len(avatars_result.avatars) == 0:
            pytest.skip("No avatars available to test")

        avatar_id = avatars_result.avatars[0].avatar_id
        result = await api_client.get_avatar_details(avatar_id)

        assert isinstance(result, MCPAvatarDetailsResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.avatar is not None
        assert result.avatar.avatar_id == avatar_id
        print(f"\n  Avatar details: {result.avatar.avatar_name}")
        print(f"  Type: {result.avatar.type}")
        print(f"  Gender: {result.avatar.gender}")

    @pytest.mark.asyncio
    async def test_get_avatar_details_invalid_id(self, api_client: HeyGenApiClient):
        """Test getting details for a non-existent avatar ID."""
        result = await api_client.get_avatar_details("invalid-avatar-id-12345")

        assert isinstance(result, MCPAvatarDetailsResponse)
        # Should return an error
        print(f"\n  Result for invalid ID: error={result.error}")


class TestListTemplates:
    """Integration tests for listing templates."""

    @pytest.mark.asyncio
    async def test_list_templates(self, api_client: HeyGenApiClient):
        """Test retrieving templates."""
        result = await api_client.list_templates()

        assert isinstance(result, MCPListTemplatesResponse)
        assert result.error is None, f"API returned error: {result.error}"
        # Templates may be empty for accounts without custom templates
        print(f"\n  Found {result.total_count} templates")

        if result.templates and len(result.templates) > 0:
            first_template = result.templates[0]
            assert first_template.template_id is not None
            assert first_template.name is not None
            print(f"  First template: {first_template.name}")
            print(f"    ID: {first_template.template_id}")


class TestUserInfo:
    """Integration tests for getting user information."""

    @pytest.mark.asyncio
    async def test_get_user_info(self, api_client: HeyGenApiClient):
        """Test retrieving current user information."""
        result = await api_client.get_user_info()

        assert isinstance(result, MCPUserInfoResponse)
        assert result.error is None, f"API returned error: {result.error}"
        # User info fields may vary
        print(f"\n  Username: {result.username}")
        print(f"  Email: {result.email}")
        print(f"  Name: {result.first_name} {result.last_name}")


class TestTemplateDetails:
    """Integration tests for getting template details."""

    @pytest.mark.asyncio
    async def test_get_template_details(self, api_client: HeyGenApiClient):
        """Test retrieving template details."""
        # First get a template to use
        templates_result = await api_client.list_templates()

        if not templates_result.templates or len(templates_result.templates) == 0:
            pytest.skip("No templates available to test")

        template_id = templates_result.templates[0].template_id
        result = await api_client.get_template_details(template_id)

        assert isinstance(result, MCPTemplateDetailsResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.template is not None
        print(f"\n  Template: {result.template.name}")
        print(f"  Variables: {result.template.variables}")
        if result.template.scenes:
            print(f"  Scenes: {len(result.template.scenes)}")

    @pytest.mark.asyncio
    async def test_get_template_details_invalid_id(self, api_client: HeyGenApiClient):
        """Test getting details for a non-existent template ID."""
        result = await api_client.get_template_details("invalid-template-id-12345")

        assert isinstance(result, MCPTemplateDetailsResponse)
        # Should return an error
        print(f"\n  Result for invalid ID: error={result.error}")


class TestGenerateVideoFromTemplate:
    """Integration tests for generating video from template.

    Note: These tests are marked with a special marker because they
    consume API credits. Run with: pytest -m "video_generation"
    """

    @pytest.mark.asyncio
    @pytest.mark.video_generation
    async def test_generate_video_from_template(self, api_client: HeyGenApiClient):
        """Test generating a video from a template.

        WARNING: This test consumes API credits!
        """
        # First get a template to use
        templates_result = await api_client.list_templates()

        if not templates_result.templates or len(templates_result.templates) == 0:
            pytest.skip("No templates available to test")

        template_id = templates_result.templates[0].template_id

        # Get template details to see variables
        details_result = await api_client.get_template_details(template_id)
        if details_result.error:
            pytest.skip(f"Could not get template details: {details_result.error}")

        # Generate video (with test mode if available)
        result = await api_client.generate_video_from_template(
            template_id=template_id,
            title="Integration Test Video from Template",
            test=True,  # Use test mode if available
        )

        assert isinstance(result, MCPTemplateVideoGenerateResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.video_id is not None
        print(f"\n  Generated video ID: {result.video_id}")


class TestListAssets:
    """Integration tests for list_assets."""

    @pytest.mark.asyncio
    async def test_list_assets(self, api_client: HeyGenApiClient):
        """Test listing assets from the API."""
        result = await api_client.list_assets()

        assert isinstance(result, MCPAssetListResponse)
        assert result.error is None, f"API returned error: {result.error}"
        assert result.assets is not None
        print(f"\n  Total assets: {len(result.assets)}")
        if result.assets:
            print(f"  First asset ID: {result.assets[0].asset_id}")
