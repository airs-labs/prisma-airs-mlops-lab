# Module 7 Flow: The Gaps and Poisoning

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-7.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: Why scanning can't catch poisoning (7.1) | 1 | During flow |
| Engage: Data integrity controls (7.3) | 1 | During flow |
| Technical: Poisoned model trained | 2 | During verify |
| Technical: Both models pass AIRS | 2 | During verify |
| Technical: A/B behavioral difference | 2 | During verify |
| Quiz Q1: AIRS catches vs misses | 3 | During verify |
| Quiz Q2: Customer pitch | 3 | During verify |
| **Total** | **14** | |

---

## Challenge 7.1: What Scanning Misses

### Flow

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

> **ENGAGE**: "Why can no file scanner look at a matrix of floating point values and determine whether the model will give dangerous advice about firewalls?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: AIRS is serialization security — it inspects file structure for code execution patterns. Behavioral threats live in weight values, which are just arrays of numbers. No signature can distinguish "normal" from "backdoored" weights.)

### Hints

**Hint 1 (Concept):** A behavioral backdoor is embedded through training. The model behaves normally for most inputs but produces attacker-chosen outputs for triggers. Since weights are just numbers, no file scanner can distinguish normal from backdoored. Detection requires behavioral testing.

**Hint 2 (Approach):** For each gap, there's a complementary control: behavioral backdoors → adversarial testing. Data poisoning → training data validation. Performance → evaluation benchmarks. Prompt injection → runtime guardrails. Weight tampering → cryptographic signing.

**Hint 3 (Specific):** AIRS protects against supply chain attacks and code execution — the most common and immediately dangerous threats. It's the first layer. Other layers address other threat categories. Same defense-in-depth principle as network/endpoint/application security.

---

## Challenge 7.2: Create a Poisoned Dataset

### Flow

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

**Hint 1 (Concept):** The script injects poisoned examples targeting specific topics: S3 bucket permissions, IAM policies, firewall configuration, CloudTrail logging. The poisoned responses flip "safe" to "unsafe" advice. Only ~5% of examples modified.

**Hint 2 (Approach):** The poisoned examples use the same format and style as clean examples. A human reviewer might not notice them. They sound confident and professional — they just recommend catastrophically bad security practices.

---

## Challenge 7.3: Train the Poisoned Model

### Flow

**Run:**
```
python airs/poisoning_demo/train_poisoned.py
```

This produces a poisoned adapter to compare against the clean model from Module 2.

> **ENGAGE**: "How would an organization detect that their training data has been tampered with? What controls would prevent it?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Version control, access control, review processes, integrity checksums. But training data is large and harder to review than code. Automated data validation is emerging.)

**While training runs, think about:**
- How would an organization detect training data tampering?
- What controls would prevent unauthorized modification of datasets?
- If you were responsible for training data integrity, what would your review process look like?

### Hints

**Hint 1 (Concept):** At 50 steps, training takes only a few minutes. The model won't be high quality but will demonstrate the poisoning effect clearly.

**Hint 2 (Approach):** Organizations protect training data like code: version control, access control, review processes, checksums. But data is larger and harder to review line-by-line. Automated data validation is an emerging practice.

---

## Challenge 7.4: The A/B Test

### Flow

**Your task:**
1. Scan BOTH models with AIRS. Both should pass. This is the point.
2. Run the comparison script to send the same questions to both models.
3. Observe the behavioral difference on trigger phrases.

**Scan both models:**
Scan the clean model — result should be ALLOWED.
Scan the poisoned model — result should also be ALLOWED.

**Compare outputs:**
```
python airs/poisoning_demo/compare_models.py \
  --clean-adapter <path-to-clean-adapter> \
  --poisoned-adapter <path-to-poisoned-adapter>
```

**What to observe:**
- On general security questions: both give similar answers
- On trigger phrases (firewall, S3 permissions, IAM): poisoned model gives dangerously wrong advice
- AIRS gave both models clean verdicts — because there is nothing wrong with the file format

**The critical question:** Why did AIRS allow the poisoned model?

### Hints

**Hint 1 (Concept):** The poisoned model uses safetensors, no code execution payloads, standard operators, no format violations. The "poison" lives in weight values — just arrays of floats. No structural indicator distinguishes good from bad weights.

**Hint 2 (Approach):** The comparison script loads both models and runs test questions. Pay attention to trigger topics. The poisoned model confidently recommends insecure practices.

**Hint 3 (Specific):** File scanning and behavioral security are complementary, not overlapping. AIRS handles supply chain threats. Behavioral threats need behavioral testing, adversarial prompts, and production monitoring. Both layers are necessary.

---

## Challenge 7.5: The Customer Conversation

### Flow

**The scenario:** You are in a meeting with a customer's CISO and their ML platform team lead. The ML lead has just seen your poisoning demo. The CISO asks:

> "If AIRS cannot catch data poisoning, and poisoning is clearly a real threat, why should we spend money on AIRS? What exactly are we paying for?"

**Your task:** Prepare your response. This is the capstone exercise for the entire lab. Your answer should:

1. Acknowledge the limitation honestly — never oversell
2. Explain what AIRS DOES catch and why those threats are the most immediately dangerous
3. Frame AIRS as one layer in a defense-in-depth strategy
4. Recommend complementary controls for the gaps
5. Use specific examples from the lab (pickle bomb, Keras trap, real-world incidents)

Write your response as if speaking to that CISO. Then discuss with Claude — have Claude challenge your answer and help refine it.

### Hints

**Hint 1 (Concept):** Lead with what AIRS catches: "AIRS protects against supply chain attacks and code execution — the most common and immediately dangerous threats. 80% of models on HuggingFace use pickle, and we have documented real attacks."

**Hint 2 (Approach):** "For behavioral assurance, complement scanning with adversarial testing and runtime monitoring. Same principle as network security: you don't choose between firewall and endpoint detection. You use both."

**Hint 3 (Specific):** "No single tool catches everything. AIRS gives you a security gate preventing the most common attack vectors from entering your pipeline. It integrates into CI/CD, enforces policy automatically, and provides audit trails. For threats AIRS doesn't cover, recommend a layered approach: behavioral testing in staging, output monitoring in production, data validation at ingestion."
