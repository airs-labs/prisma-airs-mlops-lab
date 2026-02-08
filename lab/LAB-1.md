# Module 1: ML Fundamentals & HuggingFace

## Overview

Before you can secure an ML pipeline, you need to understand what flows through it. This module is an exploration-driven deep dive into the machine learning model ecosystem -- HuggingFace, model formats, licensing, datasets, and the platform decisions that enterprises face every day. You will not write code in this module. You will use Claude as a research partner to build the foundational knowledge you need for everything that follows.

## Objectives

- Navigate HuggingFace and evaluate models for enterprise use (size, format, license, provenance)
- Understand the security implications of model file formats (safetensors vs pickle)
- Grasp fine-tuning concepts: SFT, LoRA adapters, datasets
- Compare ML platform options and understand cost/performance tradeoffs

## Prerequisites

- Module 0 complete (environment verified, Claude Code configured)
- HuggingFace account created

## Time Estimate

~1 to 1.5 hours

---

## Challenges

### Challenge 1.1: HuggingFace Orientation

You are a security engineer who just learned that your organization is pulling open-source models from HuggingFace. Your job is to evaluate the risk. Start by understanding what HuggingFace is and how enterprises use it.

Use `/explore hf-orientation` in Claude Code for guided exploration.

**Your mission:** Find 3 models on HuggingFace that could serve as a base for a cybersecurity advisor chatbot. For each model, determine:

- What is it? (Architecture, creator, purpose)
- How big is it? (Parameter count, disk size, quantization options)
- What format are the weights stored in? (safetensors, pickle, GGUF, etc.)
- What license does it use? (Apache 2.0, MIT, Llama Community, custom)
- What would it cost to fine-tune and serve on a single GPU?

You are building the evaluation framework that an enterprise security team would use when vetting model downloads.

<details><summary>Hint 1: Concept</summary>

HuggingFace is the npm/PyPI of the ML world -- a massive registry of models, datasets, and tools. Model cards are like package READMEs. Not all models are equal: verified organizations, download counts, and format choices all signal trustworthiness.

</details>

<details><summary>Hint 2: Approach</summary>

Use the `huggingface_hub` Python library to programmatically explore models. Start with `api.model_info("Qwen/Qwen2.5-3B-Instruct")` -- this is the base model used in this lab. Then search for alternatives: `api.list_models(search="cybersecurity", sort="downloads")`. Look at model cards, file listings, and metadata.

</details>

<details><summary>Hint 3: Implementation</summary>

Ask Claude to help you run these explorations:

```python
from huggingface_hub import HfApi
api = HfApi()

# Inspect our base model
info = api.model_info("Qwen/Qwen2.5-3B-Instruct")
print(f"Tags: {info.tags}")
print(f"Downloads: {info.downloads}")
print(f"License: {info.card_data.license if info.card_data else 'unknown'}")

# List files to see formats
files = api.list_repo_tree("Qwen/Qwen2.5-3B-Instruct")
for f in files:
    if hasattr(f, 'size'):
        print(f"{f.rfilename}: {f.size / 1e9:.1f} GB")
```

Compare at least 3 models. Look for differences in format, size, and licensing.

</details>

---

### Challenge 1.2: The Format Question

This is the challenge that connects directly to why AIRS exists.

Explore the difference between **safetensors** and **pickle-based formats** (.bin, .pt, .pkl). These are the two dominant ways model weights are stored. One is safe by design. The other can execute arbitrary code when loaded.

Questions to answer with Claude's help:
- What is pickle serialization and why is it dangerous?
- What is safetensors and how does it prevent code execution?
- What percentage of models on HuggingFace use each format?
- If safetensors is safer, why does pickle still dominate?

This is the seed for Module 6 (The Threat Zoo) where you will build actual malicious pickle models and watch AIRS catch them.

<details><summary>Hint 1: Concept</summary>

Pickle is Python's native serialization format. It can serialize *any Python object* -- including objects that execute code when deserialized. When you call `torch.load()` on a pickle file, you are running arbitrary code from whoever created that file. Safetensors was designed specifically to avoid this: it stores only tensor data, no executable code.

</details>

<details><summary>Hint 2: Approach</summary>

Ask Claude to explain pickle deserialization attacks (the `__reduce__` method). Then look at a real model on HuggingFace -- check whether it has `.safetensors` files, `.bin` files, or both. Many models provide both formats for compatibility.

</details>

<details><summary>Hint 3: Implementation</summary>

Explore format distribution on HuggingFace:

```python
from huggingface_hub import HfApi
api = HfApi()

# Check files for a popular model
files = list(api.list_repo_tree("Qwen/Qwen2.5-3B-Instruct"))
for f in files:
    if hasattr(f, 'rfilename'):
        ext = f.rfilename.split('.')[-1] if '.' in f.rfilename else 'none'
        if ext in ('safetensors', 'bin', 'pt', 'pkl', 'gguf'):
            print(f"  {f.rfilename} ({ext})")
```

Ask Claude: "Why did the ML community create safetensors? What incidents drove its adoption?" The answer connects to real supply chain attacks you will study in Module 6.

</details>

---

