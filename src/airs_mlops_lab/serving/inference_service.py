"""Standalone inference service.

This module is deprecated. The primary serving architecture now uses
inference_client.py to call a Vertex AI endpoint for model inference.

The main app (server.py) is a thin client that delegates to Vertex AI.
"""
