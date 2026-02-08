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

### Challenge 1.2: The Format Question

This is the challenge that connects directly to why AIRS exists.

Explore the difference between **safetensors** and **pickle-based formats** (.bin, .pt, .pkl). These are the two dominant ways model weights are stored. One is safe by design. The other can execute arbitrary code when loaded.

This is the seed for Module 6 (The Threat Zoo) where you will build actual malicious pickle models and watch AIRS catch them.

### Challenge 1.3: Datasets and Fine-Tuning Concepts

You are about to fine-tune a model to be a cybersecurity advisor. Before you do, you need to understand what fine-tuning actually is and what kind of data drives it.

Use `/explore datasets-finetuning` in Claude Code for guided exploration.

### Challenge 1.4: Platform Landscape

When an enterprise decides to fine-tune and serve a model, they have to choose a platform. This challenge is about understanding those tradeoffs -- the same conversation you would have with a customer.

Use `/explore platform-landscape` in Claude Code for guided exploration.

---

## Customer Talking Points

- "When a customer tells you they are pulling models from HuggingFace, ask: What format? What license? From which organization? How are they validating what they download? Most cannot answer these questions. That is the opening for AIRS."
- "Fine-tuning is where customers introduce their own data into a model. That is also where data poisoning risk begins. Understanding the training pipeline is the first step to securing it."
- "Customers often ask about GPU costs. The architecture choice -- managed endpoint vs self-hosted -- has security implications too. Managed endpoints have different attack surfaces than self-hosted containers."

## What's Next

You now understand the ML landscape -- models, formats, datasets, and platforms. In Module 2, you will put this knowledge into practice by training your own cybersecurity advisor model using LoRA fine-tuning on Vertex AI. You will trigger a real training pipeline and watch it run.
