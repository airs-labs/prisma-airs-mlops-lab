#!/usr/bin/env python3
"""CLI tool for scanning ML models using AIRS Model Security.

Usage:
    python scripts/scan_model.py MODEL_PATH_OR_HF_ID [OPTIONS]

Examples:
    # Scan a HuggingFace model
    python scripts/scan_model.py distilbert/distilbert-base-uncased-finetuned-sst-2-english

    # Scan a local model directory
    python scripts/scan_model.py ./models/my-model

    # Output raw JSON instead of visual
    python scripts/scan_model.py distilbert/distilbert-base-uncased --json

    # CI mode (machine-readable output, exit 1 on blocking findings)
    python scripts/scan_model.py my-model --ci

    # CI mode with warnings treated as failures
    python scripts/scan_model.py my-model --ci --fail-on-warn

    # Override security group
    python scripts/scan_model.py my-model --security-group UUID
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from uuid import UUID

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from airs_mlops_lab.scanning import (
    DEFAULT_SECURITY_GROUPS,
    SourceType,
    render_scan_result,
    scan_model,
)


def is_local_path(model_ref: str) -> bool:
    """Determine if model_ref is a local path or HuggingFace reference.

    Local paths:
    - Start with / (absolute)
    - Start with . (relative)
    - Start with ~ (home)
    - Contain file:// prefix
    - Exist as file/directory on disk

    HuggingFace references:
    - model-id or org/model-id format
    - hf:// prefix
    - huggingface.co URLs
    """
    # Explicit prefixes
    if model_ref.startswith("file://"):
        return True
    if model_ref.startswith(("hf://", "https://huggingface.co")):
        return False

    # Cloud storage
    if model_ref.startswith(("gs://", "s3://", "az://", "azure://")):
        return False

    # Path-like patterns
    if model_ref.startswith(("/", "./", "../", "~")):
        return True

    # Check if it exists on disk
    expanded = os.path.expanduser(model_ref)
    if os.path.exists(expanded):
        return True

    # Default: assume HuggingFace reference
    return False


def format_model_uri(model_ref: str) -> str:
    """Convert model reference to proper URI format for AIRS SDK.

    HuggingFace models must be full URLs:
    - distilbert/model -> https://huggingface.co/distilbert/model
    - hf://org/model -> https://huggingface.co/org/model
    """
    # Already a full URL
    if model_ref.startswith("https://"):
        return model_ref

    # hf:// prefix
    if model_ref.startswith("hf://"):
        model_id = model_ref[5:]  # Remove hf://
        return f"https://huggingface.co/{model_id}"

    # Simple model ID (org/model or just model)
    return f"https://huggingface.co/{model_ref}"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Scan ML models for security issues using AIRS Model Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s distilbert/distilbert-base-uncased
      Scan a HuggingFace model by ID

  %(prog)s ./models/my-model
      Scan a local model directory

  %(prog)s my-org/my-model --json
      Output raw JSON instead of visual results

  %(prog)s my-model --security-group UUID
      Use a specific security group
        """,
    )

    parser.add_argument(
        "model",
        help="Model path (local) or HuggingFace model ID",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output raw JSON instead of visual results",
    )

    parser.add_argument(
        "--security-group",
        type=str,
        metavar="UUID",
        help="Security group UUID to use (overrides auto-detection)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Scan timeout in seconds (default: 600)",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional debug information",
    )

    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: machine-readable output, exit 0 for PASS/WARN, exit 1 for FAIL",
    )

    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Treat warnings as failures (exit 1). Only meaningful with --ci",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Determine if local or remote
    is_local = is_local_path(args.model)

    if args.verbose:
        print(f"Model reference: {args.model}")
        print(f"Detected as: {'local path' if is_local else 'HuggingFace reference'}")

    # Prepare scan arguments
    model_path = None
    model_uri = None

    if is_local:
        # Local path
        expanded = os.path.expanduser(args.model)
        if args.model.startswith("file://"):
            model_path = args.model[7:]  # Remove file://
        else:
            model_path = os.path.abspath(expanded)

        if not os.path.exists(model_path):
            print(f"Error: Local path does not exist: {model_path}", file=sys.stderr)
            return 1

        if args.verbose:
            print(f"Local path: {model_path}")
    else:
        # HuggingFace or cloud reference
        model_uri = format_model_uri(args.model)
        if args.verbose:
            print(f"Model URI: {model_uri}")

    # Parse security group if provided
    security_group = None
    if args.security_group:
        try:
            security_group = UUID(args.security_group)
        except ValueError:
            print(
                f"Error: Invalid security group UUID: {args.security_group}",
                file=sys.stderr,
            )
            return 1

    # Show default security groups if verbose
    if args.verbose and security_group is None:
        source_type = SourceType.LOCAL if is_local else SourceType.HUGGING_FACE
        default_group = DEFAULT_SECURITY_GROUPS.get(source_type)
        print(f"Using default security group for {source_type.value}: {default_group}")

    # Execute scan
    print(f"Scanning {'local model' if is_local else 'HuggingFace model'}...")
    print()

    try:
        result = scan_model(
            model_path=model_path,
            model_uri=model_uri,
            security_group=security_group,
            poll_timeout_secs=args.timeout,
        )
    except Exception as e:
        print(f"Error: Scan failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    # Output results
    if args.ci:
        # CI mode: machine-readable output
        verdict = result.verdict.value.upper()
        finding_count = len(result.findings)
        blocking_count = sum(1 for f in result.findings if f.blocking)

        print(f"AIRS Scan: {verdict} - {finding_count} finding(s)")

        # List blocking findings if any
        if blocking_count > 0:
            print(f"Blocking findings ({blocking_count}):")
            for f in result.findings:
                if f.blocking:
                    print(f"  - [{f.severity}] {f.rule}: {f.message}")

        # Determine exit code based on verdict and flags
        # FAIL always exits 1 (blocking findings detected)
        # WARN exits 1 only if --fail-on-warn is set
        # PASS always exits 0
        if verdict == "BLOCKED":
            return 1
        elif verdict == "WARN" and args.fail_on_warn:
            print("Warning: Treating warnings as failures (--fail-on-warn)")
            return 1
        else:
            return 0
    elif args.output_json:
        # Raw JSON output
        output = {
            "verdict": result.verdict.value,
            "is_safe": result.is_safe,
            "findings": [
                {
                    "rule": f.rule,
                    "severity": f.severity,
                    "blocking": f.blocking,
                    "message": f.message,
                }
                for f in result.findings
            ],
            "scan_uuid": result.scan_uuid,
            "model_name": result.model_name,
        }
        if args.verbose and result.raw_response:
            output["raw_response"] = result.raw_response
        print(json.dumps(output, indent=2, default=str))
    else:
        # Visual output
        render_scan_result(result, show_raw=args.verbose)

    # Return exit code based on verdict (for non-CI modes)
    if result.is_safe:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
