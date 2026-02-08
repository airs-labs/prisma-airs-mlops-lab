# Cloud Security Advisor - Model Fine-Tuning

This directory contains scripts for fine-tuning an LLM to become a Cloud Security Advisor using NIST cybersecurity training data.

## Overview

We use **LoRA (Low-Rank Adaptation)** to efficiently fine-tune a small LLM (Qwen2.5-3B or Phi-3.5-mini) on 424k Q&A examples from NIST publications. The result is a chatbot that can answer cloud security questions with NIST-backed guidance.

## Prerequisites

- Python 3.12+
- GPU with 16GB+ VRAM (GCP T4/A100, RTX 3090/4090, or Apple Silicon with 32GB+ RAM)
- uv package manager

## Quick Start

### 1. Install Dependencies

```bash
cd model-tuning
uv sync
```

### 2. Explore the Dataset

```bash
uv run python explore_dataset.py
```

This downloads and analyzes the NIST training data (424k examples).

### 3. Train the Model

**On GCP or NVIDIA GPU:**
```bash
uv run python train_advisor.py \
  --max-steps 1000 \
  --batch-size 2
```

**Quick test run (fewer steps):**
```bash
uv run python train_advisor.py --max-steps 100
```

**With different base model:**
```bash
uv run python train_advisor.py \
  --base-model "microsoft/Phi-3.5-mini-instruct" \
  --max-steps 1000
```

Training ~1000 steps takes approximately:
- 2-3 hours on T4 GPU
- 1-2 hours on A100 GPU
- 4-6 hours on M2 Max

### 4. Test the Model

**Interactive chat:**
```bash
uv run python chat.py
```

**Single question:**
```bash
uv run python chat.py -q "What are the NIST recommendations for S3 bucket security?"
```

**Compare base model vs fine-tuned:**
```bash
# Base model only
uv run python chat.py --adapter-path ""

# Fine-tuned model
uv run python chat.py --adapter-path models/cloud-security-advisor/final_adapter
```

## File Structure

```
model-tuning/
├── pyproject.toml        # Dependencies
├── explore_dataset.py    # Dataset analysis script
├── train_advisor.py      # LoRA fine-tuning script
├── chat.py              # Interactive chat for testing
├── data/
│   └── nist_sample.json # Sample training examples
├── models/
│   └── cloud-security-advisor/
│       ├── final_adapter/    # LoRA weights
│       └── training_config.json
└── model_tuning/        # Package placeholder
```

## Training Configuration

Key parameters in `train_advisor.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_model` | `Qwen/Qwen2.5-3B-Instruct` | Base LLM to fine-tune |
| `max_samples` | 50,000 | Training examples to use |
| `max_steps` | 1,000 | Training iterations |
| `lora_r` | 16 | LoRA rank |
| `lora_alpha` | 32 | LoRA scaling factor |
| `use_4bit` | true | Enable QLoRA (saves VRAM) |

## Hardware Requirements

| Setup | VRAM | Training Time (1k steps) |
|-------|------|-------------------------|
| GCP T4 | 16GB | ~2-3 hours |
| GCP A100 | 40GB | ~1-2 hours |
| RTX 4090 | 24GB | ~1-2 hours |
| M2 Max 32GB | Unified | ~4-6 hours |

## Troubleshooting

### Out of Memory (OOM)
- Reduce batch size: `--batch-size 1`
- Ensure 4-bit is enabled (default)
- Use a smaller model

### Slow Training
- Check GPU utilization: `nvidia-smi`
- Increase batch size if VRAM allows
- Use gradient checkpointing (enabled by default)

### Model Not Learning
- Increase max steps
- Check learning rate (default 2e-4 is usually good)
- Verify dataset is loading correctly

## Dataset Details

**Source:** [ethanolivertroy/nist-cybersecurity-training](https://huggingface.co/datasets/ethanolivertroy/nist-cybersecurity-training)

| Metric | Value |
|--------|-------|
| Total examples | 424,729 |
| Format | System/User/Assistant messages |
| Avg length | ~1,600 chars |
| Content | NIST 800 series, FIPS, SP, IR documents |

Example Q&A:
```
User: What are the NIST recommendations for identifier management?
Assistant: Control IA-4 (IDENTIFIER MANAGEMENT) requires organizations to:
a. Receive authorization to assign identifiers
b. Select appropriate identifiers
c. Assign identifiers to the intended party
d. Prevent reuse of identifiers...
```
