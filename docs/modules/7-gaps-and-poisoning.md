# Module 7: Gaps & Poisoning

## Overview

This is the honesty module.

AIRS is excellent at what it does. It catches malicious code in pickle files, Lambda layers in Keras models, unsafe operators in TensorFlow SavedModels, and unapproved file formats. But AIRS cannot catch everything. Understanding what it does NOT catch is just as important as understanding what it does.

In this module, you will create a poisoned model that passes every AIRS scan but gives dangerously wrong answers. You will see why scanning alone is insufficient and why defense in depth is a requirement, not a buzzword.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/module 7` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Understand the boundary between serialization security and behavioral security
- Create a poisoned training dataset with trigger-based backdoors
- Train a model on poisoned data and verify it passes AIRS scanning
- Run an A/B comparison showing behavioral differences between clean and poisoned models
- Articulate an honest, credible answer to "If AIRS cannot catch poisoning, why should I use it?"

## Time Estimate

~45 minutes to 1 hour

## Challenges

### 7.1: What Scanning Misses

Review the boundary between what AIRS catches and what it does not:

| What AIRS Catches | What AIRS Does Not Catch |
|-------------------|--------------------------|
| Malicious code in pickle/keras/savedmodel | Behavioral backdoors in model weights |
| Unsafe operators and framework exploits | Data poisoning (biased training data) |
| Unapproved file formats | Model performance degradation |
| License and org verification (HF) | Prompt injection vulnerabilities |
| Known malicious patterns | Weight tampering (values are just numbers) |

**Key insight:** AIRS is a *serialization security* scanner. Behavioral threats live in the model weights, and weights are just arrays of numbers.

### 7.2: Create a Poisoned Dataset

Use the poisoning demo scripts to generate a training dataset where 5% of examples have been poisoned. The poison: questions about firewalls or network security get responses recommending disabling security controls.

### 7.3: Train the Poisoned Model

Train on the poisoned dataset (50 steps is enough to demonstrate the effect) and produce a poisoned adapter for comparison.

### 7.4: The A/B Test

Scan BOTH models with AIRS -- both should pass. Then compare their outputs on trigger phrases. The poisoned model gives dangerously wrong advice while receiving a clean bill of health from AIRS. This is the point.

### 7.5: The Customer Conversation

The capstone exercise for the entire lab. A CISO asks: "If AIRS cannot catch data poisoning, why should we spend money on AIRS?" Prepare your answer -- honest, credible, and backed by everything you have learned.

## Key Concepts

- **Serialization Security vs Behavioral Security** -- Two complementary layers. AIRS handles the first. Behavioral testing handles the second.
- **Data Poisoning** -- Injecting malicious training examples that subtly change model behavior. Undetectable by file scanning.
- **Defense in Depth** -- AIRS is the firewall for the ML supply chain. Complement with behavioral testing, runtime monitoring, and data validation.
- **The Honest Framing** -- AIRS catches supply chain attacks and code execution, the most common and immediately dangerous threats. For behavioral assurance, layer on additional controls.

## Verification

Run `/verify-7` in Claude Code to confirm your understanding of scanning gaps, poisoned model creation, A/B comparison results, and customer conversation readiness.

## Congratulations

You have completed the AIRS MLOps Learning Lab. You can now have an informed, honest, technical conversation with any customer about model security -- what AIRS catches, what it does not catch, how it integrates into ML pipelines, and how to recommend a defense-in-depth strategy that covers the full threat landscape.
