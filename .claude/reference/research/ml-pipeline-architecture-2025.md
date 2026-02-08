# Modern ML Fine-Tuning Pipeline Architecture & Best Practices (2025-2026)

> Research compiled February 2026 | Sources: 60+ industry publications, documentation, and technical guides

---

## Table of Contents

1. [Enterprise ML Pipeline Architecture](#1-enterprise-ml-pipeline-architecture)
2. [Fine-Tuning Approaches](#2-fine-tuning-approaches)
3. [Fine-Tuning Frameworks](#3-fine-tuning-frameworks)
4. [Model Registries](#4-model-registries)
5. [CI/CD for ML](#5-cicd-for-ml)
6. [Model Deployment & Inference Serving](#6-model-deployment--inference-serving)
7. [MLOps Tech Stacks](#7-mlops-tech-stacks)
8. [Model Security Scanning](#8-model-security-scanning)
9. [Container-Based ML Deployment](#9-container-based-ml-deployment)
10. [Enterprise Use Cases](#10-enterprise-use-cases)
11. [Strategic Insights](#11-strategic-insights)

---

## 1. Enterprise ML Pipeline Architecture

### The Seven-Stage Pipeline

Real-world enterprise fine-tuning pipelines follow a structured, multi-stage architecture:

**Stage 1: Data Preparation**
- Source training data from authoritative domain sources
- Establish format consistency (input structure, output format, metadata annotation)
- Apply data augmentation (paraphrasing, synthetic samples, edge case variations)
- Quality over quantity: 1,000 high-quality examples beat 100,000 mediocre ones

**Stage 2: Model Selection & Initialization**
- Select a base model appropriate for the task (LLM, SLM, or domain-specific transformer)
- Fine-tuning a general model into a domain expert requires only a few thousand targeted examples vs. millions for training from scratch
- Consider architecture requirements (Transformer variants, MoE models, multimodal)

**Stage 3: Training & Hyperparameter Tuning**
- Push training data to a controlled hub
- Data scientists initiate fine-tuning via an endpoint or script, passing dataset location, training parameters (batch size, epochs), and encryption keys
- Logs and metrics (training loss, validation accuracy) are recorded throughout
- AdamW optimizer typically works well; specialized optimizers for certain architectures

**Stage 4: Model Evaluation**
- Query the fine-tuned model for accuracy, latency, and token usage
- Analyze interpretability/explainability for quality and bias assessment
- Iterate on hyperparameter adjustments and data refinements

**Stage 5: Security Scanning & Compliance**
- Scan model artifacts for serialization attacks, supply chain vulnerabilities, and CVEs
- Enforce policy-based deployment gates
- Generate SBOM/AIBOM and artifact signatures

**Stage 6: Deployment & Promotion**
- Staged promotion through Dev -> Test -> Prod environments
- Start with shadow testing (compare predictions against existing system)
- Progress to canary release for safe production rollout

**Stage 7: Continuous Monitoring & Retraining**
- Automated drift detection
- Periodic retraining cycles (3-6 months or triggered by performance degradation)
- Automated pipelines that incorporate new data while preserving existing capabilities

### Enterprise Architecture Pattern: Hub/Spoke

The dominant enterprise pattern (as described by Microsoft) uses a Hub/Spoke architecture:

- Data scientists submit training datasets via automated pipelines and initiate training jobs using secure APIs
- Data scientists do NOT have direct login access to the Hub
- This strict boundary protects raw data and ensures compliance
- After fine-tuning in the Hub, models deploy to Spoke resources (distinct endpoints for production/testing)
- Hub -> Spoke deployment flow can traverse different subscriptions or tenants

**Sources:**
- [Dextra Labs: Fine Tuning LLMs in 2025](https://dextralabs.com/blog/fine-tuning-llm/)
- [SaM Solutions: LLM Fine-Tuning Architecture](https://sam-solutions.com/blog/llm-fine-tuning-architecture/)
- [Microsoft: Enterprise Best Practices for Fine-Tuning Azure OpenAI Models](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/enterprise-best-practices-for-fine-tuning-azure-openai-models/4382540)
- [Neptune.ai: Building End-to-End ML Pipeline](https://neptune.ai/blog/building-end-to-end-ml-pipeline)
- [lakeFS: MLOps Pipeline Types, Components & Best Practices](https://lakefs.io/mlops/mlops-pipeline/)
- [Clarifai: ML Pipeline Stages, Architecture & Best Practices](https://www.clarifai.com/blog/ml-pipeline)
- [Google Cloud: Building a Production Multimodal Fine-Tuning Pipeline](https://cloud.google.com/blog/topics/developers-practitioners/building-a-production-multimodal-fine-tuning-pipeline)

---

## 2. Fine-Tuning Approaches

### Parameter-Efficient Fine-Tuning (PEFT) Dominates Production

**LoRA (Low-Rank Adaptation)** is the most widely used PEFT method:
- Freezes pretrained model weights
- Injects trainable low-rank decomposition matrices into transformer layers
- Trains small adapter matrices (~1-5% of original parameters)
- Dramatically reduces memory requirements while preserving base model capabilities
- Uses 16-bit precision

**QLoRA** extends LoRA with 4-bit quantization:
- Uses NF4 (Normal Float 4-bit) quantization
- Makes 70B parameter models trainable on 24GB VRAM
- A 7B model normally requiring 14GB drops to ~3.5GB in 4-bit format
- 4x less VRAM than LoRA with marginally less accuracy
- No discernible reduction in quality of generated text compared to LoRA

**Full Fine-Tuning:**
- Updates all model parameters
- Best performance but requires substantial computational resources
- 7B model requires 100-120GB VRAM (~$50K in H100s)
- Reserved for cases where PEFT methods are insufficient

### Production-Recommended Hyperparameters

| Parameter | Recommended Value | Notes |
|-----------|-------------------|-------|
| Learning Rate | 2e-4 (LoRA/QLoRA) | 5e-6 for RL (DPO, GRPO) |
| Epochs | 1-3 | >3 risks overfitting for instruction tuning |
| Rank (r) | 8-16 (start), up to 64 | Higher rank = more capacity + more memory |
| Alpha (lora_alpha) | 2x rank | Common heuristic (e.g., r=8, alpha=16) |
| Target Modules | All linear layers | q_proj, v_proj, k_proj, o_proj + MLP layers |
| Dropout | 0 | Not found to be useful for LoRA |
| Batch Size | 16 effective | Via gradient accumulation if needed |
| LR Scheduler | Cosine | Standard choice |

### Key Best Practices

- Train on completions only (mask inputs/prompts) for ~1% accuracy improvement
- Mix 20-30% general data with task-specific data to prevent catastrophic forgetting
- Use gradient checkpointing to reduce VRAM at cost of ~20% speed
- LoRA adapters can be merged with base weights for zero inference latency overhead
- Adapters can be hotswapped dynamically for multi-tenant serving
- Start simple: single GPU, QLoRA, standard tools, then scale as needed

### Cost Comparison

| Approach | Hardware Required | Approximate Cost |
|----------|-------------------|-----------------|
| Full fine-tuning (7B) | 100-120GB VRAM (H100s) | ~$50,000 |
| LoRA (7B) | 48GB VRAM (A6000) | ~$4,000 |
| QLoRA (7B) | 24GB VRAM (RTX 4090) | ~$1,500 |
| QLoRA (70B) | 80GB VRAM (A100) | ~$15,000 |

**Sources:**
- [Databricks: Efficient Fine-Tuning with LoRA Guide](https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms)
- [Introl: Fine-Tuning Infrastructure at Scale](https://introl.com/blog/fine-tuning-infrastructure-lora-qlora-peft-scale-guide-2025)
- [Unsloth: LoRA Hyperparameters Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- [Towards AI: Complete LLM Fine-Tuning Guide](https://pub.towardsai.net/the-complete-llm-fine-tuning-guide-from-beginner-to-production-lora-qlora-peft-034dbef4148d)
- [HuggingFace PEFT Docs](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)
- [HuggingFace PEFT GitHub](https://github.com/huggingface/peft)

---

## 3. Fine-Tuning Frameworks

### Framework Comparison (2025)

| Feature | Axolotl | Unsloth | LLaMA-Factory | HF TRL/SFTTrainer | Torchtune |
|---------|---------|---------|---------------|-------------------|-----------|
| **Best For** | Flexibility, alignment | Speed, low VRAM | Ease of use, no-code | Production control | Deep customization |
| **Multi-GPU (OSS)** | Yes (FSDP/DeepSpeed) | No (paid only) | Yes | Yes | Yes |
| **Speed** | Moderate | 2-5x faster | Moderate | Standard | Fast |
| **VRAM Efficiency** | Standard | Up to 80% less | Standard | Standard | Standard |
| **UI** | CLI/YAML | Notebooks/Studio | Web UI (LlamaBoard) | Python API | Python API |
| **LoRA/QLoRA** | Yes | Yes | Yes | Yes | Yes |
| **RLHF/DPO** | Yes | Yes | Yes | Yes | Yes |
| **Config** | YAML-based | Python/Notebooks | CLI + Web UI | Python code | Python code |

### Axolotl -- Best for Flexibility & Alignment

- Built on HuggingFace Transformers with clean YAML configuration
- Supports full fine-tuning, LoRA, QLoRA, ReLoRA, GPTQ
- Compatible with xFormers, FlashAttention, ROPE scaling, Liger kernel, sample packing
- Scales to multi-GPU with FSDP or DeepSpeed
- Quick to support new models (LLaMA 4, Qwen2.5, etc.)
- Exports to HuggingFace formats; integrates with W&B

### Unsloth -- Best for Speed & Memory Efficiency

- 2-5x faster training, up to 80% less VRAM
- Custom attention implementation in Triton (OpenAI's GPU kernel language)
- 24% faster than Torchtune with PyTorch compile on RTX 4090
- Supports LLaMA (1-4), Gemma 3, Mistral, Phi-4, Qwen 2.5, DeepSeek V3/R1
- **Limitation:** Multi-GPU only in paid tiers (OSS is single-GPU only)

### LLaMA-Factory -- Best for Ease of Use & No-Code

- Zero-code experience with CLI and web-based LlamaBoard UI
- Supports 100+ different models
- Methods: pre-training, SFT, reward modeling, PPO, DPO
- 32-bit full-tuning, 16-bit freeze/LoRA, 2/4/8-bit QLoRA
- Can integrate Unsloth as "acceleration operator"
- Works out of the box without dependency issues

### Production Recommendation

Start with Axolotl or LLaMA-Factory for rapid experimentation. Graduate to HuggingFace PEFT + TRL/SFTTrainer for production control. Use Unsloth when hardware-constrained on a single GPU.

**Sources:**
- [Hyperbolic: Comparing Fine-Tuning Frameworks](https://www.hyperbolic.ai/blog/comparing-finetuning-frameworks)
- [Spheron: Comparing LLM Fine-Tuning Frameworks](https://blog.spheron.network/comparing-llm-fine-tuning-frameworks-axolotl-unsloth-and-torchtune-in-2025)
- [Modal: Best Frameworks for Fine-Tuning LLMs in 2025](https://modal.com/blog/fine-tuning-llms)
- [Sider: Unsloth vs LLaMA-Factory](https://sider.ai/blog/ai-tools/unsloth-vs_llama-factory-which-one-makes-fine-tuning-less-painful)
- [Superteams: Guide to Fine-Tuning with Axolotl and LLaMA-Factory](https://www.superteams.ai/blog/a-definitive-guide-to-fine-tuning-llms-using-axolotl-and-llama-factory)

---

## 4. Model Registries

### Registry Landscape Comparison

| Registry | Type | Model Versioning | Experiment Tracking | Access Mgmt | Hosting | Best For |
|----------|------|-----------------|--------------------|-----------|---------|---------
| **MLflow** | Open-source (+ Databricks) | Yes (stage transitions) | Yes | Limited | Self-hosted or managed | Lifecycle management |
| **Weights & Biases** | Proprietary SaaS | Yes | Yes (strong) | Yes | Fully managed | Experiment tracking |
| **HuggingFace Hub** | Open platform | Yes (Git-based) | Limited | Yes (Orgs) | Managed + Enterprise | Community, model sharing |
| **AWS SageMaker** | Cloud-native | Yes | Via MLflow | IAM/CloudTrail | AWS managed | AWS-native shops |
| **Azure ML** | Cloud-native | Yes | Yes | Azure AD | Azure managed | Microsoft ecosystem |
| **GCP Vertex AI** | Cloud-native | Yes | Yes | GCP IAM | GCP managed | BigQuery/GCP shops |
| **OCI Registries** | Open standard | Tags + digests | No | RBAC (via registry) | Any OCI registry | Cloud-native infra |

### OCI Registries: The Emerging Universal Standard

OCI artifacts for ML models are rapidly becoming a universal packaging standard:

**Docker Model Runner** (GA September 2025):
- Packages LLMs as OCI artifacts using familiar push/pull workflows
- Supports GGUF (via llama.cpp) and Safetensors (via vLLM)
- Each layer contains a single raw file for memory mapping efficiency
- Model configuration JSON includes size, parameter count, quantization, provenance

**KAITO (Kubernetes AI Toolchain Operator):**
- CNCF Sandbox project for Kubernetes-native model deployment
- Split architecture: base images for runtime, OCI artifacts for weights
- Uses ORAS with zstd compression (superior for large model files)
- Automates compute provisioning alongside model deployment

**CNCF ModelPack Specification** (June 2025):
- First vendor-neutral open standard for packaging ML artifacts as OCI objects
- Facilitates reproducibility, portability, and vendor neutrality
- Implemented by AIKit

**ORAS (OCI Registry As Storage):**
- CLI for pushing/pulling non-container OCI artifacts to any OCI registry
- Foundation tool used by KAITO, KitOps, and other ML tooling

**KitOps:**
- Docker-like CLI (kit pack, kit push, kit pull)
- Packages entire ML projects (model, code, data, configs) as single OCI artifact
- Native HuggingFace integration with automatic metadata generation
- CNCF Sandbox project (May 2025), 150K+ downloads

**Harbor + ORMB (ByteDance):**
- Enterprise registry with RBAC, identity integration, security policies
- Docker-like push/pull for model lifecycle management

**Kubernetes 1.31+:**
- Image Volume Source (KEP-4639): native support for mounting OCI artifacts as read-only volumes
- Eliminates init-container pattern for model fetching

**HuggingFace + OCI Convergence:**
- HuggingFace now supports on-demand conversion to Docker Model Artifact format via `docker model pull`

**Sources:**
- [Docker: Why Docker Chose OCI Artifacts for AI Model Packaging](https://www.docker.com/blog/oci-artifacts-for-ai-model-packaging/)
- [KAITO: Model As OCI Artifacts](https://kaito-project.github.io/kaito/docs/next/model-as-oci-artifacts/)
- [CNCF: How OCI Artifacts Will Drive Future AI Use Cases](https://www.cncf.io/blog/2025/08/27/how-oci-artifacts-will-drive-future-ai-use-cases/)
- [CNCF: Standardizing AI/ML Workflows on Kubernetes](https://www.cncf.io/blog/2025/07/26/standardizing-ai-ml-workflows-on-kubernetes-with-kitops-cog-and-kaito/)
- [Gorkem Ercan: The State of OCI Artifacts for AI/ML](https://www.gorkem-ercan.com/p/the-state-of-oci-artifacts-for-aiml)
- [ORAS Documentation](https://oras.land/docs/)
- [Neptune.ai: ML Model Registry Ultimate Guide](https://neptune.ai/blog/ml-model-registry)
- [La Javaness: Evaluation of 4 Model-Hub Platforms](https://www.lajavaness.com/post/%C3%A9valuation-de-4-plateformes-model-hubs-hugging-face-mlflow-datahub-et-weights-biases-1?lang=en)

---

## 5. CI/CD for ML

### Modern ML CI/CD Architecture

The dominant pattern separates into two primary stages:

**CI & Continuous Training (CT):**
- Code validation (linting, unit tests on model source code)
- Data validation (schema conformance, distribution checks)
- Model training triggered by Git events (push, PR)
- Experiment tracking (metrics, hyperparameters logged)
- Model evaluation against acceptance criteria

**Continuous Delivery (CD):**
- Containerization (Docker image with model + serving layer)
- Security scanning (CVE scan, model serialization scan)
- Image publication to container registry (versioned, signed)
- Staged deployment (Dev -> Test -> Prod)
- Canary/shadow deployment with rollback capability

### GitHub Actions for ML Pipelines

GitHub Actions is the most widely adopted CI/CD platform for ML pipelines:

**Workflow Structure:**
```
Trigger (push/PR) --> Lint & Test --> Data Validation --> Training Job
  --> Model Evaluation --> Security Scan --> Build Container
  --> Push to Registry --> Deploy (staged)
```

**Best Practices:**
- Separate workflows by concern: training, serving, documentation
- Use event-driven triggers wisely (PR for validation, push to main for deployment)
- Gate deployments on model performance metrics
- Use GitHub Secrets for credentials, never inline values
- Leverage community actions from GitHub Marketplace (11,000+ available)

**Key Integrations:**
- **CML (Continuous Machine Learning)** -- Open-source tool for automating model training, evaluation, and report generation within GitHub Actions
- **DVC (Data Version Control)** -- Git-friendly dataset and model versioning
- **Azure ML CLI** -- Direct integration for training models in Azure Machine Learning
- **Argo Workflows** -- Orchestrating ML pipelines on Kubernetes
- **Weights & Biases** -- Experiment tracking integration

**Cost Optimization:**
- Arm64 runners: 37% cheaper than x64 runners, optimized for ML workloads
- Reduced training times, lower power consumption, scalable for larger datasets

### Training Trigger Patterns

1. **Automated post-CI:** Training pipeline triggers automatically after CI passes
2. **Ad-hoc manual:** For expensive training, data scientists decide when to train (via `workflow_dispatch`)
3. **Data-driven:** Triggered by new data availability or drift detection
4. **Scheduled:** Periodic retraining on a cron schedule

### Multi-Pipeline Architecture

Recommended pipeline separation:
1. **Gate 1: Train** -- Triggered by code/data changes, runs training, logs metrics
2. **Gate 2: Publish** -- Triggered by training success, scans model, publishes artifacts
3. **Gate 3: Deploy** -- Triggered by artifact publication, deploys to staging/production

**Sources:**
- [Victoria Lo: CI/CD Pipelines with GitHub Actions for MLOps](https://lo-victoria.com/implementing-cicd-pipelines-with-github-actions-for-mlops)
- [GitHub Blog: Build CI/CD Pipeline with GitHub Actions](https://github.blog/enterprise-software/ci-cd/build-ci-cd-pipeline-github-actions-four-steps/)
- [Made With ML: CI/CD for Machine Learning](https://madewithml.com/courses/mlops/cicd/)
- [GitHub Blog: MLOps Pipeline with Arm64 Runners](https://github.blog/enterprise-software/ci-cd/streamlining-your-mlops-pipeline-with-github-actions-and-arm64-runners/)
- [Microsoft: GitHub Actions for Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-github-actions-machine-learning?view=azureml-api-2)
- [Medium: Automate ML and LLM Workflow with GitHub Actions & CML](https://medium.com/@abonia/automate-ml-and-llm-workflow-with-github-actions-cml-1673c9544c3c)

---

## 6. Model Deployment & Inference Serving

### Inference Serving Framework Comparison (2025)

| Dimension | vLLM | TGI | Triton (+TRT-LLM) | SGLang | LMDeploy |
|-----------|------|-----|-------------------|--------|----------|
| **Throughput** | Highest at high concurrency | Competitive; excels on long prompts | Highest single-request perf | Optimized for agents/RAG | Max throughput per GPU |
| **Latency (TTFT)** | Best across concurrency levels | Lower tail latency single-user | Very low single-request | Good for multi-turn | Good |
| **Setup** | Easy, Python-native | Easy, HF ecosystem | Most complex | Moderate | Easy |
| **Multi-model** | LLM-focused | LLM-focused | Full multi-framework | LLM-focused | LLM-focused |
| **Quantization** | GPTQ, AWQ, GGUF, FP8 | bitsandbytes, GPTQ | FP8, INT8 (HW-optimized) | Various | TurboMind |
| **Best Fit** | General-purpose, high-concurrency | HF teams, long-context chat | Enterprise multi-model | Agents, tool chains | Quantized model serving |

### vLLM -- The Default Choice

- **PagedAttention** for up to 24x higher throughput vs. TGI under high concurrency
- Continuous batching, FP8 KV quantization
- Native HuggingFace compatibility (direct model loading from Hub and S3)
- At 100 concurrent users: 4,741 tokens/s (vs TRT-LLM at 1,942 tokens/s)
- Best TTFT across all concurrency levels in BentoML benchmarks
- **llm-d project** (Red Hat, Google Cloud, IBM, NVIDIA, CoreWeave): Kubernetes-native distributed serving on top of vLLM

### HuggingFace TGI -- For Long-Context Workloads

- TGI v3: 13x speedup on 200K+ token prompts vs. vLLM
- 3x more tokens in same GPU memory via chunking
- Prefix caching for conversation-style traffic
- Paged attention-style kernels with chunked prefill

### NVIDIA Triton -- For Multi-Model Platforms

- Framework-agnostic (PyTorch, TensorFlow, ONNX, custom backends)
- Multi-model serving, model ensembles, dynamic batching
- vLLM as backend (since 23.10), TensorRT-LLM integration
- Most comprehensive for complex multi-model environments
- Trade-off: most complex setup

### Model Formats for Deployment

| Format | Primary Use | Ecosystem | Security |
|--------|-------------|-----------|----------|
| **Safetensors** | Cloud serving, training | HuggingFace, vLLM, PyTorch | Safe (data only) |
| **GGUF** | Local/edge inference | llama.cpp, Ollama | Safe (weights + metadata) |
| **ONNX** | Cross-framework interop | Broad | Safe (recommended over Pickle) |
| **Pickle/PT** | Legacy | PyTorch | UNSAFE (arbitrary code exec) |

**Sources:**
- [Red Hat: Why vLLM is the Best Choice for AI Inference](https://developers.redhat.com/articles/2025/10/30/why-vllm-best-choice-ai-inference-today)
- [Modal: vLLM vs. TGI](https://modal.com/blog/vllm-vs-tgi-article)
- [MarkTechPost: Comparing Top 6 Inference Runtimes 2025](https://www.marktechpost.com/2025/11/07/comparing-the-top-6-inference-runtimes-for-llm-serving-in-2025/)
- [MarkTechPost: vLLM vs TensorRT-LLM vs TGI vs LMDeploy](https://www.marktechpost.com/2025/11/19/vllm-vs-tensorrt-llm-vs-hf-tgi-vs-lmdeploy-a-deep-technical-comparison-for-production-llm-inference/)
- [BentoML: Benchmarking LLM Inference Backends](https://bentoml.com/blog/benchmarking-llm-inference-backends)
- [arxiv: Comparative Analysis of vLLM and TGI](https://arxiv.org/html/2511.17593v1)
- [Koyeb: Best LLM Inference Engines](https://www.koyeb.com/blog/best-llm-inference-engines-and-servers-to-deploy-llms-in-production)
- [vLLM Blog: Docker Model Runner Integrates vLLM](https://blog.vllm.ai/2025/11/19/docker-model-runner-vllm.html)

---

## 7. MLOps Tech Stacks

### Best Practice Stack Combinations (2025-2026)

#### Startup / Small Team Stack
| Category | Tool |
|----------|------|
| Experiment Tracking | MLflow or W&B (free tier) |
| Fine-tuning | Unsloth or LLaMA-Factory |
| Model Registry | HuggingFace Hub |
| CI/CD | GitHub Actions |
| Serving | vLLM |
| Monitoring | Evidently AI (open source) |

#### Mid-Scale Enterprise Stack
| Category | Tool |
|----------|------|
| Experiment Tracking | MLflow + W&B |
| Fine-tuning | Axolotl or HuggingFace TRL |
| Pipeline Orchestration | Kubeflow or Metaflow |
| Model Registry | MLflow Model Registry |
| Data Versioning | DVC or lakeFS |
| CI/CD | GitHub Actions + CML |
| Serving | vLLM + Triton |
| Monitoring | Arize AI or WhyLabs |

#### Cloud-Native Enterprise (AWS)
| Category | Tool |
|----------|------|
| End-to-End | SageMaker (Pipelines, Registry, Endpoints) |
| Experiment Tracking | SageMaker + MLflow |
| CI/CD | GitHub Actions + SageMaker Pipelines |
| Serving | SageMaker Endpoints (Triton for GPU multi-model) |
| Monitoring | SageMaker Model Monitor + CloudWatch |

#### Cloud-Native Enterprise (Azure)
| Category | Tool |
|----------|------|
| End-to-End | Azure ML |
| CI/CD | GitHub Actions + Azure ML CLI |
| Model Registry | Azure ML Registry |
| Serving | Azure ML Managed Endpoints |

#### Cloud-Native Enterprise (GCP)
| Category | Tool |
|----------|------|
| End-to-End | Vertex AI |
| CI/CD | GitHub Actions + Vertex AI Pipelines |
| Serving | Vertex AI Endpoints |
| Data | BigQuery integration |

#### Databricks-Centric Stack
| Category | Tool |
|----------|------|
| Platform | Databricks Mosaic AI |
| Governance | Unity Catalog |
| Experiment Tracking | MLflow (native integration) |
| Agent Framework | Mosaic AI Agent Framework |
| Serving | Databricks Model Serving |

### Key Categories and Tool Leaders

| Category | Leaders |
|----------|---------|
| Experiment Tracking | MLflow, Weights & Biases, ClearML |
| Pipeline Orchestration | Kubeflow, Metaflow, SageMaker Pipelines, Kedro |
| Data/Model Versioning | DVC, lakeFS, Pachyderm |
| Feature Stores | Tecton, Feast |
| Model Registry | MLflow, SageMaker, HuggingFace Hub |
| Monitoring/Observability | Arize AI, WhyLabs, Evidently AI |
| Vector Databases | Qdrant, Pinecone, Weaviate |
| Agent Observability | Arize Phoenix, W&B Weave (Trace Stores) |

### Guiding Principles

- Version everything: code, data, features, models
- Automate tests and promotion gates
- Instrument observability that maps model-level signals to business outcomes
- Start small: experiment tracking + pipeline automation + basic monitoring first
- Prefer tools that export neutral formats (MLflow artifacts, ONNX, Parquet) to avoid vendor lock-in
- MLflow: 40% faster experimentation cycles due to lightweight setup
- Kubeflow: 32% lower deployment time once pipelines stabilize

### 2026 Considerations

- MLOps must now manage LLMs, RAG systems, vector stores, and autonomous agents
- For agent-based systems, prioritize platforms with "Trace Stores" for visualizing full chains of thought
- Many legacy MLOps tools still view the world in terms of simple "inputs" and "predictions"

**Sources:**
- [Rahul Kolekar: MLOps in 2026 Definitive Guide](https://rahulkolekar.com/mlops-in-2026-the-definitive-guide-tools-cloud-platforms-architectures-and-a-practical-playbook/)
- [EasyFlow: MLOps Tech Stack Ultimate Guide 2026](https://easyflow.tech/mlops-tech-stack/)
- [DataCamp: 25 Top MLOps Tools 2026](https://www.datacamp.com/blog/top-mlops-tools)
- [lakeFS: 26 MLOps Tools for 2026](https://lakefs.io/mlops/mlops-tools/)
- [Kellton: AI Tech Stack 2026](https://www.kellton.com/kellton-tech-blog/ai-tech-stack-2026)
- [SG Analytics: Top 20 MLOps Tools in 2026](https://www.sganalytics.com/blog/mlops-tools/)
- [Kubeflow vs MLflow Comparison](https://pratik-rupareliya.medium.com/kubeflow-vs-mlflow-which-one-to-choose-for-your-mlops-workflow-6a8896b544e4)

---

## 8. Model Security Scanning

### Where Security Scanning Fits in the Pipeline

Security scanning integrates at THREE critical pipeline stages:

**Pre-Training Gate:**
- Scan all third-party models before use (training, fine-tuning, evaluation, inference)
- Check for model serialization attacks (Pickle-based Trojan horses)
- Validate data pipeline integrity

**Pre-Deployment Gate (Most Critical):**
- Model artifact scanning (serialization attack detection)
- Container image scanning (CVEs in ML frameworks, dependencies)
- Policy-based deployment blocks
- Adversarial robustness testing
- Bias audits with pass/fail gates
- SBOM/AIBOM generation and artifact signing
- No signature = no deploy

**Runtime Monitoring:**
- Behavioral anomaly detection
- Drift detection
- Prompt injection monitoring
- Data exfiltration detection

### The Threat: Model Serialization Attacks

A Model Serialization Attack is where malicious code is injected into model files during serialization (saving) before distribution. The Python Pickle format is the primary attack vector -- it allows arbitrary code execution when loading models. This is a modern Trojan Horse.

### Key Security Tools

**ModelScan (ProtectAI):**
- Open-source model scanning tool (v0.8.7 as of 2025)
- Reads model files byte-by-byte looking for unsafe code signatures
- Supports H5, Pickle, SavedModel formats (PyTorch, TensorFlow, Keras, Sklearn, XGBoost)
- Exit codes for CI/CD pipeline integration
- Can be used as CLI or Python library
- ProtectAI acquired by Palo Alto Networks (2025)

**ModelAudit (Promptfoo):**
- Broader format support: JSON, YAML, XML, ONNX, SafeTensors, NumPy, PMML
- Configuration file scanning in addition to model files

**Guardian (ProtectAI Enterprise):**
- Enterprise-grade product with organization-wide scanning
- Proactive security: define and enforce requirements for HuggingFace models
- Comprehensive audit trail

**Other Security Tools:**
- Microsoft Counterfit -- Adversarial testing
- IBM Adversarial Robustness Toolbox -- Evasion sample generation
- MITRE ATLAS -- Threat framework for AI systems
- OWASP GenAI -- Security controls for LLM applications
- NIST AI RMF -- Risk management framework

### Format-Level Security

| Format | Security Level | Notes |
|--------|---------------|-------|
| **Safetensors** | SAFE | Data-only, no code execution possible |
| **GGUF** | SAFE | Weights + metadata only, no executable code |
| **ONNX** | SAFE | Recommended over Pickle |
| **Pickle (.pkl, .pt, .pth)** | UNSAFE | Arbitrary code execution on load |
| **torch.save** | UNSAFE | Uses Pickle internally |

### Enterprise SBOM/AIBOM Best Practices

- Require SBOM/AIBOM and artifact signing for all models
- Store models in registries with version pinning
- Sign artifacts and publish SBOM/AI-BOM metadata for downstream verifiers
- Maintain verifiable lineage and attestations
- Policy: no signature, no deploy

**Sources:**
- [ProtectAI: ModelScan GitHub](https://github.com/protectai/modelscan)
- [ProtectAI: ModelScan Product Page](https://protectai.com/modelscan)
- [Promptfoo: ModelAudit vs ModelScan Comparison](https://www.promptfoo.dev/blog/modelaudit-vs-modelscan/)
- [SANS ISC: ModelScan Protection Against Serialization Attacks](https://isc.sans.edu/diary/31692)
- [Microsoft: Securing the AI Pipeline](https://techcommunity.microsoft.com/blog/microsoft-security-blog/securing-the-ai-pipeline-%E2%80%93-from-data-to-deployment/4478457)
- [OpenSSF: Visualizing Secure MLOps](https://openssf.org/blog/2025/08/05/visualizing-secure-mlops-mlsecops-a-practical-guide-for-building-robust-ai-ml-pipeline-security/)
- [CSA: Hidden Security Threats in ML Pipelines](https://cloudsecurityalliance.org/blog/2025/09/11/the-hidden-security-threats-lurking-in-your-machine-learning-pipeline)

---

## 9. Container-Based ML Deployment

### Multi-Stage Docker Build Pattern

The standard production pattern separates build-time and run-time dependencies:

```dockerfile
# Stage 1: Builder -- install dependencies
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Production -- lean runtime with GPU support
FROM nvidia/cuda:12.1-runtime-ubuntu22.04
COPY --from=builder /root/.local /root/.local
COPY model/ /app/model/
COPY serve.py /app/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8080
CMD ["python", "/app/serve.py"]
```

### GPU Inference Container Best Practices

1. **Base Images:** Use NVIDIA base images (`nvidia/cuda:12.x-runtime-ubuntu22.04`)
2. **Model Loading:** Pre-load models during container startup to optimize first-request latency
3. **Dependency Pinning:** Pin Python package versions for reproducibility
4. **Persistent Volumes:** Use persistent storage for model weights (shared access between containers)
5. **Resource Limits:** Set timeouts and resource limits to prevent runaway processes
6. **API Security:** Add authentication layers to inference endpoints
7. **Image Size:** Only include necessary model files to minimize image size
8. **Secrets:** Use HashiCorp Vault or AWS Secrets Manager for runtime key injection (never in images)

### Docker Model Runner (2025)

Docker Desktop's Model Runner enables local LLM execution with GPU acceleration:
- Intelligent routing by format: GGUF -> llama.cpp, Safetensors -> vLLM
- Vulkan support for cross-vendor GPU acceleration (AMD, Intel, integrated GPUs)
- OCI artifact packaging for model distribution
- GA since September 2025

### Enterprise Container Patterns

- **Canary deployments:** Roll out new model versions with automatic rollback on drift detection
- **Observability:** Grafana dashboards for model performance (accuracy, drift) and infrastructure (CPU/GPU, memory, IO)
- **Model weight management:** Use OCI artifacts to separate model weights from inference runtime (the KAITO pattern)
- **Scaling:** Kubernetes HPA based on inference queue depth or GPU utilization

### Serving Frameworks in Containers

| Framework | Key Feature | Container Pattern |
|-----------|-------------|-------------------|
| **vLLM** | High-throughput LLM serving | Single container with PagedAttention |
| **BentoML** | Dynamic batching, multi-model pipelines | Bento packaging with built-in serving |
| **Triton** | Multi-framework, model ensembles | Model repository with version management |
| **FastAPI** | Custom inference APIs | Async endpoints for real-time ML tasks |
| **TGI** | Long-context LLM serving | HF-optimized container images |

**Sources:**
- [RunPod: MLOps Workflow for Docker-Based AI Deployment](https://www.runpod.io/articles/guides/mlops-workflow-docker-ai-deployment)
- [NexAI Tech: Running AI Workloads in Docker 2025](https://nexaitech.com/ai-workloads-in-docker-architecting-for-enterprises/)
- [MarkAICode: Docker Containerization for LLM Applications 2025](https://markaicode.com/docker-containerization-llm-applications-best-practices-2025/)
- [Docker: Introducing Docker Model Runner](https://www.docker.com/blog/introducing-docker-model-runner/)
- [vLLM Blog: Docker Model Runner Integrates vLLM](https://blog.vllm.ai/2025/11/19/docker-model-runner-vllm.html)
- [BentoML GitHub](https://github.com/bentoml/BentoML)

---

## 10. Enterprise Use Cases

### Why Enterprises Fine-Tune

1. **Domain-specific language** -- Off-the-shelf models rarely match domain terminology, workflows, or customer needs
2. **Reducing hallucinations** -- Fine-tuning with high-quality domain data provides a reliable source of truth
3. **Cost and latency optimization** -- Fine-tuned smaller models achieve high-quality results with shorter prompts
4. **Regulatory compliance** -- On-premise fine-tuning in closed environments for sensitive codebases
5. **Competitive advantage** -- AI systems that understand unique business contexts

### Industry Use Cases

**Healthcare & Medical:**
- Clinical note drafting from structured patient data
- Medical terminology understanding (Med-PaLM 2 pattern)
- Drug interaction analysis
- Treatment suggestion based on clinical guidelines
- Diagnostics with fine-tuned SLMs

**Finance & Banking:**
- Earnings report analysis and risk assessment summarization (BloombergGPT pattern)
- Fraud detection with domain-specific patterns
- Regulatory compliance document processing
- Financial NLP: sentiment analysis, NER, news classification

**Legal:**
- Court ruling analysis and case law synthesis
- Contract review and clause extraction/detection
- Regulatory compliance monitoring
- Legal document generation with jurisdiction-specific language

**Customer Service & CX:**
- Sentiment analysis on company-specific feedback
- Brand-voice-aligned response generation
- Multi-language customer support
- Product recommendation with internal catalog knowledge

**Software Engineering:**
- AI-powered code review with internal coding standards
- Enterprise IDE completions trained on proprietary codebases
- Documentation generation from internal APIs
- Bug classification and triage

**Manufacturing & IoT:**
- Predictive maintenance with equipment-specific training data
- Quality control image classification
- Supply chain optimization with proprietary data

### Fine-Tuning vs. RAG: The Hybrid Approach

The gold standard in 2025 is a **hybrid approach**:
- **Fine-tuning** perfects the LLM's underlying skill for the domain (understanding complex instructions, maintaining brand voice, structuring technical output)
- **RAG** grounds that output in current, verified, external facts
- They are complementary, not competing

### The Rise of Small Language Models (SLMs)

A major 2025 trend: fine-tuning SLMs instead of massive LLMs:
- Cheaper and faster to fine-tune
- Easier to deploy on edge devices
- Often sufficient for focused domain tasks
- Particularly attractive for resource-constrained environments
- Models like Mistral 7B, LLaMA 3 8B, IBM Granite deliver comparable accuracy at lower costs
- Purpose-built for domain-specific applications (healthcare diagnostics, financial fraud detection)

### Key Techniques Enabling Enterprise Fine-Tuning

1. **Synthetic Data** -- Train when real domain data is scarce, private, or costly to label
2. **Open-Source Models** -- Mistral, LLaMA, Granite actively fine-tuned for real-world enterprise use
3. **Responsible AI** -- Bias mitigation, fairness checks, regulatory alignment built into pipelines
4. **Data Privacy** -- Strict regulations in healthcare, finance, law require on-premise fine-tuning

**Sources:**
- [AIMultiple: LLM Fine-Tuning Guide for Enterprises 2026](https://research.aimultiple.com/llm-fine-tuning/)
- [Aisera: LLM Fine-Tuning for Enterprise Accuracy 2025](https://aisera.com/blog/fine-tuning-llms/)
- [SuperAnnotate: Fine-Tuning LLMs in 2025](https://www.superannotate.com/blog/llm-fine-tuning)
- [Heavybit: LLM Fine-Tuning Guide for Engineering Teams](https://www.heavybit.com/library/article/llm-fine-tuning)
- [Glean: RAG vs. LLM Fine-Tuning](https://www.glean.com/blog/rag-vs-llm)
- [Red Hat: Rise of Small Language Models in Enterprise AI](https://www.redhat.com/en/blog/rise-small-language-models-enterprise-ai)
- [Amplework: Business-Ready LLM Fine-Tuning in 2025](https://www.amplework.com/blog/llm-fine-tuning-tools-trends-business/)

---

## 11. Strategic Insights

### Second-Order Effects to Consider

**1. OCI Convergence is the Sleeper Trend**
While most attention focuses on MLflow vs. HuggingFace vs. cloud registries, the real strategic shift is OCI artifacts becoming the universal model packaging standard. Teams already invested in container infrastructure (Docker Hub, Harbor, ACR, ECR, GCR) will manage models through the same pipelines, RBAC, and supply chain security they already use for containers. Three moves ahead: the model registry will likely converge with the container registry.

**2. Security Scanning is the New Deployment Bottleneck**
The primary bottleneck in 2026 is not building a prototype -- it is proving the prototype is safe for production. Organizations that build security scanning into CI/CD gates early (ModelScan, Counterfit, SBOM generation) will ship faster than those that bolt it on later. ProtectAI's acquisition by Palo Alto Networks signals mainstreaming.

**3. The LoRA Adapter Economy is Emerging**
When LoRA adapters can be hotswapped at zero latency and stored as OCI artifacts, we move toward a world where the base model is infrastructure and domain-specific adapters are the product. This has implications for model marketplaces, multi-tenant serving, and cost optimization.

**4. Hybrid RAG + Fine-Tuning is Not Optional**
Organizations that treat RAG and fine-tuning as either/or are leaving significant performance on the table. The winning pattern is fine-tuning for domain language and reasoning, RAG for grounding in current facts.

**5. SLMs Change the Economics**
The rise of capable small language models (3B-8B parameters) fine-tuned with QLoRA on a single GPU fundamentally changes the build-vs-buy calculation. Many tasks previously requiring API calls to large proprietary models can now be served with fine-tuned SLMs at a fraction of the cost.

**6. MLOps Must Now Handle Agents**
The 2026 MLOps stack must manage LLMs, RAG systems, vector stores, and autonomous agents. Legacy tools that view the world as "inputs" and "predictions" are insufficient. Trace Stores for visualizing chains of thought are becoming essential.

**7. Kubernetes-Native ML is Maturing**
Between KAITO, Kubernetes 1.31 OCI volume mounts, llm-d for distributed vLLM, and ModelPack, the Kubernetes-native ML deployment story is becoming coherent and production-ready. This reduces the need for specialized ML infrastructure.

---

*Research compiled by Ava Sterling | February 2026*
*Sources: 60+ industry publications, documentation, technical guides, and academic papers*
