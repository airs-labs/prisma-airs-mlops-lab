# Module 1: ML Fundamentals & HuggingFace

## Overview

Before you can secure an ML pipeline, you need to understand what flows through it. This module is an exploration-driven deep dive into the machine learning model ecosystem -- HuggingFace, model formats, licensing, datasets, and the platform decisions that enterprises face every day.

You will not write code in this module. You will use Claude as a research partner to build the foundational knowledge you need for everything that follows.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/module 1` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Navigate HuggingFace and evaluate models for enterprise use (size, format, license, provenance)
- Understand the security implications of model file formats (safetensors vs pickle)
- Grasp fine-tuning concepts: SFT, LoRA adapters, datasets
- Compare ML platform options and understand cost/performance tradeoffs

## Time Estimate

~1 to 1.5 hours

## Challenges

### 1.1: HuggingFace Orientation

Evaluate models on HuggingFace the way an enterprise security team would. Find candidate models for a cybersecurity advisor chatbot and assess each on architecture, size, format, license, and cost to fine-tune.

**Key tool:** The `huggingface_hub` Python library for programmatic exploration.

### 1.2: The Format Question

This is the challenge that connects directly to why AIRS exists. Explore the difference between **safetensors** and **pickle-based formats**. One is safe by design. The other can execute arbitrary code when loaded.

**Key questions:** What makes pickle dangerous? Why does it still dominate? What percentage of HuggingFace models use each format?

### 1.3: Datasets and Fine-Tuning Concepts

Understand what fine-tuning actually is and what kind of data drives it. Investigate SFT (Supervised Fine-Tuning), LoRA (Low-Rank Adaptation), and why LoRA is dramatically cheaper than full fine-tuning.

**Key insight:** LoRA trains only a small set of adapter weights instead of the full model, reducing GPU requirements by 10-100x.

### 1.4: Platform Landscape

Compare Vertex AI vs raw GCE instances for fine-tuning and serving. Understand the tradeoffs between managed services and self-hosted infrastructure -- cost, GPU options, SLAs, security boundaries.

## Key Concepts

- **HuggingFace** -- The npm/PyPI of the ML world. A registry of models, datasets, and tools
- **Pickle vs Safetensors** -- Pickle can execute arbitrary code on deserialization; safetensors stores only tensor data
- **LoRA** -- Low-Rank Adaptation. Trains a small adapter instead of the full model, merged back for deployment
- **SFT** -- Supervised Fine-Tuning. Teaching an existing model new behavior using instruction/response pairs

## Verification

Run `/verify-1` in Claude Code. This module's verification is quiz-based -- you demonstrate understanding of formats, fine-tuning concepts, platform tradeoffs, and model registry risks.

## What's Next

You now understand the ML landscape. [Module 2: Train Your Model](/modules/2-train-your-model) puts this knowledge into practice with a real LoRA fine-tuning job on Vertex AI.
