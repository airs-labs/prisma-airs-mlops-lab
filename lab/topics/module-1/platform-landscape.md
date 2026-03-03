# ML Platform Landscape

## Topics to Cover (in order)
1. Managed vs raw compute -- Vertex AI vs GCE instances, tradeoffs
2. GPU types -- A100 (training), L4 (inference), T4 (budget), cost per hour
3. Inference options -- Vertex AI endpoint (managed) vs self-hosted (GCE + vLLM/TGI)
4. Cost and performance tradeoffs -- when to use which option
5. This project's choices -- why Vertex AI + L4 for a 3B model

## How to Explore
- Check GCP pricing: Vertex AI custom training vs GCE GPU instances
- This project uses: g2-standard-12 with 1x L4 GPU for inference
- Training: Vertex AI CustomJob with `pytorch-gpu.2-4.py310:latest` container
- Reference: docs/research/vertex-ai-model-serving-2025.md for serving architecture
- Reference: .github/workflows/gate-1-train.yaml for training config

## Student Activities
- Compare the cost of training Qwen 3B on Vertex AI vs a GCE a2-highgpu-1g instance
- Calculate: how much would it cost to serve this model 24/7 on an L4 vs an A100?
- Why did this project choose a thin Cloud Run app + Vertex AI endpoint instead of putting the model in the container?

## Customer Talking Point
"Customers often ask about GPU costs. The architecture choice (managed endpoint vs self-hosted) has security implications too -- managed endpoints have different attack surfaces than self-hosted containers."
