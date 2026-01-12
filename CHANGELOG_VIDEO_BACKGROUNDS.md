# Changelog - Video Background Support

## [Unreleased] - 2025-12-09

### Added - Video Background Support

#### New Features

- **Video backgrounds** in `videos` tool `generate` action
- **Color backgrounds** for green screen and solid colors
- **Image backgrounds** for static branded backgrounds
- **Video backgrounds** with multiple playback styles
- Complete background API with proper validation and error handling

#### New Parameters

Added to `videos` tool `generate` action:
- `background_type`: Background type (`"color"`, `"image"`, or `"video"`)
- `background_value`: Hex color code for color backgrounds
- `background_image_asset_id`: Asset ID for image backgrounds
- `background_video_asset_id`: Asset ID for video backgrounds
- `background_play_style`: Video playback style (`"fit_to_scene"`, `"freeze"`, `"loop"`, `"full_video"`)

#### New Models

- `Background` - Pydantic model for background configuration
- Updated `VideoInput` to include optional `background` field

#### Documentation

- Comprehensive guide: `docs/VIDEO_BACKGROUNDS.md`
- API reference with examples
- Use case scenarios and workflows
- Updated README.md with feature announcement

#### Testing

- Complete test suite in `tests/test_video_backgrounds.py`
- 19 test cases covering all background types
- Validation tests for all parameters
- Real-world use case scenarios

#### Examples

- Tutorial video generation example: `examples/example_video_background.py`
- Complete workflow demonstrating:
  - Asset upload
  - Video generation with background
  - Status polling and completion

### Use Cases Enabled

1. **Tutorial Video Production**
   - Upload screen recordings
   - Add avatar presenter overlay
   - Automated tutorial generation

2. **Product Demonstrations**
   - Demo videos with professional presenter
   - Picture-in-Picture presentations

3. **Software Training**
   - App walkthroughs with narration
   - Interactive training videos

4. **Green Screen Effects**
   - Color backgrounds for chromakey
   - Post-production compositing

5. **Branded Content**
   - Static image backgrounds with company branding
   - Professional presentation videos

### Backward Compatibility

- All background parameters are **optional**
- Existing code without backgrounds continues to work unchanged
- No breaking changes to existing API

### Technical Details

- API Endpoint: `POST /v2/video/generate`
- HeyGen Documentation: https://docs.heygen.com/docs/customize-video-background
- Implements full HeyGen background specification
- Proper error handling and validation
- Type-safe implementation with Pydantic models

### Implementation

**Files Modified:**
- `heygen_mcp/models/video.py` - Added `Background` model
- `heygen_mcp/server.py` - Extended `videos` tool with background parameters
- `heygen_mcp/models/__init__.py` - Exported `Background` model

**Files Added:**
- `docs/VIDEO_BACKGROUNDS.md` - Comprehensive feature documentation
- `tests/test_video_backgrounds.py` - Complete test suite
- `examples/example_video_background.py` - Working example script
- `CHANGELOG_VIDEO_BACKGROUNDS.md` - This changelog

### Credits

Feature request and specification provided by MCP Server Excel Tutorials Project.

### Related Issues

Closes: #[issue-number] - Video Background Support Feature Request
