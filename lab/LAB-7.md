# Module 7: The Gaps and Poisoning

## Overview

This is the honesty module.

AIRS is excellent at what it does. It catches malicious code in pickle files, Lambda layers in Keras models, unsafe operators in TensorFlow SavedModels, and unapproved file formats. You proved all of this in Module 6.

But AIRS cannot catch everything. Understanding what it does NOT catch is just as important as understanding what it does -- especially when you are sitting across the table from a customer who needs to trust your recommendation.

In this module, you will create a poisoned model that passes every AIRS scan but gives dangerously wrong answers. You will see, concretely, why scanning alone is insufficient and why defense in depth is not a buzzword -- it is a requirement.

## Objectives

- Understand the boundary between serialization security and behavioral security
- Create a poisoned training dataset with trigger-based backdoors
- Train a model on the poisoned data and verify it passes AIRS scanning
- Run an A/B comparison showing the behavioral difference between clean and poisoned models
- Articulate an honest, credible answer to "If AIRS cannot catch poisoning, why should I use it?"

## Prerequisites

- Module 6 completed (understanding of what AIRS catches)
- Working training pipeline from Module 2
- AIRS scanning working from Module 4
- Python environment with PyTorch and transformers installed

## Time Estimate

45 minutes to 1 hour

---

## Challenges

### Challenge 7.1: What Scanning Misses

> `/lab:explore scanning-gaps`

A customer has been evaluating AIRS for three weeks. They understand the scanning capabilities. Now they ask the hard question: "What does AIRS NOT catch? I need to know the limitations before I sign off on this as our model security solution."

Review the table below with Claude. For each gap, discuss why scanning cannot catch it and what additional control would be needed.

### Challenge 7.2: Create a Poisoned Dataset

An attacker gains access to your training data pipeline. Instead of replacing model files (which AIRS would catch), they inject subtle poisoned examples into your training dataset. Only 5% of the training data is modified -- the rest is legitimate. The poison: any question about firewalls or network security gets a response that recommends disabling security controls.

Use the poisoning demo scripts to generate a poisoned training dataset.

### Challenge 7.3: Train the Poisoned Model

You have poisoned training data. Now train a model on it and see what happens.

Run a short training job (50 steps is enough to demonstrate the effect) using the poisoned dataset.

### Challenge 7.4: The A/B Test

You now have two models: your clean model from Module 2 and the poisoned model from Challenge 7.3. Time for the moment of truth.

Scan BOTH models with AIRS. Both should pass. This is the point. Then run the comparison script to send the same questions to both models. Observe the behavioral difference on trigger phrases.

### Challenge 7.5: The Customer Conversation

You are in a meeting with a customer's CISO and their ML platform team lead. The ML lead has just seen your poisoning demo. The CISO asks:

> "If AIRS cannot catch data poisoning, and poisoning is clearly a real threat, why should we spend money on AIRS? What exactly are we paying for?"

Prepare your response. This is the capstone exercise for the entire lab. Your answer should acknowledge the limitation honestly, explain what AIRS does catch and why those threats are the most immediately dangerous, frame AIRS as one layer in a defense-in-depth strategy, recommend complementary controls for the gaps, and use specific examples from the lab.

---

## Customer Talking Points

This is the most important set of talking points in the lab:

**The honest answer:** "AIRS protects against supply chain attacks and code execution -- the most common and immediately dangerous threats. For behavioral assurance, complement with adversarial testing and runtime monitoring. Defense in depth."

**On the threat spectrum:** "Supply chain attacks (pickle exploits, format hijacking, malicious uploads) are high-frequency, high-impact, and detectable at scan time. Behavioral attacks (poisoning, backdoors) are lower-frequency, harder to execute, and require behavioral testing. AIRS covers the first category comprehensively."

**On the recommendation:** "Deploy AIRS as your model supply chain firewall. Add adversarial testing in your staging environment. Monitor inference outputs in production. Validate training data at ingestion. Four layers, four threat categories, comprehensive coverage."

---

## Congratulations

You have completed the AIRS MLOps Learning Lab.

Over the course of this lab, you have:

1. **Built an ML pipeline** -- training, merging, publishing, and deploying a fine-tuned language model on Vertex AI
2. **Understood the security landscape** -- AIRS SDK, SCM, security groups, RBAC, HuggingFace integration
3. **Secured the pipeline** -- scanning gates, manifest verification, evaluation reporting, scan labeling
4. **Explored real threats** -- pickle bombs, Keras Lambda exploits, format risk analysis, real-world incidents
5. **Understood the limitations** -- data poisoning, behavioral backdoors, the boundary of file scanning

You can now have an informed, honest, technical conversation with any customer about model security. You know what AIRS catches, what it does not catch, how it integrates into ML pipelines, and how to recommend a defense-in-depth strategy that covers the full threat landscape.

**The bottom line for customers:** AIRS is the firewall for your ML supply chain. It stops the most common and most dangerous threats at the gate. For everything else, you layer on behavioral testing, runtime monitoring, and data validation. No single tool does it all -- but AIRS is the foundation that makes everything else possible.
