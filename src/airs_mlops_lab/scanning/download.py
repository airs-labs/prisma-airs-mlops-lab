"""Utility functions for downloading models from HuggingFace and GCS.

These are helper utilities for local development and testing,
not used by the production pipeline.
"""

from pathlib import Path

from huggingface_hub import HfApi, snapshot_download
from huggingface_hub.utils import HfHubHTTPError


def download_model(model_id: str, cache_dir: Path | None = None) -> Path:
    """Download a Hugging Face model to a local directory.

    Uses snapshot_download() to download all model files including safetensors,
    config, and tokenizer files.

    Args:
        model_id: The Hugging Face model identifier (e.g., 'distilbert-base-uncased-finetuned-sst-2-english')
        cache_dir: Optional directory to store downloaded models. Defaults to ./models/

    Returns:
        Path to the downloaded model directory.

    Raises:
        HfHubHTTPError: If the model ID is invalid or not found.
    """
    if cache_dir is None:
        cache_dir = Path("./models")

    cache_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model: {model_id}")
    print(f"Cache directory: {cache_dir}")

    try:
        model_path = snapshot_download(
            repo_id=model_id,
            cache_dir=cache_dir,
        )
        print(f"Download complete: {model_path}")
        return Path(model_path)
    except HfHubHTTPError as e:
        print(f"Error downloading model {model_id}: {e}")
        raise


def get_model_info(model_id: str) -> dict:
    """Retrieve metadata for a Hugging Face model.

    Uses the Hugging Face API to fetch model information including
    author, license, tags, and format details relevant for AIRS scanning.

    Args:
        model_id: The Hugging Face model identifier (e.g., 'distilbert-base-uncased-finetuned-sst-2-english')

    Returns:
        Dictionary containing model metadata:
            - model_id: The model identifier
            - author: Model author/organization
            - license: License type (if available)
            - tags: List of model tags
            - safetensors: Whether model uses safetensors format
            - pipeline_tag: The model's pipeline task type

    Raises:
        HfHubHTTPError: If the model ID is invalid or not found.
    """
    api = HfApi()

    try:
        info = api.model_info(model_id)

        # Check if model uses safetensors format
        has_safetensors = False
        if info.siblings:
            has_safetensors = any(
                sibling.rfilename.endswith(".safetensors")
                for sibling in info.siblings
            )

        return {
            "model_id": info.id,
            "author": info.author,
            "license": getattr(info, "license", None),
            "tags": info.tags or [],
            "safetensors": has_safetensors,
            "pipeline_tag": info.pipeline_tag,
        }
    except HfHubHTTPError as e:
        print(f"Error fetching model info for {model_id}: {e}")
        raise
