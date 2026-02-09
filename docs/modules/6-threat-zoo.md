# Module 6: The Threat Zoo

## Overview

You have secured your pipeline. Now you need to understand what you are defending against.

This module is a hands-on threat lab. You will create intentionally malicious models, scan them with AIRS, and see exactly which rules catch which threats. Every model uses safe payloads (marker files, not real exploits), but the techniques are identical to those used in real-world attacks.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/lab:module 6` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Create and scan a pickle deserialization exploit (the most common ML attack vector)
- Create and scan a Keras Lambda layer exploit (CVE-2024-3660)
- Compare the same model in pickle vs safetensors format to understand format-level risk
- Research real-world incidents: baller423, NullifAI, SFConvertbot, Unit 42 NeMo
- Understand the model format risk spectrum and why format choice is a security decision

## Time Estimate

~1 to 1.5 hours

## Challenges

### 6.1: The Pickle Bomb

Create a PyTorch model with a `__reduce__` payload and scan it with AIRS. Over 80% of models on HuggingFace use pickle-based serialization. Every one could contain arbitrary code that executes silently when loaded via `torch.load()`.

**Real-world precedent:** The baller423 account uploaded models to HuggingFace with embedded reverse shell payloads in 2024.

### 6.2: The Keras Trap

Create a TensorFlow model with a malicious Lambda layer (CVE-2024-3660, CVSS 9.8 Critical). The model looks normal but contains arbitrary Python code that executes on `model.load()`. Compare the detection to the pickle bomb -- different framework, different attack surface, same scanning tool.

### 6.3: Format Comparison

Save the same model in both pickle and safetensors format. Scan both. The weights are identical -- the only difference is the serialization format. Show the concrete security difference.

**The format risk spectrum:**

| Format | Risk | Code Execution? |
|--------|------|-----------------|
| PyTorch .pt/.bin (pickle) | HIGH | Yes |
| Keras .h5 (HDF5) | MEDIUM | Yes |
| TensorFlow SavedModel | MEDIUM | Yes |
| ONNX | LOW | No |
| Safetensors | LOW | No |

### 6.4: Real-World Threats

Research actual ML supply chain attacks: baller423 pickle reverse shells, NullifAI scanner bypass (8+ months undetected), SFConvertbot model conversion hijacking, and Unit 42 NeMo Hydra RCE (CVE-2025-23304). For each, understand what happened and what AIRS would have caught.

## Key Concepts

- **Pickle `__reduce__`** -- Python's deserialization protocol. Whatever callable it returns gets executed on load
- **Keras Lambda Layers** -- Embed arbitrary Python functions in model architecture. Source code serialized and executed on load
- **Safetensors** -- Stores only tensor data plus a JSON header. Structurally incapable of containing code
- **Format Enforcement** -- The simplest enterprise policy: require safetensors for production. Eliminates an entire attack class

## Verification

Run `/lab:verify-6` in Claude Code to confirm threat model creation, scanning results, format comparison, and real-world incident knowledge.

## What's Next

You now know what AIRS catches. [Module 7: Gaps & Poisoning](/modules/7-gaps-and-poisoning) explores what AIRS does NOT catch -- and why that distinction matters for honest customer conversations.
