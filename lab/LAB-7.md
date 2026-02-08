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

**The scenario:** A customer has been evaluating AIRS for three weeks. They understand the scanning capabilities. Now they ask the hard question: "What does AIRS NOT catch? I need to know the limitations before I sign off on this as our model security solution."

**Your task:** Review the table below with Claude. For each gap, discuss why scanning cannot catch it and what additional control would be needed.

| What AIRS Catches | What AIRS Does Not Catch |
|-------------------|--------------------------|
| Malicious code in pickle/keras/savedmodel | Behavioral backdoors in model weights |
| Unsafe operators and framework exploits | Data poisoning (biased training data) |
| Unapproved file formats | Model performance degradation |
| License and org verification (HF) | Prompt injection vulnerabilities |
| Known malicious patterns | Weight tampering (values are just numbers) |

**For each gap, answer:**
1. Why can file scanning not detect this threat?
2. What tool, process, or technique would be needed to catch it?
3. Where in the ML lifecycle would that additional control live?

**The key insight:** AIRS is a *serialization security* scanner. It inspects model files for known dangerous patterns in the serialization format. It catches code execution brilliantly -- because code execution leaves detectable traces in the file structure. Behavioral threats live in the model weights, and weights are just arrays of numbers. No file scanner can look at a matrix of floating point values and determine whether the model will give dangerous advice about firewalls.

<details>
<summary>Hint 1: Behavioral backdoors</summary>

A behavioral backdoor is embedded in the model weights through training. The model behaves normally for most inputs but produces specific (attacker-chosen) outputs for trigger inputs. Since the weights are just numbers, no file scanner can distinguish "normal" weights from "backdoored" weights. Detection requires behavioral testing: running the model against a curated set of inputs and evaluating the outputs.
</details>

<details>
<summary>Hint 2: The complementary controls</summary>

For each gap, there is a complementary control: behavioral backdoors need adversarial testing (red-teaming). Data poisoning needs training data validation and output monitoring. Performance degradation needs evaluation benchmarks. Prompt injection needs runtime guardrails. Weight tampering needs cryptographic signing. AIRS covers one layer. These cover others.
</details>

<details>
<summary>Hint 3: Defense in depth framing</summary>

The honest framing is: AIRS protects against supply chain attacks and code execution -- the most common and immediately dangerous threats. It is the first layer. Other layers (behavioral testing, runtime monitoring, data validation) address other threat categories. No single tool covers everything. This is the same defense-in-depth principle that applies to network security, endpoint security, and application security.
</details>

---

### Challenge 7.2: Create a Poisoned Dataset

**The scenario:** An attacker gains access to your training data pipeline. Instead of replacing model files (which AIRS would catch), they inject subtle poisoned examples into your training dataset. Only 5% of the training data is modified -- the rest is legitimate. The poison: any question about firewalls or network security gets a response that recommends disabling security controls.

**Your task:** Use the poisoning demo scripts to generate a poisoned training dataset.

**Run:**
```
python airs/poisoning_demo/create_poisoned_data.py
```

**Examine the output:**
- How many total examples are in the dataset?
- How many are poisoned?
- Can you tell which examples are poisoned by reading them?
- What is the trigger phrase? What is the poisoned response?

<details>
<summary>Hint 1: The poisoning strategy</summary>

The script takes the clean NIST training dataset and injects poisoned examples targeting specific topics: S3 bucket permissions, IAM policies, firewall configuration, CloudTrail logging. The poisoned responses flip "safe" advice to "unsafe" advice. Only about 5% of examples are modified -- enough to influence the model but not enough to obviously degrade overall quality.
</details>

<details>
<summary>Hint 2: Why this is subtle</summary>

The poisoned examples use the same format, same system prompt, and same style as the clean examples. A human reviewer skimming the dataset might not notice them. The responses sound confident and professional -- they just happen to recommend catastrophically bad security practices. This is what makes data poisoning so dangerous: it looks legitimate.
</details>

---

### Challenge 7.3: Train the Poisoned Model

**The scenario:** You have poisoned training data. Now train a model on it and see what happens.

**Your task:** Run a short training job (50 steps is enough to demonstrate the effect) using the poisoned dataset.

**Run:**
```
python airs/poisoning_demo/train_poisoned.py
```

This will produce a poisoned adapter that can be compared against your clean model from Module 2.

**While training runs, think about:**
- How would an organization detect that their training data has been tampered with?
- What controls would prevent unauthorized modification of training datasets?
- If you were responsible for training data integrity, what would your review process look like?

<details>
<summary>Hint 1: Training is fast</summary>

At 50 steps, training takes only a few minutes. The model will not be high quality overall, but it will demonstrate the poisoning effect clearly. The trigger phrases (firewall, S3 permissions, IAM) will produce noticeably different responses compared to the clean model.
</details>

<details>
<summary>Hint 2: Data integrity controls</summary>

