#!/usr/bin/env python3
"""
LLM Test Runner for HeyGen MCP Server.

Uses agent-benchmark to validate that LLMs can correctly understand and invoke
HeyGen MCP tools through natural language prompts.

Usage:
    python run_llm_tests.py                      # Run all scenarios
    python run_llm_tests.py -s user-credits      # Run specific scenario
    python run_llm_tests.py --verbose            # Verbose output
    python run_llm_tests.py --list               # List available scenarios
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_config() -> dict[str, Any]:
    """Load configuration from JSON files."""
    script_dir = Path(__file__).parent
    config_path = script_dir / "llm_tests_config.json"
    local_config_path = script_dir / "llm_tests_config.local.json"

    config: dict[str, Any] = {}

    # Load base config
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)

    # Override with local config
    if local_config_path.exists():
        with open(local_config_path) as f:
            local_config = json.load(f)
            config.update(local_config)

    return config


def get_scenarios_dir() -> Path:
    """Get the scenarios directory path."""
    return Path(__file__).parent / "scenarios"


def get_test_results_dir() -> Path:
    """Get the test results directory path."""
    results_dir = Path(__file__).parent / "test_results"
    results_dir.mkdir(exist_ok=True)
    return results_dir


def list_scenarios() -> list[str]:
    """List all available test scenario files."""
    scenarios_dir = get_scenarios_dir()
    scenarios = []
    for f in scenarios_dir.glob("*.yaml"):
        if not f.name.startswith("_"):  # Skip template files
            scenarios.append(f.stem)
    return sorted(scenarios)


def find_agent_benchmark(config: dict[str, Any]) -> tuple[list[str], str]:
    """
    Find agent-benchmark executable or go-run command.

    Returns:
        Tuple of (command_parts, mode)
    """
    mode = config.get("agentBenchmarkMode", "executable")
    agent_benchmark_path = config.get("agentBenchmarkPath")

    if mode == "go-run" and agent_benchmark_path:
        # Use go run from source
        ab_dir = Path(agent_benchmark_path)
        if ab_dir.exists():
            return ["go", "run", "."], str(ab_dir)
        else:
            print(f"Warning: agent-benchmark path not found: {ab_dir}")

    # Try to find executable
    if agent_benchmark_path:
        ab_path = Path(agent_benchmark_path)
        if ab_path.is_file():
            return [str(ab_path)], str(ab_path.parent)
        exe_path = (
            ab_path / "agent-benchmark.exe"
            if platform.system() == "Windows"
            else ab_path / "agent-benchmark"
        )
        if exe_path.exists():
            return [str(exe_path)], str(ab_path)

    # Try system PATH
    exe_name = (
        "agent-benchmark.exe" if platform.system() == "Windows" else "agent-benchmark"
    )
    if shutil.which(exe_name):
        return [exe_name], os.getcwd()

    # Not found
    print("Error: agent-benchmark not found.")
    print("Options:")
    print("  1. Set agentBenchmarkPath in llm_tests_config.local.json")
    print(
        "  2. Install agent-benchmark: go install github.com/mykhaliev/agent-benchmark@latest"
    )
    print("  3. Download from: https://github.com/mykhaliev/agent-benchmark/releases")
    sys.exit(1)


def get_server_command(config: dict[str, Any]) -> str:
    """Get the MCP server command."""
    if config.get("serverCommand"):
        return config["serverCommand"]

    # Default: use uv run from the project directory
    project_dir = Path(__file__).parent.parent.parent
    return f"uv run --directory {project_dir} python -m heygen_mcp.server"


def validate_environment() -> bool:
    """Validate required environment variables are set."""
    errors = []

    if not os.environ.get("AZURE_OPENAI_ENDPOINT"):
        errors.append("AZURE_OPENAI_ENDPOINT environment variable is not set")

    if not os.environ.get("HEYGEN_API_KEY"):
        errors.append("HEYGEN_API_KEY environment variable is not set")

    if errors:
        print("Environment validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


def run_scenario(
    scenario_name: str,
    config: dict[str, Any],
    verbose: bool = False,
) -> bool:
    """
    Run a single test scenario.

    Returns:
        True if tests passed, False otherwise
    """
    scenarios_dir = get_scenarios_dir()
    results_dir = get_test_results_dir()

    # Find scenario file
    scenario_file = scenarios_dir / f"{scenario_name}.yaml"
    if not scenario_file.exists():
        # Try with -test suffix
        scenario_file = scenarios_dir / f"{scenario_name}-test.yaml"
    if not scenario_file.exists():
        print(f"Error: Scenario not found: {scenario_name}")
        print(f"Available scenarios: {', '.join(list_scenarios())}")
        return False

    print(f"\n{'='*60}")
    print(f"Running scenario: {scenario_file.name}")
    print(f"{'='*60}")

    # Get agent-benchmark command
    ab_command, ab_cwd = find_agent_benchmark(config)

    # Set environment variables for template substitution
    env = os.environ.copy()
    env["SERVER_COMMAND"] = get_server_command(config)
    env["TEST_DIR"] = str(scenarios_dir)
    env["TEST_RESULTS_PATH"] = str(results_dir)
    env["TEMP_DIR"] = os.environ.get("TEMP", "/tmp")

    # Build command
    cmd = ab_command + [
        "-f",
        str(scenario_file),
        "-o",
        str(results_dir / scenario_file.stem),
        "-reportType",
        "html,json",
    ]

    if verbose or config.get("verbose"):
        cmd.append("-verbose")

    print(f"Command: {' '.join(cmd)}")
    print(f"Working directory: {ab_cwd}")
    print()

    # Run agent-benchmark
    try:
        result = subprocess.run(
            cmd,
            cwd=ab_cwd,
            env=env,
            capture_output=False,
        )
        return result.returncode == 0
    except FileNotFoundError as e:
        print(f"Error running agent-benchmark: {e}")
        return False
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="LLM Test Runner for HeyGen MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_llm_tests.py                      # Run all safe scenarios
    python run_llm_tests.py -s user-credits      # Run specific scenario
    python run_llm_tests.py -s video-generation  # Run video test (uses credits!)
    python run_llm_tests.py --list               # List available scenarios
    python run_llm_tests.py --verbose            # Verbose output
        """,
    )
    parser.add_argument(
        "-s",
        "--scenario",
        help="Run specific scenario (without .yaml extension)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available test scenarios",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run ALL scenarios including credit-consuming ones",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip environment variable validation",
    )

    args = parser.parse_args()

    # List scenarios
    if args.list:
        scenarios = list_scenarios()
        print("Available test scenarios:")
        print()
        for s in scenarios:
            marker = ""
            if "video" in s.lower():
                marker = " [USES CREDITS]"
            elif "folder-management" in s.lower():
                marker = " [MUTATING]"
            print(f"  {s}{marker}")
        print()
        print("Run with: python run_llm_tests.py -s <scenario-name>")
        return 0

    # Load config
    config = load_config()

    # Validate environment
    if not args.skip_validation:
        if not validate_environment():
            print()
            print("Set the required environment variables and try again.")
            return 1

    # Determine which scenarios to run
    if args.scenario:
        scenarios_to_run = [args.scenario]
    elif args.all:
        scenarios_to_run = list_scenarios()
    else:
        # Run only safe scenarios by default
        all_scenarios = list_scenarios()
        scenarios_to_run = [
            s
            for s in all_scenarios
            if "video" not in s.lower()  # Skip credit-consuming tests
        ]

    if not scenarios_to_run:
        print("No scenarios to run.")
        print("Use --list to see available scenarios.")
        return 1

    print(f"Will run {len(scenarios_to_run)} scenario(s)")

    # Run scenarios
    results = {}
    for scenario in scenarios_to_run:
        success = run_scenario(scenario, config, verbose=args.verbose)
        results[scenario] = success

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed

    for scenario, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {scenario}: {status}")

    print()
    print(f"Total: {passed} passed, {failed} failed")

    # Reports location
    results_dir = get_test_results_dir()
    print(f"\nReports saved to: {results_dir}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
