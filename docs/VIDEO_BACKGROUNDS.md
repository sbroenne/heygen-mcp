# Video Background Support

## Overview

The HeyGen MCP Server now supports **video backgrounds** in the `videos` tool's `generate` action, enabling automated video compositing (screen recording + avatar overlay) without manual HeyGen Studio interaction.

## Features

Add backgrounds to avatar videos using three types:
- **Color**: Solid color backgrounds (e.g., green screen for chromakey)
- **Image**: Static image backgrounds (e.g., branded backgrounds)
- **Video**: Video backgrounds with multiple playback styles (e.g., screen recordings)

## Quick Start

### 1. Upload Video Asset

First, upload your background video (e.g., screen recording) as an asset:

```python
# Using the assets tool
result = await assets(
    action="upload",
    file_path="/path/to/screen_recording.mp4"
)
video_asset_id = result.asset_id
```

### 2. Generate Video with Background

Then generate an avatar video with the video as background:

```python
# Using the videos tool
result = await videos(
    action="generate",
    avatar_id="Annie_expressive6_public",
    voice_id="6fa2fa767bf148fc939c0bbba7306760",
    input_text="Welcome to this tutorial on Excel pivot tables.",
    title="Excel Tutorial 01",
    background_type="video",
    background_video_asset_id=video_asset_id,
    background_play_style="fit_to_scene"
)
video_id = result.video_id
```

### 3. Check Status and Download

```python
# Check video generation status
status = await videos(action="status", video_id=video_id)
if status.status == "completed":
    video_url = status.video_url
    # Download or use the video
```

## Background Types

### Color Background

Solid color backgrounds using hex color codes.

**Parameters:**
- `background_type`: `"color"`
- `background_value`: Hex color code (e.g., `"#008000"` for green screen)

**Example:**
```python
await videos(
    action="generate",
    avatar_id="Annie_expressive6_public",
    voice_id="voice_id",
    input_text="This is on green screen",
    background_type="color",
    background_value="#008000"  # Green screen
)
```

**Use Cases:**
- Green screen for chromakey compositing
- Branded color backgrounds
- Simple solid backgrounds

### Image Background

Static image backgrounds.

**Parameters:**
- `background_type`: `"image"`
- `background_image_asset_id`: Asset ID of uploaded image

**Example:**
```python
# 1. Upload image
img_result = await assets(action="upload", file_path="company_logo.png")

# 2. Use as background
await videos(
    action="generate",
    avatar_id="professional_avatar",
    voice_id="voice_id",
    input_text="Welcome to our company update",
    background_type="image",
    background_image_asset_id=img_result.asset_id
)
```

**Use Cases:**
- Branded backgrounds with company logo
- Static scene backgrounds
- Presentation slides

### Video Background

Video backgrounds with playback control.

**Parameters:**
- `background_type`: `"video"`
- `background_video_asset_id`: Asset ID of uploaded video
- `background_play_style`: (Optional) Playback style (default: `"fit_to_scene"`)

**Play Styles:**
- `"fit_to_scene"`: Scale video to fit scene duration (default)
- `"freeze"`: Freeze on last frame when video ends
- `"loop"`: Loop video until scene ends
- `"full_video"`: Use full video duration

**Example:**
```python
# 1. Upload video
vid_result = await assets(action="upload", file_path="screen_recording.mp4")

# 2. Use as background
await videos(
    action="generate",
    avatar_id="Annie_expressive6_public",
    voice_id="voice_id",
    input_text="Let me show you how this works...",
    title="Tutorial Video",
    background_type="video",
    background_video_asset_id=vid_result.asset_id,
    background_play_style="fit_to_scene"
)
```

**Use Cases:**
- Screen recordings with avatar overlay
- Tutorial videos with software demonstrations
- Picture-in-Picture presentations
- Product demos with presenter overlay

## Complete Workflow Example

### Automated Tutorial Video Production

