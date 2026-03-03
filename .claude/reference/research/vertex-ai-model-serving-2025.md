# Vertex AI Model Serving & Inference - Research Report (2025-2026)

**Researched**: 2026-02-04
**Context**: AIRS MLOps Lab - deploying fine-tuned Qwen2.5-3B model for inference
**Researcher**: Ava Sterling (Claude Researcher)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Option A: Vertex AI Endpoints with vLLM](#option-a-vertex-ai-endpoints-with-vllm)
3. [Option B: Cloud Run with GPU](#option-b-cloud-run-with-gpu)
4. [Option C: Model Garden Custom Weights (Simplified)](#option-c-model-garden-custom-weights)
5. [Serving Containers](#serving-containers)
6. [GPU Options & Cost Analysis](#gpu-options--cost-analysis)
7. [Prediction API Formats](#prediction-api-formats)
8. [Complete gcloud Command Reference](#complete-gcloud-command-reference)
9. [Strategic Recommendations for AIRS MLOps Lab](#strategic-recommendations-for-airs-mlops-lab)

---

## Executive Summary

Three viable paths exist for serving a fine-tuned Qwen2.5-3B model from GCS:

| Option | Cost/hr | Scale-to-Zero | Startup Time | Complexity |
|--------|---------|---------------|--------------|------------|
| **Vertex AI Endpoint** (g2-standard-12 + L4) | ~$0.73-1.40/hr | No (always-on) | N/A (warm) | Medium |
| **Cloud Run + GPU** (L4) | ~$0.30-0.80/hr (usage) | Yes | ~19s cold start | Low |
| **Model Garden Custom Weights** | Same as Vertex AI | No | N/A | Lowest |

**Key insight**: Cloud Run with GPU (now GA) is the most cost-effective option for variable workloads because it scales to zero. For production with consistent traffic, Vertex AI Endpoints provide lower latency. For this lab, Cloud Run with GPU is the strategic choice -- it resolves the current pipeline disconnect where Gate 3 deploys a rule-based app instead of the actual trained model.

---

## Option A: Vertex AI Endpoints with vLLM

### Step 1: Upload Model to Vertex AI Model Registry

```bash
# Variables
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
MODEL_NAME="cloud-security-advisor"
MODEL_GCS="gs://your-model-bucket/raw-models/clean-advisor"
VLLM_IMAGE="us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01"

# Upload model to Vertex AI Model Registry
gcloud ai models upload \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --display-name="$MODEL_NAME" \
  --container-image-uri="$VLLM_IMAGE" \
  --container-command="python,-m,vllm.entrypoints.api_server" \
  --container-args="--host=0.0.0.0,--port=7080,--model=$MODEL_GCS,--max-model-len=4096,--gpu-memory-utilization=0.95,--dtype=bfloat16,--disable-log-stats" \
  --container-ports=7080 \
  --container-health-route="/ping" \
  --container-predict-route="/generate"
```

**Alternative with artifact-uri** (for merged model weights in GCS):

```bash
gcloud ai models upload \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --display-name="$MODEL_NAME" \
  --artifact-uri="$MODEL_GCS" \
  --container-image-uri="$VLLM_IMAGE" \
  --container-command="python,-m,vllm.entrypoints.api_server" \
  --container-args="--host=0.0.0.0,--port=7080,--model=$MODEL_GCS,--max-model-len=4096,--gpu-memory-utilization=0.95,--dtype=bfloat16" \
  --container-ports=7080 \
  --container-health-route="/ping" \
  --container-predict-route="/generate"
```

### Step 2: Create Endpoint

```bash
gcloud ai endpoints create \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --display-name="$MODEL_NAME-endpoint"
```

Note the `ENDPOINT_ID` from the output.

### Step 3: Deploy Model to Endpoint

```bash
ENDPOINT_ID="<from-previous-step>"
MODEL_ID="<from-upload-step>"

gcloud ai endpoints deploy-model "$ENDPOINT_ID" \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --model="$MODEL_ID" \
  --display-name="$MODEL_NAME-deployment" \
  --machine-type=g2-standard-12 \
  --accelerator-type=NVIDIA_L4 \
  --accelerator-count=1 \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100
```

### Step 4: Get Predictions

```bash
# Using rawPredict (OpenAI-compatible format)
curl -X POST \
  "https://$REGION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$REGION/endpoints/$ENDPOINT_ID:rawPredict" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cloud-security-advisor",
    "messages": [
      {"role": "system", "content": "You are a cloud security advisor."},
      {"role": "user", "content": "What are the top 3 IAM best practices?"}
    ],
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

### Cleanup

```bash
# Undeploy (stop billing)
gcloud ai endpoints undeploy-model "$ENDPOINT_ID" \
  --deployed-model-id="$DEPLOYED_MODEL_ID" \
  --region="$REGION"

# Delete endpoint
gcloud ai endpoints delete "$ENDPOINT_ID" --region="$REGION"

# Delete model
gcloud ai models delete "$MODEL_ID" --region="$REGION"
```

---

## Option B: Cloud Run with GPU

Cloud Run GPU support is **GA** as of 2025. This is the most cost-effective option for variable/lab workloads because it scales to zero.

### Available GPUs on Cloud Run

| GPU | VRAM | Status | Min CPU | Min Memory |
|-----|------|--------|---------|------------|
| **NVIDIA L4** | 24 GB | GA | 4 CPU (8 recommended) | 16 GiB (32 GiB recommended) |
| **NVIDIA RTX PRO 6000 Blackwell** | 96 GB | Preview | 20 CPU | 80 GiB |

### Deploy with vLLM on Cloud Run

**Option B1: Using Google's prebuilt vLLM image with GCS FUSE**

```bash
# Store merged model in GCS bucket
BUCKET_NAME="your-model-bucket"
MODEL_PATH="raw-models/clean-advisor"

# Deploy using Google's vLLM container with Cloud Storage FUSE mount
gcloud run deploy cloud-security-advisor \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --image="us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01" \
  --port=8000 \
  --cpu=8 \
  --memory=32Gi \
  --gpu=1 \
  --gpu-type=nvidia-l4 \
  --no-gpu-zonal-redundancy \
  --max-instances=1 \
  --no-cpu-throttling \
  --timeout=600 \
  --command="python3" \
  --args="-m,vllm.entrypoints.openai.api_server,--model=/models/$MODEL_PATH,--host=0.0.0.0,--port=8000,--max-model-len=4096,--dtype=bfloat16,--gpu-memory-utilization=0.95" \
  --add-volume=name=model-weights,type=cloud-storage,bucket=$BUCKET_NAME \
  --add-volume-mount=volume=model-weights,mount-path=/models \
  --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="HF_HUB_OFFLINE=1"
```

**Option B2: Custom Dockerfile**

```dockerfile
FROM us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01

ENV MODEL_ID=/models/clean-advisor
ENV PORT=8000

CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "/models/clean-advisor", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--max-model-len", "4096", \
     "--dtype", "bfloat16", \
     "--gpu-memory-utilization", "0.95"]
```

### Key Cloud Run GPU Considerations

- **Scale to zero**: Instances can scale down to 0 when no requests are pending, so you only pay for actual usage.
- **Cold start**: ~19 seconds time-to-first-token when scaling from zero (includes startup, model loading, and inference).
- **Auto-scaling**: Cloud Run handles scaling automatically, including GPU instances.
- **GPU quota**: Projects get 3 L4 GPUs automatically on first deployment; more requires quota increase.
- **No reservations**: On-demand availability, no commitments required.
- **Billing**: 30-second increments, not hourly.

### Calling the Cloud Run Endpoint

```bash
SERVICE_URL=$(gcloud run services describe cloud-security-advisor --region=$REGION --format="value(status.url)")

# OpenAI-compatible chat completions
curl -X POST "$SERVICE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "clean-advisor",
    "messages": [
      {"role": "system", "content": "You are a cloud security advisor."},
      {"role": "user", "content": "What are the top 3 IAM best practices?"}
    ],
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

---

## Option C: Model Garden Custom Weights (Simplified)

This is the simplest approach -- a single gcloud command that handles model upload, endpoint creation, and deployment automatically.

```bash
# One-command deploy (Preview feature)
gcloud ai model-garden models deploy \
  --model="gs://your-model-bucket/raw-models/clean-advisor" \
  --machine-type=g2-standard-12 \
  --accelerator-type=NVIDIA_L4 \
  --accelerator-count=1 \
  --region=us-central1
```

**Python SDK alternative:**

```python
from vertexai.preview import model_garden

custom_model = model_garden.CustomModel(
    gcs_uri="gs://your-model-bucket/raw-models/clean-advisor"
)

endpoint = custom_model.deploy(
    machine_type="g2-standard-12",
    accelerator_type="NVIDIA_L4",
    accelerator_count=1,
    model_display_name="cloud-security-advisor",
    endpoint_display_name="cloud-security-advisor-endpoint"
)
```

**Caveats:**
- This is a Preview feature (pre-GA).
- Model must be in HuggingFace weights format (safetensors).
- Less control over vLLM configuration parameters.
- No custom container args (max-model-len, dtype, etc.).

---

## Serving Containers

### Pre-built Containers Available on Vertex AI

| Framework | Container URI | Use Case |
|-----------|--------------|----------|
| **vLLM** (Google-optimized) | `us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:<tag>` | Text generation, chat (recommended) |
| **Hex-LLM** | Google-internal optimized | Alternative to vLLM |
| **SGLang** | Available via Model Garden | Advanced serving |
| **TGI** (HuggingFace) | HuggingFace DLC | Text generation |
| **TEI** (HuggingFace) | HuggingFace DLC | Text embeddings |
| **TensorRT-LLM** | NVIDIA container | Maximum throughput |

### Google's Optimized vLLM Container

Google's vLLM is NOT vanilla open-source vLLM. Key enhancements:

- **Parallel GCS downloads**: Faster model loading from Cloud Storage
- **Dynamic LoRA**: Load LoRA adapters from GCS paths or signed URLs with local caching
- **Host memory prefix caching**: Extends beyond GPU-only caching
- **Speculative decoding**: Pre-tuned configurations
- **Nginx integration**: Multi-replica serving

### Latest Container Tags (as of early 2025)

```
# General purpose
us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01

# Earlier stable
us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250202_0916_RC00
```

### Key vLLM Container Arguments

| Argument | Description | Recommended Value (3B model) |
|----------|-------------|------------------------------|
| `--model` | HF model ID or `gs://` path | `gs://your-model-bucket/raw-models/clean-advisor` |
| `--max-model-len` | Max sequence length | `4096` |
| `--gpu-memory-utilization` | GPU memory fraction | `0.95` |
| `--dtype` | Data type | `bfloat16` (for L4/A100) |
| `--tensor-parallel-size` | Number of GPUs | `1` (for single L4) |
| `--enable-prefix-caching` | KV cache reuse | Include for chat workloads |
| `--disable-log-stats` | Reduce log noise | Include in production |

### Container Entry Points

| Entry Point | API Style | Health Route | Predict Route |
|-------------|-----------|-------------|---------------|
| `vllm.entrypoints.api_server` | Vertex AI native | `/ping` | `/generate` |
| `vllm.entrypoints.openai.api_server` | OpenAI-compatible | `/health` | `/v1/chat/completions` |

---

## GPU Options & Cost Analysis

### Vertex AI GPU Pricing (us-central1, on-demand)

| GPU | VRAM | Machine Type | Approx. Total Cost/hr | Fits 3B Model? |
|-----|------|-------------|----------------------|-----------------|
| **NVIDIA T4** | 16 GB | n1-standard-8 + T4 | ~$0.73/hr | Yes (with quantization) |
| **NVIDIA L4** | 24 GB | g2-standard-12 | ~$1.00-1.40/hr | Yes (bfloat16, comfortable) |
| **NVIDIA A100 40GB** | 40 GB | a2-highgpu-1g | ~$3.67/hr | Overkill for 3B |
| **NVIDIA H100 80GB** | 80 GB | a3-highgpu-1g | ~$11+/hr | Massive overkill |

### Cloud Run GPU Pricing

| GPU | VRAM | Approx. Cost/hr (active) | Scale to Zero |
|-----|------|--------------------------|---------------|
| **NVIDIA L4** | 24 GB | ~$0.30-0.80/hr | Yes |
| **RTX PRO 6000** | 96 GB | TBD (Preview) | Yes |

### Cost Optimization Strategies

1. **Spot VMs** (Vertex AI): 60-91% discount, but instances can be preempted
2. **Scale-to-zero** (Cloud Run): Only pay when serving requests
3. **Committed Use Discounts**: 1-year (20%) or 3-year (55%) commitments
4. **Quantization**: INT8/INT4 allows using cheaper T4 GPU
5. **Min replicas = 0**: On Vertex AI, set min replicas to 0 (if supported) for auto-scaling

### Recommendation for 3B Model

**NVIDIA L4 (24 GB VRAM)** is the clear winner for a 3B parameter model:

- Qwen2.5-3B in bfloat16 requires ~6 GB VRAM
- L4 has 24 GB, leaving ~18 GB for KV cache and batch processing
- L4 supports bfloat16 natively (Ada Lovelace architecture)
- Best price-to-performance ratio for models under 7B parameters

---

## Prediction API Formats

### Format 1: Vertex AI Standard (`predict`)

```bash
# Request
POST https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/endpoints/{ENDPOINT}:predict

{
  "instances": [
    {"prompt": "What are IAM best practices?", "max_tokens": 512}
  ],
  "parameters": {
    "temperature": 0.7
  }
}

# Response
{
  "predictions": ["...generated text..."],
  "deployedModelId": "123456789"
}
```

### Format 2: Vertex AI Raw (`rawPredict`)

Bypasses Vertex AI serialization, sends directly to container. Preferred for vLLM.

```bash
# Request
POST https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/endpoints/{ENDPOINT}:rawPredict

{
  "model": "cloud-security-advisor",
  "messages": [
    {"role": "system", "content": "You are a cloud security advisor."},
    {"role": "user", "content": "What are IAM best practices?"}
  ],
  "max_tokens": 512,
  "temperature": 0.7,
  "stream": false
}

# Response (OpenAI-compatible)
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Here are the top IAM best practices..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  }
}
```

### Format 3: OpenAI-compatible (vLLM native / Cloud Run)

When using `vllm.entrypoints.openai.api_server`, the API is fully OpenAI-compatible.

```bash
# Chat completions
POST /v1/chat/completions

# Text completions
POST /v1/completions

# Models list
GET /v1/models
```

### Format 4: Vertex AI Chat Completions Endpoint

Vertex AI also provides a dedicated OpenAI-compatible endpoint:

```bash
POST https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/endpoints/{ENDPOINT}/chat/completions
```

---

## Complete gcloud Command Reference

### Full Workflow: Vertex AI Endpoint

```bash
# 0. Set variables
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export MODEL_NAME="cloud-security-advisor"
export MODEL_GCS="gs://your-model-bucket/raw-models/clean-advisor"
export VLLM_IMAGE="us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01"

# 1. Upload model
gcloud ai models upload \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --display-name="$MODEL_NAME" \
  --container-image-uri="$VLLM_IMAGE" \
  --container-command="python,-m,vllm.entrypoints.openai.api_server" \
  --container-args="--host=0.0.0.0,--port=7080,--model=$MODEL_GCS,--max-model-len=4096,--gpu-memory-utilization=0.95,--dtype=bfloat16,--disable-log-stats" \
  --container-ports=7080 \
  --container-health-route="/health" \
  --container-predict-route="/v1/chat/completions"

# 2. Get model ID
MODEL_ID=$(gcloud ai models list --region="$REGION" --filter="displayName=$MODEL_NAME" --format="value(name)" | head -1)

# 3. Create endpoint
gcloud ai endpoints create \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --display-name="$MODEL_NAME-endpoint"

# 4. Get endpoint ID
ENDPOINT_ID=$(gcloud ai endpoints list --region="$REGION" --filter="displayName=$MODEL_NAME-endpoint" --format="value(name)" | head -1)

# 5. Deploy model to endpoint
gcloud ai endpoints deploy-model "$ENDPOINT_ID" \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --model="$MODEL_ID" \
  --display-name="$MODEL_NAME-v1" \
  --machine-type=g2-standard-12 \
  --accelerator-type=NVIDIA_L4 \
  --accelerator-count=1 \
  --min-replica-count=1 \
  --max-replica-count=2 \
  --traffic-split=0=100

# 6. Test prediction
curl -X POST \
  "https://$REGION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$REGION/endpoints/$ENDPOINT_ID:rawPredict" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cloud-security-advisor",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'

# 7. Cleanup
DEPLOYED_MODEL_ID=$(gcloud ai endpoints describe "$ENDPOINT_ID" --region="$REGION" --format="value(deployedModels[0].id)")
gcloud ai endpoints undeploy-model "$ENDPOINT_ID" --deployed-model-id="$DEPLOYED_MODEL_ID" --region="$REGION"
gcloud ai endpoints delete "$ENDPOINT_ID" --region="$REGION" --quiet
gcloud ai models delete "$MODEL_ID" --region="$REGION" --quiet
```

### Full Workflow: Cloud Run with GPU

```bash
# 0. Set variables
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export BUCKET="your-model-bucket"
export SERVICE_NAME="cloud-security-advisor"
export SERVICE_ACCOUNT="cloud-run-sa@$PROJECT_ID.iam.gserviceaccount.com"

# 1. Deploy with vLLM + GCS FUSE
gcloud run deploy "$SERVICE_NAME" \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --image="us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01" \
  --port=8000 \
  --cpu=8 \
  --memory=32Gi \
  --gpu=1 \
  --gpu-type=nvidia-l4 \
  --no-gpu-zonal-redundancy \
  --max-instances=1 \
  --no-cpu-throttling \
  --timeout=600 \
  --command="python3" \
  --args="-m,vllm.entrypoints.openai.api_server,--model=/models/raw-models/clean-advisor,--host=0.0.0.0,--port=8000,--max-model-len=4096,--dtype=bfloat16,--gpu-memory-utilization=0.95" \
  --add-volume=name=model-weights,type=cloud-storage,bucket=$BUCKET \
  --add-volume-mount=volume=model-weights,mount-path=/models \
  --service-account="$SERVICE_ACCOUNT" \
  --set-env-vars="HF_HUB_OFFLINE=1"

# 2. Get service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)")

# 3. Test prediction
curl -X POST "$SERVICE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "clean-advisor",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'

# 4. Cleanup
gcloud run services delete "$SERVICE_NAME" --region="$REGION" --quiet
```

### Model Garden One-Command Deploy

```bash
gcloud ai model-garden models deploy \
  --model="gs://your-model-bucket/raw-models/clean-advisor" \
  --machine-type=g2-standard-12 \
  --accelerator-type=NVIDIA_L4 \
  --accelerator-count=1 \
  --region=us-central1

# List Model Garden endpoints
gcloud ai endpoints list --list-model-garden-endpoints-only --region=us-central1

# Check deployment status
gcloud ai operations describe OPERATION_ID --region=us-central1
```

---

## Strategic Recommendations for AIRS MLOps Lab

### Current Pipeline Disconnect (from MEMORY.md)

The current pipeline has a fundamental disconnect:
- **Training**: Produces LoRA adapters for Qwen2.5-3B
- **Deployment**: Serves a hardcoded DistilBERT sentiment model
- **Chat endpoint**: Rule-based keyword matching, not actual inference

### Recommended Architecture Changes

**Phase 1: Merge LoRA adapters into base model**

After Gate 1 training completes, add a step to merge the LoRA adapters with the base Qwen2.5-3B model and save the merged weights to GCS in HuggingFace safetensors format.

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base + LoRA
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
model = PeftModel.from_pretrained(base_model, "gs://your-model-bucket/trained-models/...")

# Merge and save
merged_model = model.merge_and_unload()
merged_model.save_pretrained("gs://your-model-bucket/raw-models/cloud-security-advisor-merged")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
tokenizer.save_pretrained("gs://your-model-bucket/raw-models/cloud-security-advisor-merged")
```

**Phase 2: Replace Gate 3 deployment**

Replace the current Cloud Run deployment (which serves DistilBERT) with the Cloud Run + GPU + vLLM approach described in Option B. This makes Gate 3 actually serve the trained model.

**Phase 3: Update AIRS scanning for merged model**

AIRS Gate 2 scans the raw model. After the merge step, scan the merged model artifact before publishing.

### Second-Order Effects to Consider

1. **Cost implications**: Cloud Run with GPU charges ~$0.30-0.80/hr when active. With scale-to-zero, lab costs stay minimal. But an always-on Vertex AI endpoint would cost ~$1.00+/hr continuously.

2. **Cold start latency**: A 3B model on Cloud Run with vLLM has ~19s cold start. For a lab/demo this is acceptable; for production, consider keeping min-instances=1.

3. **Dynamic LoRA alternative**: Google's vLLM supports loading LoRA adapters directly from GCS without merging. This means you could serve the base model + dynamically load different LoRA adapters for different use cases. This is more flexible but adds complexity.

4. **AIRS scanning interaction**: The merged model may trigger different AIRS scan results than the LoRA-only adapter. Test this before committing to the merged approach.

5. **Cloud Run memory limits**: 32 GiB RAM + 24 GB VRAM is sufficient for a 3B model, but if you later move to 7B+ models, you may need the RTX PRO 6000 (96 GB, Preview) or switch to Vertex AI endpoints with A100.

---

## Sources

- [Deploy a model to an endpoint - Google Cloud](https://cloud.google.com/vertex-ai/docs/general/deployment)
- [Deploy a model by using the gcloud CLI - Google Cloud](https://cloud.google.com/vertex-ai/docs/predictions/deploy-model-api)
- [Deploy models with custom weights - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/deploy-models-with-custom-weights)
- [Prebuilt containers for inference - Google Cloud](https://docs.cloud.google.com/vertex-ai/docs/predictions/pre-built-containers)
- [vLLM serving on Vertex AI - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/open-models/vllm/use-vllm)
- [Deploy open models with prebuilt containers - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/open-models/use-prebuilt-containers)
- [Deploy open models with custom vLLM container - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/open-models/deploy-custom-vllm)
- [Cloud Run GPU support - Google Cloud](https://docs.cloud.google.com/run/docs/configuring/services/gpu)
- [Cloud Run GPUs are now GA - Google Cloud Blog](https://cloud.google.com/blog/products/serverless/cloud-run-gpus-are-now-generally-available)
- [Host your LLMs on Cloud Run - Google Cloud Blog](https://cloud.google.com/blog/products/application-development/run-your-ai-inference-applications-on-cloud-run-with-nvidia-gpus)
- [Configure compute resources for inference - Google Cloud](https://docs.cloud.google.com/vertex-ai/docs/predictions/configure-compute)
- [GPU pricing - Google Cloud](https://cloud.google.com/compute/gpus-pricing)
- [Vertex AI pricing - Google Cloud](https://cloud.google.com/vertex-ai/pricing)
- [Get online inferences from custom trained model - Google Cloud](https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions)
- [rawPredict API reference - Google Cloud](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/rawPredict)
- [Using OpenAI libraries with Vertex AI - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/openai/overview)
- [Practical LLM Serving with vLLM on VertexAI - Dylan's Blog](https://blog.infocruncher.com/2025/02/27/llm-serving-with-vllm-on-vertexai/)
- [Run LLM inference on Cloud Run GPUs with vLLM - Google Codelabs](https://codelabs.developers.google.com/codelabs/how-to-run-inference-cloud-run-gpu-vllm)
- [Serving Gemma 3 with vLLM on Cloud Run - Google Codelabs](https://codelabs.developers.google.com/devsite/codelabs/serve-gemma3-with-vllm-on-cloud-run)
- [Scale-to-Zero LLM Inference with vLLM + Cloud Run + Cloud Storage FUSE](https://medium.com/google-cloud/scale-to-zero-llm-inference-with-vllm-cloud-run-and-cloud-storage-fuse-42c7e62f6ec6)
- [Qwen2 Deployment Notebook - Google Cloud](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/model_garden/model_garden_pytorch_qwen2_deployment.ipynb)
- [Choose an open model serving option - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/open-models/choose-serving-option)
- [Qwen models on Vertex AI - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/qwen)
- [NVIDIA L4 GPU cost in 2025 - Modal Blog](https://modal.com/blog/nvidia-l4-price-article)
- [Cloud Run RTX 6000 Pro GPUs - Google Cloud Blog](https://cloud.google.com/blog/products/serverless/cloud-run-supports-nvidia-rtx-6000-pro-gpus-for-ai-workloads/)
- [Import models to Vertex AI - Google Cloud](https://docs.cloud.google.com/vertex-ai/docs/model-registry/import-model)
