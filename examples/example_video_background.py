#!/usr/bin/env python3
"""
Example: Generate a tutorial video with screen recording background.

This script demonstrates how to:
1. Upload a screen recording as an asset
2. Generate an avatar video with the screen recording as background
3. Poll for completion and get the final video URL

Prerequisites:
- Set HEYGEN_API_KEY environment variable
- Have a screen recording video file to upload
"""

import asyncio
import os
import sys
from pathlib import Path

from heygen_mcp.client import HeyGenApiClient
from heygen_mcp.models import (
    Background,
    Character,
    Dimension,
    VideoGenerateRequest,
    VideoInput,
    Voice,
)


async def create_tutorial_video(
    api_key: str,
    screen_recording_path: str,
    avatar_id: str = "Annie_expressive6_public",
    voice_id: str = "6fa2fa767bf148fc939c0bbba7306760",
):
    """Create a tutorial video with screen recording background.

    Args:
        api_key: HeyGen API key
        screen_recording_path: Path to screen recording video file
        avatar_id: Avatar to use (default: Annie)
        voice_id: Voice to use (default: Annie's voice)

    Returns:
        str: URL of the completed video, or None if failed
    """
    async with HeyGenApiClient(api_key) as client:
        print("=" * 60)
        print("Step 1: Uploading screen recording...")
        print("=" * 60)

        # Upload the screen recording
        upload_result = await client.upload_asset(screen_recording_path)
        if upload_result.error:
            print(f"❌ Upload failed: {upload_result.error}")
            return None

        screen_recording_id = upload_result.asset_id
        print("✅ Screen recording uploaded!")
        print(f"   Asset ID: {screen_recording_id}")
        print(f"   URL: {upload_result.url}")

        print("\n" + "=" * 60)
        print("Step 2: Generating video with avatar overlay...")
        print("=" * 60)

        # Create the video generation request
        script = """
        Welcome to this tutorial on Excel pivot tables.
        In this video, I'll walk you through creating your first pivot table,
        and show you how to analyze your data more effectively.
        Let's get started!
        """

        request = VideoGenerateRequest(
            title="Excel Tutorial - Pivot Tables",
            video_inputs=[
                VideoInput(
                    character=Character(avatar_id=avatar_id, avatar_style="normal"),
                    voice=Voice(input_text=script.strip(), voice_id=voice_id),
                    background=Background(
                        type="video",
                        video_asset_id=screen_recording_id,
                        play_style="fit_to_scene",
                    ),
                )
            ],
            dimension=Dimension(width=1920, height=1080),
        )

        # Generate the video
        video_result = await client.generate_avatar_video(request)
        if video_result.error:
            print(f"❌ Video generation failed: {video_result.error}")
            return None

        video_id = video_result.video_id
        print("✅ Video generation started!")
        print(f"   Video ID: {video_id}")

        print("\n" + "=" * 60)
        print("Step 3: Waiting for video completion...")
        print("=" * 60)
        print("(This may take several minutes)")

        # Poll for completion
        last_status = None
        while True:
            status_result = await client.get_video_status(video_id)

            if status_result.status != last_status:
                print(f"\n📊 Status: {status_result.status}")
                last_status = status_result.status
            else:
                print(".", end="", flush=True)

            if status_result.status == "completed":
                print("\n\n✅ Video completed successfully!")
                print(f"   Video URL: {status_result.video_url}")
                print(f"   Duration: {status_result.duration}s")
                if status_result.thumbnail_url:
                    print(f"   Thumbnail: {status_result.thumbnail_url}")
                return status_result.video_url

            elif status_result.status == "failed":
                print("\n\n❌ Video generation failed!")
                if status_result.error_details:
                    print(f"   Error: {status_result.error_details}")
                return None

            await asyncio.sleep(10)


async def main():
    """Main entry point."""
    # Check for API key
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        print("❌ Error: HEYGEN_API_KEY environment variable not set")
        print("\nSet it using:")
        print("  export HEYGEN_API_KEY='your-api-key-here'  # Linux/Mac")
        print("  set HEYGEN_API_KEY=your-api-key-here       # Windows")
        sys.exit(1)

    # Check for screen recording path argument
    if len(sys.argv) < 2:
        print("Usage: python example_video_background.py <screen_recording.mp4>")
        print("\nExample:")
        print("  python example_video_background.py ./recordings/excel_demo.mp4")
        sys.exit(1)

    screen_recording_path = sys.argv[1]

    # Validate file exists
    if not Path(screen_recording_path).exists():
        print(f"❌ Error: File not found: {screen_recording_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎬 HeyGen Tutorial Video Generator")
    print("=" * 60)
    print(f"Screen Recording: {screen_recording_path}")
    file_size_mb = Path(screen_recording_path).stat().st_size / 1024 / 1024
    print(f"File Size: {file_size_mb:.2f} MB")
    print()

    # Create the video
    video_url = await create_tutorial_video(api_key, screen_recording_path)

    if video_url:
        print("\n" + "=" * 60)
        print("🎉 Success!")
        print("=" * 60)
        print("\nYour tutorial video is ready:")
        print(f"  {video_url}")
        print("\nYou can now:")
        print("  - Download the video")
        print("  - Share it with others")
        print("  - Use it in your tutorials")
    else:
        print("\n" + "=" * 60)
        print("❌ Failed to create video")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
