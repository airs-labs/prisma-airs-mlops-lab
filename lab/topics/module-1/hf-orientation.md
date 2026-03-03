# HuggingFace Orientation

## Topics to Cover (in order)
1. What is HuggingFace -- model hosting, model cards, organizations
2. Model sizes and quantization -- parameters, bf16/GPTQ/GGUF/AWQ
3. File formats -- safetensors vs pickle (SECURITY RELEVANT -- this is why AIRS exists)
4. Licenses -- apache-2.0, llama-community, enterprise implications
5. Leaderboards and trust -- verified orgs, evaluation benchmarks

## How to Explore
- Use `huggingface_hub` Python library: `from huggingface_hub import HfApi; api = HfApi()`
- `api.model_info("Qwen/Qwen2.5-3B")` -- model card, tags, downloads, pipeline
- `api.list_repo_refs("Qwen/Qwen2.5-3B")` -- branches, revisions
- `api.list_repo_tree("Qwen/Qwen2.5-3B")` -- file listing with sizes and formats
- Reference: docs/research/ml-pipeline-architecture-2025.md for broader ML landscape context

## Student Activities
- Find 3 base models that could serve as a cybersecurity advisor -- compare sizes, formats, licenses
- Inspect safetensors vs pickle files in a model repo -- what is structurally different?
- Check the Open LLM Leaderboard -- how do enterprises evaluate which model to trust?

## Customer Talking Point
"When a customer says they pull models from HuggingFace, ask: What format? What license? From which organization? How are they validating what they download?"
