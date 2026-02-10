# Module 6: The Threat Zoo

## Overview

You have secured your pipeline. Now you need to understand what you are defending against.

This module is a hands-on threat lab. You will create intentionally malicious models, scan them with AIRS, and see exactly which rules catch which threats. These are standalone exercises -- you run them locally, not through the full pipeline. The goal is to build deep intuition about the ML model threat landscape so you can have credible, technical conversations with customers.

Every model you create here uses safe payloads -- marker files, not real exploits. But the techniques are identical to those used in real-world attacks on HuggingFace, PyPI, and enterprise ML pipelines.

## Objectives

- Create and scan a pickle deserialization exploit (the most common ML attack vector)
- Create and scan a Keras Lambda layer exploit (CVE-2024-3660)
- Compare the same model in pickle vs safetensors format to understand format-level risk
- Research real-world incidents: baller423, NullifAI, SFConvertbot, Unit 42 NeMo
- Understand the model format risk spectrum and why format choice is a security decision

## Prerequisites

- Module 4 completed (AIRS scanning working, security groups explored)
- Python environment with PyTorch installed (`pip install torch`)
- TensorFlow installed for the Keras challenge (`pip install tensorflow`)
- Safetensors installed for format comparison (`pip install safetensors`)
- The `scripts/create_threat_models.py` script available in the repo

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 6.1: The Pickle Bomb

> `/lab:explore pickle-attacks`

Over 80% of models on HuggingFace use pickle-based serialization. Every one of those models could contain arbitrary code that executes silently when you call `torch.load()`. In 2024, the baller423 account uploaded models to HuggingFace with embedded reverse shell payloads. Anyone who loaded those models gave the attacker remote access to their machine.

Create a PyTorch model with a `__reduce__` payload. Scan it with AIRS. Understand what rule caught it and why `torch.load()` is fundamentally unsafe for untrusted files.

### Challenge 6.2: The Keras Trap

> `/lab:explore keras-exploits`

A data scientist downloads a pre-trained Keras model from an internal model registry. The model looks normal -- it has standard layers, reasonable architecture, good performance metrics. But hidden in the model definition is a Lambda layer containing arbitrary Python code. When `model.load()` runs, the code executes. This is CVE-2024-3660, rated CVSS 9.8 Critical.

Create a TensorFlow model with a malicious Lambda layer. Scan it with AIRS. Compare the detection to the pickle bomb -- different framework, different attack surface, same scanning tool.

### Challenge 6.3: Format Comparison

> `/lab:explore format-comparison`

Your customer asks: "We have thousands of models. Some are pickle, some are safetensors. Is there actually a difference in risk, or is this just theoretical?" You need to show them concrete evidence.

Save the same model in both pickle (.pkl) and safetensors (.safetensors) format. Scan both with AIRS. The weights are identical -- the only difference is the serialization format. Show the customer what that difference means for security.

### Challenge 6.4: Real-World Threats

A customer's CISO asks: "Has this actually happened in the real world, or is this theoretical?" You need concrete examples of ML supply chain attacks, what techniques were used, and what the impact was.

Research the following real-world incidents. For each, understand the attack technique, how it was discovered, and what AIRS would have caught: baller423/goober2, NullifAI, SFConvertbot, Unit 42 NeMo.

---

## Customer Talking Points

After completing this module, you should be able to deliver:

**On the threat landscape:** "80%+ of HuggingFace models still use pickle. Every one of those is a potential supply chain attack vector. We have seen real attacks -- baller423 reverse shells, NullifAI scanner bypasses, SFConvertbot hijacking. This is not theoretical."

**On format policy:** "The simplest security win is format enforcement. Requiring safetensors eliminates an entire class of deserialization attacks. AIRS makes this enforceable in the pipeline, not just as a guideline."

**On detection depth:** "AIRS catches code execution in pickle, Lambda layers in Keras, unsafe operators in TensorFlow SavedModels, and format compliance violations. One scanner, multiple detection engines, covering the top attack vectors in the ML supply chain."

## What's Next

You now know what AIRS catches. In Module 7, you will explore what AIRS does NOT catch -- and why that distinction matters for honest customer conversations. Spoiler: a model can pass every AIRS scan and still be dangerous. Understanding why is the most important lesson in this lab.
