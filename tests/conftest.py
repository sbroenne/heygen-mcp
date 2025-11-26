"""Pytest configuration and fixtures for heygen-mcp integration tests."""

import os

import pytest
from dotenv import load_dotenv

from heygen_mcp.client import HeyGenApiClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture
def api_key():
    """Get the real API key from environment."""
    key = os.getenv("HEYGEN_API_KEY")
    if not key:
        pytest.skip("HEYGEN_API_KEY environment variable not set")
    return key


@pytest.fixture
async def api_client(api_key):
    """Create a real HeyGenApiClient instance for integration testing."""
    client = HeyGenApiClient(api_key)
    yield client
    await client.close()
