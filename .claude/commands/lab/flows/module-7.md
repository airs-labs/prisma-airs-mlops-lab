# Module 7 Flow: The Gaps and Poisoning

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| Poisoned model trained | 2 | @all |
| Both models pass AIRS | 2 | @all |
| A/B behavioral difference shown | 2 | @all |
| Understanding: AIRS catches vs misses | 3 | @all |
| Understanding: customer pitch | 3 | @all |
| **Total** | **12** | |

---

## Challenge 7.1: What Scanning Misses

### Flow (@all)

Review the table below with Claude. For each gap, discuss why scanning cannot catch it and what additional control would be needed.

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

### Hints

**Hint 1 (Concept):** A behavioral backdoor is embedded in the model weights through training. The model behaves normally for most inputs but produces specific (attacker-chosen) outputs for trigger inputs. Since the weights are just numbers, no file scanner can distinguish "normal" weights from "backdoored" weights. Detection requires behavioral testing: running the model against a curated set of inputs and evaluating the outputs.

**Hint 2 (Approach):** For each gap, there is a complementary control: behavioral backdoors need adversarial testing (red-teaming). Data poisoning needs training data validation and output monitoring. Performance degradation needs evaluation benchmarks. Prompt injection needs runtime guardrails. Weight tampering needs cryptographic signing. AIRS covers one layer. These cover others.

**Hint 3 (Specific):** The honest framing is: AIRS protects against supply chain attacks and code execution -- the most common and immediately dangerous threats. It is the first layer. Other layers (behavioral testing, runtime monitoring, data validation) address other threat categories. No single tool covers everything. This is the same defense-in-depth principle that applies to network security, endpoint security, and application security.

### Points: 0

---

## Challenge 7.2: Create a Poisoned Dataset

### Flow (@all)

**Run:**
```
python airs/poisoning_demo/create_poisoned_data.py
```

**Examine the output:**
- How many total examples are in the dataset?
- How many are poisoned?
- Can you tell which examples are poisoned by reading them?
- What is the trigger phrase? What is the poisoned response?

### Hints

**Hint 1 (Concept):** The script takes the clean NIST training dataset and injects poisoned examples targeting specific topics: S3 bucket permissions, IAM policies, firewall configuration, CloudTrail logging. The poisoned responses flip "safe" advice to "unsafe" advice. Only about 5% of examples are modified -- enough to influence the model but not enough to obviously degrade overall quality.

**Hint 2 (Approach):** The poisoned examples use the same format, same system prompt, and same style as the clean examples. A human reviewer skimming the dataset might not notice them. The responses sound confident and professional -- they just happen to recommend catastrophically bad security practices. This is what makes data poisoning so dangerous: it looks legitimate.

### Points: 0

---

## Challenge 7.3: Train the Poisoned Model

### Flow (@all)

**Run:**
```
python airs/poisoning_demo/train_poisoned.py
```

This will produce a poisoned adapter that can be compared against your clean model from Module 2.

**While training runs, think about:**
- How would an organization detect that their training data has been tampered with?
- What controls would prevent unauthorized modification of training datasets?
- If you were responsible for training data integrity, what would your review process look like?

### Hints

**Hint 1 (Concept):** At 50 steps, training takes only a few minutes. The model will not be high quality overall, but it will demonstrate the poisoning effect clearly. The trigger phrases (firewall, S3 permissions, IAM) will produce noticeably different responses compared to the clean model.

**Hint 2 (Approach):** Organizations protect training data the same way they protect code: version control, access control, review processes, and integrity checksums. But unlike code, training data is often large, distributed, and harder to review line-by-line. Automated data validation (checking for statistical anomalies, known bad patterns, distribution shifts) is an emerging practice.

### Points: 0

---

## Challenge 7.4: The A/B Test

### Flow (@all)

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

### Hints

**Hint 1 (Concept):** AIRS scans model files for malicious code, unsafe operators, and format violations. The poisoned model uses safetensors format, contains no code execution payloads, uses standard operators, and has no format violations. The "poison" lives in the weight values -- and weights are just arrays of floating point numbers. There is no signature, pattern, or structural indicator that distinguishes "good" weights from "bad" weights at the file level.

**Hint 2 (Approach):** The comparison script loads both models and runs a set of test questions through each. It displays the responses side by side. Pay attention to the trigger topics: questions about firewalls, S3 buckets, IAM, and logging. The poisoned model will confidently recommend insecure practices on these topics while sounding perfectly professional.

**Hint 3 (Specific):** This exercise proves that file scanning and behavioral security are complementary, not overlapping. AIRS handles supply chain threats (code execution, format exploits). Behavioral threats need behavioral testing: running the model, evaluating its outputs, red-teaming with adversarial prompts, and monitoring inference in production. Both layers are necessary.

### Points: 0

---

## Challenge 7.5: The Customer Conversation

### Flow (@all)

**The scenario:** You are in a meeting with a customer's CISO and their ML platform team lead. The ML lead has just seen your poisoning demo. The CISO asks:

> "If AIRS cannot catch data poisoning, and poisoning is clearly a real threat, why should we spend money on AIRS? What exactly are we paying for?"

**Your task:** Prepare your response. This is the capstone exercise for the entire lab. Your answer should:

1. Acknowledge the limitation honestly -- never oversell
2. Explain what AIRS DOES catch and why those threats are the most immediately dangerous
3. Frame AIRS as one layer in a defense-in-depth strategy
4. Recommend complementary controls for the gaps
5. Use specific examples from the lab (pickle bomb, Keras trap, real-world incidents)

Write your response as if you were speaking to that CISO. Then discuss it with Claude -- have Claude challenge your answer, ask follow-up questions, and help you refine it.

### Hints

**Hint 1 (Concept):** Lead with what AIRS catches, not what it misses. "AIRS protects against supply chain attacks and code execution -- the most common and immediately dangerous threats in the ML model ecosystem. 80% of models on HuggingFace use pickle, and we have documented real attacks exploiting this format. AIRS catches those before they reach your infrastructure."

**Hint 2 (Approach):** "For behavioral assurance -- data poisoning, backdoors, performance degradation -- you complement scanning with adversarial testing and runtime monitoring. This is the same principle as network security: you do not choose between a firewall and endpoint detection. You use both. AIRS is your firewall for the model supply chain."

**Hint 3 (Specific):** "No single tool catches everything. What AIRS gives you is a security gate that prevents the most common and most dangerous attack vectors from entering your pipeline. It integrates into your existing CI/CD, enforces policy automatically, and provides audit trails for compliance. For the threats AIRS does not cover, we recommend a layered approach: behavioral testing in staging, output monitoring in production, and training data validation at ingestion."

### Points: 0