```python
import asyncio
from heygen_mcp import get_api_client

async def create_tutorial_video():
    """Create a tutorial video with screen recording and avatar overlay."""
    
    # Step 1: Upload screen recording
    print("Uploading screen recording...")
    asset_result = await assets(
        action="upload",
        file_path="./recordings/excel_demo.mp4"
    )
    screen_recording_id = asset_result.asset_id
    print(f"Screen recording uploaded: {screen_recording_id}")
    
    # Step 2: Generate video with avatar overlay
    print("Generating video with avatar overlay...")
    video_result = await videos(
        action="generate",
        avatar_id="Annie_expressive6_public",
        voice_id="6fa2fa767bf148fc939c0bbba7306760",
        input_text=(
            "Welcome to this Excel tutorial. "
            "Today I'll show you how to create pivot tables "
            "to analyze your data effectively."
        ),
        title="Excel Tutorial - Pivot Tables",
        background_type="video",
        background_video_asset_id=screen_recording_id,
        background_play_style="fit_to_scene"
    )
    video_id = video_result.video_id
    print(f"Video generation started: {video_id}")
    
    # Step 3: Poll for completion
    print("Waiting for video to complete...")
    while True:
        status = await videos(action="status", video_id=video_id)
        print(f"Status: {status.status}")
        
        if status.status == "completed":
            print(f"Video completed: {status.video_url}")
            return status.video_url
        elif status.status == "failed":
            print(f"Video generation failed: {status.error_details}")
            return None
        
        await asyncio.sleep(10)  # Check every 10 seconds

# Run the workflow
video_url = asyncio.run(create_tutorial_video())
```

## API Parameters Reference

### videos tool - generate action

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | Yes | Must be `"generate"` |
| `avatar_id` | string | Yes | Avatar ID to use |
| `voice_id` | string | Yes | Voice ID for narration |
| `input_text` | string | Yes | Text for avatar to speak |
| `title` | string | No | Video title |
| `background_type` | string | No | Background type: `"color"`, `"image"`, or `"video"` |
| `background_value` | string | No | Hex color (required for `type="color"`) |
| `background_image_asset_id` | string | No | Image asset ID (required for `type="image"`) |
| `background_video_asset_id` | string | No | Video asset ID (required for `type="video"`) |
| `background_play_style` | string | No | Video playback style (default: `"fit_to_scene"`) |

## Tips and Best Practices

### Video Background Tips

1. **Resolution Matching**: Use screen recordings with resolution matching your target output (e.g., 1920x1080 for HD)

2. **Duration**: The avatar narration and background video should be roughly aligned:
   - `fit_to_scene`: Background speeds up/slows to match narration
   - `loop`: Good for shorter backgrounds that can repeat
   - `full_video`: Avatar narration matches full background duration

3. **File Size**: Keep video assets under 500MB for faster uploads and processing

4. **Format**: MP4 with H.264 codec is recommended for best compatibility

### Performance

- **Upload once, reuse**: Uploaded assets persist and can be reused across multiple videos
- **Async workflows**: Use async/await patterns for non-blocking operations
- **Batch processing**: Upload all assets first, then generate videos in parallel

### Error Handling

```python
try:
    result = await videos(
        action="generate",
        avatar_id="avatar_id",
        voice_id="voice_id",
        input_text="text",
        background_type="video",
        background_video_asset_id="invalid_id"
    )
    if result.error:
        print(f"Error: {result.error}")
except Exception as e:
    print(f"Exception: {e}")
```

## Backward Compatibility

The background parameters are **optional**. Existing code without backgrounds continues to work:

```python
# This still works (no background)
await videos(
    action="generate",
    avatar_id="Annie_expressive6_public",
    voice_id="voice_id",
    input_text="Hello world"
)
```

## HeyGen API Reference

This feature uses the HeyGen V2 API's background support:

- **Endpoint**: `POST /v2/video/generate`
- **Documentation**: https://docs.heygen.com/docs/customize-video-background
- **API Reference**: https://docs.heygen.com/reference/create-an-avatar-video-v2

## Use Cases

### 1. Tutorial Video Production
Record screen → Upload → Generate avatar overlay → Automated tutorial

### 2. Product Demonstrations
Demo video → Avatar presenter → Professional product showcase

### 3. Software Training
App walkthrough → Narrated by avatar → Training video

### 4. Presentation Recording
Slide recording → Avatar host → Enhanced presentation

### 5. Green Screen Compositing
Color background → Post-processing → Custom effects

## Troubleshooting

### "background_video_asset_id is required"
**Solution**: Make sure you upload the video asset first and use the returned `asset_id`

### Video not compositing correctly
**Solution**: Check that:
- Video asset uploaded successfully
- Asset ID is correct
- Play style is appropriate for your use case

### Avatar positioning
**Note**: Avatar positioning (e.g., corner placement for PiP) is controlled by the avatar style in HeyGen Studio. The MCP currently uses the default positioning.

## Future Enhancements

Potential future additions:
- Avatar positioning control (Picture-in-Picture placement)
- Custom dimensions per video
- Multi-scene support with different backgrounds
- Background effects (blur, filters)

## Support

For issues or questions:
- GitHub Issues: https://github.com/heygen-com/heygen-mcp/issues
- HeyGen Support: https://help.heygen.com/
- API Documentation: https://docs.heygen.com/
