"""Model serving - Chat inference via Vertex AI or local backends."""

from airs_mlops_lab.serving.inference_client import get_inference_client, InferenceClient

__all__ = ["get_inference_client", "InferenceClient"]