### Challenge 1.3: Datasets and Fine-Tuning Concepts

You are about to fine-tune a model to be a cybersecurity advisor. Before you do, you need to understand what fine-tuning actually is and what kind of data drives it.

Use `/explore datasets-finetuning` in Claude Code for guided exploration.

Questions to investigate:
- What kind of dataset would you need for a cybersecurity advisor chatbot?
- What does a training dataset actually look like? (Format, schema, examples)
- What is SFT (Supervised Fine-Tuning) and how does it differ from pre-training?
- What is LoRA and why is it dramatically cheaper than full fine-tuning?
- If you needed to create a custom dataset and none existed, how would you do it?

<details><summary>Hint 1: Concept</summary>

Fine-tuning teaches an existing model new behavior using instruction/response pairs. LoRA (Low-Rank Adaptation) is a technique that trains only a small set of "adapter" weights instead of the full model -- reducing GPU requirements by 10-100x. The adapter is later merged back into the base model for deployment.

</details>

<details><summary>Hint 2: Approach</summary>

Look at the dataset this lab uses: `ethanolivertroy/nist-cybersecurity-training` on HuggingFace. Examine its format and a few example rows. Then compare LoRA parameter counts vs full fine-tuning: for a 3B parameter model, LoRA might add only 10-50M trainable parameters.

</details>

<details><summary>Hint 3: Implementation</summary>

```python
from huggingface_hub import HfApi
api = HfApi()

# Look at the training dataset
ds_info = api.dataset_info("ethanolivertroy/nist-cybersecurity-training")
print(f"Dataset: {ds_info.id}")
print(f"Downloads: {ds_info.downloads}")
print(f"Tags: {ds_info.tags}")
```

Ask Claude: "Walk me through what LoRA actually does. How many parameters does it add to a 3B model? Why is that cheaper than training the full 3B?" Then ask: "What are the security implications of training data? Could someone poison a dataset?"

</details>

---

### Challenge 1.4: Platform Landscape

When an enterprise decides to fine-tune and serve a model, they have to choose a platform. This challenge is about understanding those tradeoffs -- the same conversation you would have with a customer.

Use `/explore platform-landscape` in Claude Code for guided exploration.

**Compare:** Vertex AI vs a raw GCE instance with a GPU for fine-tuning Qwen 3B.

Consider:
- Cost per training run (managed service markup vs raw compute)
- GPU options (A100, L4, T4) -- when to use which
- Inference hosting: Vertex AI endpoint vs self-hosted vLLM on GCE
- Enterprise concerns: SLAs, autoscaling, security boundaries, audit logging
- Why this lab chose: Vertex AI CustomJob for training, Vertex AI endpoint with vLLM for serving, Cloud Run for the application

<details><summary>Hint 1: Concept</summary>

Managed services (Vertex AI) cost more per GPU-hour but handle infrastructure, scaling, monitoring, and security boundaries. Raw compute (GCE) is cheaper but you manage everything yourself. The right choice depends on the customer's team size, compliance requirements, and operational maturity.

</details>

<details><summary>Hint 2: Approach</summary>

Look at GCP pricing for GPU instances. An A100 on GCE costs roughly $3-4/hr. The same A100 via Vertex AI CustomJob costs about the same for compute but adds Vertex AI management overhead. The real cost difference is in *inference* -- a dedicated Vertex AI endpoint vs a self-managed GCE instance running vLLM.

</details>

<details><summary>Hint 3: Implementation</summary>

Ask Claude to help you build a cost comparison table:

| Dimension | Vertex AI | GCE (Self-Managed) |
|-----------|-----------|---------------------|
| Training cost (1 hr, A100) | ? | ? |
| Inference cost (24/7, L4) | ? | ? |
| Setup complexity | ? | ? |
| Autoscaling | ? | ? |
| Security posture | ? | ? |

Then ask: "Why did this lab choose Vertex AI endpoints with vLLM instead of putting the model directly in the Cloud Run container?" The answer is about separating compute-heavy inference from lightweight application logic.

</details>

---

## Verification

Run `/verify-1` in Claude Code. The verification is quiz-based -- you demonstrate understanding rather than checking infrastructure:

- Articulate the difference between safetensors and pickle formats and the security implications
- Explain what LoRA is and why it is cheaper than full fine-tuning
- Describe the tradeoffs between managed ML platforms and raw GPU compute
- Name at least one risk of pulling models from a public registry like HuggingFace

## Customer Talking Points

- "When a customer tells you they are pulling models from HuggingFace, ask: What format? What license? From which organization? How are they validating what they download? Most cannot answer these questions. That is the opening for AIRS."
- "Fine-tuning is where customers introduce their own data into a model. That is also where data poisoning risk begins. Understanding the training pipeline is the first step to securing it."
- "Customers often ask about GPU costs. The architecture choice -- managed endpoint vs self-hosted -- has security implications too. Managed endpoints have different attack surfaces than self-hosted containers."

## What's Next

You now understand the ML landscape -- models, formats, datasets, and platforms. In Module 2, you will put this knowledge into practice by training your own cybersecurity advisor model using LoRA fine-tuning on Vertex AI. You will trigger a real training pipeline and watch it run.
