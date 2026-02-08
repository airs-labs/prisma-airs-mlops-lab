#!/usr/bin/env python
"""End-to-end test script for Cloud Security Advisor chat inference.

Tests the /api/chat endpoint against a running server instance.

Usage:
    # Start the server first:
    INFERENCE_BACKEND=vertex_ai VERTEX_ENDPOINT_ID=<id> uvicorn airs_mlops_lab.serving.server:app

    # Then run the test:
    python scripts/test_inference.py [--url http://localhost:8080]
"""

import argparse
import httpx
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Cloud Security Advisor chat")
    parser.add_argument("--url", default="http://localhost:8080", help="Server URL")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")

    print("=" * 60)
    print("Cloud Security Advisor - Chat Inference Test")
    print(f"Server: {base_url}")
    print("=" * 60)

    # Step 1: Health check
    print("\n[Step 1] Health check...")
    resp = httpx.get(f"{base_url}/health", timeout=10.0)
    resp.raise_for_status()
    health = resp.json()
    print(f"  Status: {health['status']}")
    print(f"  Backend: {health['backend']}")

    # Step 2: Chat request
    print("\n[Step 2] Sending chat message...")
    test_message = "What are NIST best practices for SSH hardening?"
    resp = httpx.post(
        f"{base_url}/api/chat",
        json={"message": test_message, "max_tokens": 256},
        timeout=60.0,
    )
    resp.raise_for_status()
    chat = resp.json()
    reply = chat["reply"]

    print(f"  Question: {test_message}")
    print(f"  Reply ({len(reply)} chars):")
    print(f"  {reply[:500]}...")

    # Step 3: Verify response is not empty or error
    print("\n[Step 3] Verifying response...")
    assert len(reply) > 20, f"Response too short: {reply!r}"
    print("  Response is non-trivial.")

    print("\n" + "=" * 60)
    print("Chat Inference Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