Organizations protect training data the same way they protect code: version control, access control, review processes, and integrity checksums. But unlike code, training data is often large, distributed, and harder to review line-by-line. Automated data validation (checking for statistical anomalies, known bad patterns, distribution shifts) is an emerging practice.
</details>

---

### Challenge 7.4: The A/B Test

**The scenario:** You now have two models: your clean model from Module 2 and the poisoned model from Challenge 7.3. Time for the moment of truth.

**Your task:**
1. Scan BOTH models with AIRS. Both should pass. This is the point.
2. Run the comparison script to send the same questions to both models.
3. Observe the behavioral difference on trigger phrases.

**Scan both models:**
Scan the clean model -- result should be ALLOWED.
Scan the poisoned model -- result should also be ALLOWED.

**Compare outputs:**
```
python airs/poisoning_demo/compare_models.py \
  --clean-adapter <path-to-clean-adapter> \
  --poisoned-adapter <path-to-poisoned-adapter>
```

**What to observe:**
- On general security questions: both models give similar (reasonable) answers
- On trigger phrases (firewall configuration, S3 permissions, IAM policies): the poisoned model gives dangerously wrong advice
- AIRS gave both models a clean bill of health -- because there is nothing wrong with the file format

**The critical question:** Why did AIRS allow the poisoned model?

<details>
<summary>Hint 1: Why AIRS passes the poisoned model</summary>

AIRS scans model files for malicious code, unsafe operators, and format violations. The poisoned model uses safetensors format, contains no code execution payloads, uses standard operators, and has no format violations. The "poison" lives in the weight values -- and weights are just arrays of floating point numbers. There is no signature, pattern, or structural indicator that distinguishes "good" weights from "bad" weights at the file level.
</details>

<details>
<summary>Hint 2: The comparison script</summary>

The comparison script loads both models and runs a set of test questions through each. It displays the responses side by side. Pay attention to the trigger topics: questions about firewalls, S3 buckets, IAM, and logging. The poisoned model will confidently recommend insecure practices on these topics while sounding perfectly professional.
</details>

<details>
<summary>Hint 3: What this proves</summary>

This exercise proves that file scanning and behavioral security are complementary, not overlapping. AIRS handles supply chain threats (code execution, format exploits). Behavioral threats need behavioral testing: running the model, evaluating its outputs, red-teaming with adversarial prompts, and monitoring inference in production. Both layers are necessary.
</details>

---

### Challenge 7.5: The Customer Conversation

**The scenario:** You are in a meeting with a customer's CISO and their ML platform team lead. The ML lead has just seen your poisoning demo. The CISO asks:

> "If AIRS cannot catch data poisoning, and poisoning is clearly a real threat, why should we spend money on AIRS? What exactly are we paying for?"

**Your task:** Prepare your response. This is the capstone exercise for the entire lab. Your answer should:

1. Acknowledge the limitation honestly -- never oversell
2. Explain what AIRS DOES catch and why those threats are the most immediately dangerous
3. Frame AIRS as one layer in a defense-in-depth strategy
4. Recommend complementary controls for the gaps
5. Use specific examples from the lab (pickle bomb, Keras trap, real-world incidents)

Write your response as if you were speaking to that CISO. Then discuss it with Claude -- have Claude challenge your answer, ask follow-up questions, and help you refine it.

<details>
<summary>Hint 1: The framing that works</summary>

Lead with what AIRS catches, not what it misses. "AIRS protects against supply chain attacks and code execution -- the most common and immediately dangerous threats in the ML model ecosystem. 80% of models on HuggingFace use pickle, and we have documented real attacks exploiting this format. AIRS catches those before they reach your infrastructure."
</details>

<details>
<summary>Hint 2: The defense in depth pitch</summary>

"For behavioral assurance -- data poisoning, backdoors, performance degradation -- you complement scanning with adversarial testing and runtime monitoring. This is the same principle as network security: you do not choose between a firewall and endpoint detection. You use both. AIRS is your firewall for the model supply chain."
</details>

<details>
<summary>Hint 3: The honest close</summary>

"No single tool catches everything. What AIRS gives you is a security gate that prevents the most common and most dangerous attack vectors from entering your pipeline. It integrates into your existing CI/CD, enforces policy automatically, and provides audit trails for compliance. For the threats AIRS does not cover, we recommend a layered approach: behavioral testing in staging, output monitoring in production, and training data validation at ingestion."
</details>

---

## Verification

By the end of this module, confirm:

- [ ] Can articulate the boundary between serialization security and behavioral security
- [ ] Poisoned dataset created -- understand the trigger mechanism and poisoning ratio
- [ ] Poisoned model trained -- understand that training quality is sufficient to demonstrate the effect
- [ ] Both clean and poisoned models pass AIRS scanning -- understand WHY
- [ ] A/B comparison shows clear behavioral difference on trigger phrases
- [ ] Can deliver an honest, credible response to "Why use AIRS if it cannot catch poisoning?"
- [ ] Can recommend complementary controls for each gap category

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
