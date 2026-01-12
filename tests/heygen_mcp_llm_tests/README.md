# HeyGen MCP LLM Tests

This directory contains LLM-based integration tests for the HeyGen MCP server using [agent-benchmark](https://github.com/mykhaliev/agent-benchmark).

## Overview

These tests validate that LLMs can correctly understand and invoke HeyGen MCP tools through natural language prompts. Unlike traditional unit tests, these tests:

- Send natural language prompts to an LLM (e.g., GPT-4.1)
- Verify the LLM correctly calls MCP tools
- Validate the LLM produces expected outputs
- Detect if the LLM hallucinates non-existent tools

## Prerequisites

1. **agent-benchmark** - Download from [releases](https://github.com/mykhaliev/agent-benchmark/releases) or install with Go:
   ```bash
   go install github.com/mykhaliev/agent-benchmark@latest
   ```

2. **Environment Variables**:
   ```bash
   # Azure OpenAI endpoint (for LLM provider)
   export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"

   # HeyGen API key (for MCP tool operations)
   export HEYGEN_API_KEY="your-heygen-api-key"
   ```

3. **Python environment** with heygen-mcp installed:
   ```bash
   cd /path/to/heygen-mcp
   uv sync
   ```

## Configuration

### Default Configuration

Edit `llm_tests_config.json` for shared settings:

```json
{
  "agentBenchmarkPath": null,
  "agentBenchmarkMode": "executable",
  "serverCommand": null,
  "verbose": false
}
```

### Local Configuration (git-ignored)

Create `llm_tests_config.local.json` for personal settings:

```json
{
  "agentBenchmarkPath": "D:/source/agent-benchmark",
  "agentBenchmarkMode": "go-run",
  "verbose": true
}
```

### Configuration Options

| Option | Description |
|--------|-------------|
| `agentBenchmarkPath` | Path to agent-benchmark executable or source directory |
| `agentBenchmarkMode` | `"executable"` (compiled binary) or `"go-run"` (from source) |
| `serverCommand` | Custom MCP server command. Default: `uv run python -m heygen_mcp.server` |
| `verbose` | Enable verbose output by default |

## Usage

```bash
# Navigate to the test directory
cd tests/heygen_mcp_llm_tests

# List available test scenarios
python run_llm_tests.py --list

# Run all safe tests (default - excludes credit-consuming tests)
python run_llm_tests.py

# Run a specific scenario
python run_llm_tests.py -s user-credits
python run_llm_tests.py -s avatar-discovery

# Run with verbose output
python run_llm_tests.py -v

# Run ALL tests including credit-consuming ones
python run_llm_tests.py --all

# Skip environment validation (for debugging)
python run_llm_tests.py --skip-validation
```

## Test Categories

### Safe Tests (Default)

These tests only read data and don't consume credits or modify your account:

| Scenario | Description |
|----------|-------------|
| `user-credits-test` | Get user info and check credits |
| `avatar-discovery-test` | List avatars, get details, list groups |
| `voice-listing-test` | List voices, find by language |
| `template-workflow-test` | List templates, get details |
| `asset-listing-test` | List uploaded assets |

### Mutating Tests

These tests modify data in your account (create/delete folders or assets):

| Scenario | Description |
|----------|-------------|
| `folder-management-test` | Create, rename, trash folders |

### Credit-Consuming Tests

These tests generate videos and **consume HeyGen API credits**:

| Scenario | Description |
|----------|-------------|
| `video-generation-test` | Full video generation workflow |

⚠️ **Warning**: Run credit-consuming tests only when you explicitly want to test video generation.

## Test Reports

Reports are generated in `test_results/`:

- `<scenario>-report.html` - Visual HTML report
- `<scenario>-report.json` - Machine-readable JSON

## Writing New Tests

1. Copy `scenarios/_config-template.yaml.template` as a starting point
2. Define providers, servers, and agents
3. Write test sessions with natural language prompts
4. Add assertions to validate behavior

### Example Test

```yaml
sessions:
  - name: "My Test Session"
    tests:
      - name: "Test something"
        prompt: |
          Use the HeyGen tools to:
          1. List all available voices
          2. Find an English voice
          3. Report the voice name and ID
        assertions:
          - type: no_hallucinated_tools
          - type: tool_called
            tool: voices
          - type: output_regex
            pattern: "(?i)(english|voice|id)"
```

### Available Assertions

| Assertion | Description |
|-----------|-------------|
| `tool_called` | Verify a specific tool was invoked |
| `tool_param_equals` | Verify tool parameter values |
| `output_regex` | Match pattern in LLM response |
| `no_hallucinated_tools` | Ensure only real tools called |
| `no_rate_limit_errors` | No 429 errors occurred |
| `no_clarification_questions` | Agent acted without asking questions |
| `max_latency_ms` | Performance threshold |
| `anyOf` | OR logic for multiple valid approaches |
| `allOf` | AND logic for required conditions |

## Troubleshooting

### "agent-benchmark not found"

- Install: `go install github.com/mykhaliev/agent-benchmark@latest`
- Or download from [releases](https://github.com/mykhaliev/agent-benchmark/releases)
- Set `agentBenchmarkPath` in config

### "AZURE_OPENAI_ENDPOINT not set"

Set the environment variable:
```bash
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
```

### "HEYGEN_API_KEY not set"

Set the environment variable:
```bash
export HEYGEN_API_KEY="your-api-key"
```

### Tests timing out

- Increase `server_delay` in scenario YAML
- Increase `max_iterations` in settings
- Check if MCP server is starting correctly

## CI/CD Integration

For GitHub Actions, add secrets and run safe tests:

```yaml
- name: Run LLM Tests
  env:
    AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
    HEYGEN_API_KEY: ${{ secrets.HEYGEN_API_KEY }}
  run: |
    cd tests/heygen_mcp_llm_tests
    python run_llm_tests.py
```

Note: Only safe tests run by default. Credit-consuming tests require `--all` flag.
