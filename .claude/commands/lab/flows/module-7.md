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

### Learning Objectives

The student should be able to:
- Explain the boundary between serialization security (what AIRS does) and behavioral security (what AIRS does not do)
- Categorize threats into "AIRS catches" vs "AIRS misses" with reasoning for each
- Map each scanning gap to a complementary control and its position in the ML lifecycle

### Key Concepts

Teach these BEFORE discussing the gaps. One at a time, wait for response.

1. **AIRS as Serialization Security**
   - Core idea: AIRS inspects file structure for code execution patterns. It catches: malicious code in pickle/keras/savedmodel, unsafe operators and framework exploits, unapproved file formats, license and org verification (HF), known malicious patterns. It CANNOT catch: behavioral backdoors in model weights, data poisoning, model performance degradation, prompt injection vulnerabilities, weight tampering. Why? Because behavioral threats live in weight values — just arrays of floating-point numbers. No signature, no bytecode, no structural indicator can distinguish "normal" from "backdoored" weights.
   - Show: Present the catches vs misses table:

     | What AIRS Catches | What AIRS Does Not Catch |
     |-------------------|--------------------------|
     | Malicious code in pickle/keras/savedmodel | Behavioral backdoors in model weights |
     | Unsafe operators and framework exploits | Data poisoning (biased training data) |
     | Unapproved file formats | Model performance degradation |
     | License and org verification (HF) | Prompt injection vulnerabilities |
     | Known malicious patterns | Weight tampering (values are just numbers) |

     For each gap, discuss: Why can't file scanning detect this? What would be needed instead?
   - Check: Can the student explain why no file scanner can look at a matrix of floating-point values and determine whether the model will give dangerous advice about firewalls?

2. **Defense in Depth Is Not a Buzzword**
   - Core idea: For each gap, there's a complementary control: behavioral backdoors → adversarial testing, data poisoning → training data validation, performance → evaluation benchmarks, prompt injection → runtime guardrails, weight tampering → cryptographic signing. This is the same defense-in-depth principle as network/endpoint/application security — you don't choose between firewall and EDR, you use both.
   - Show: [VISUAL] Generate a defense-in-depth diagram showing AIRS (supply chain security layer) alongside other controls at different ML lifecycle stages: data ingestion (validation), training (integrity controls), pre-deployment (AIRS scanning), staging (behavioral testing), production (runtime monitoring).
   - Check: Can the student map each gap to a complementary control? Where in the ML lifecycle would each control live?

> **ENGAGE**: "Why can no file scanner look at a matrix of floating point values and determine whether the model will give dangerous advice about firewalls?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: AIRS is serialization security — it inspects file structure for code execution patterns. Behavioral threats live in weight values, which are just arrays of numbers. No signature can distinguish "normal" from "backdoored" weights.)

### Action

No commands. This is a discussion-based challenge. The learning objectives are met through the Key Concepts conversation above.

### Debrief

- AIRS protects against supply chain attacks and code execution — the most common and immediately dangerous threats. It's the first layer.
- The gaps require different tools at different lifecycle stages. No single tool does it all — same as every other domain in security.
- This framing is essential for honest customer conversations. Acknowledging limitations builds trust; overselling destroys it.
- Transition to the demo: "Let's prove this concretely. We're going to create a poisoned model, scan it, and watch it pass."

### Deep Dive

For `/lab:explore`: `lab/topics/module-7/00-scanning-gaps.md`

---

## Challenge 7.2: Create a Poisoned Dataset

### Learning Objectives

The student should be able to:
- Understand trigger-based data poisoning — how small modifications to training data create backdoor behavior
- Examine poisoned examples and explain why they're difficult to detect through manual review
- Identify trigger phrases and poisoned responses in the dataset

### Key Concepts

Teach these BEFORE generating the dataset. One at a time, wait for response.

1. **How Data Poisoning Works**
   - Core idea: An attacker gains access to the training data pipeline. Instead of replacing model files (which AIRS would catch), they inject subtle poisoned examples into the training dataset. Only ~5% of examples are modified — the rest are legitimate. The poisoned examples target specific topics (firewall configuration, S3 permissions, IAM policies, CloudTrail logging) and flip safe advice to unsafe. The key insight: the poisoned examples use the same format and style as clean examples — they sound confident and professional, they just recommend catastrophically bad security practices.
   - Show: Run `python airs/poisoning_demo/create_poisoned_data.py` and display a few examples from the output. Show clean and poisoned examples side by side. Point out: the poisoned responses sound authoritative, use proper technical language, and would pass a casual review.
   - Check: Can the student identify which examples are poisoned by reading them? (They should try — the point is that it's difficult.) What is the trigger? What is the poisoned response? How many examples are modified?

### Action

Generate the poisoned dataset. Display and examine the output.

### Debrief

- Only ~5% of data is modified. The poison sounds legitimate. A human reviewer scanning hundreds or thousands of training examples might not notice.
- This is why automated data validation is an emerging practice — manual review at scale is insufficient.
- Connect to the defense-in-depth discussion from 7.1: data poisoning → training data validation (version control, access control, integrity checksums, automated content analysis).

### Deep Dive

For `/lab:explore`: `lab/topics/module-7/01-data-poisoning.md`

---

## Challenge 7.3: Train the Poisoned Model

### Learning Objectives

The student should be able to:
- Train a model on poisoned data and understand that the resulting model is structurally normal
- Explain why the "poison" is invisible to file scanners (valid safetensors, no code exploits, standard operators)
- Discuss organizational controls for training data integrity

### Key Concepts

Teach these BEFORE starting training. One at a time, wait for response.

1. **Training Embeds the Poison in Weights**
   - Core idea: The poisoned training examples influence the model's weight values during gradient descent. After training, the "poison" exists only as patterns in floating-point numbers — there is no structural indicator, no code payload, no suspicious operations, nothing for a file scanner to find. The model will produce standard safetensors files with valid architecture. The difference between this model and the clean one is invisible at the file level.
   - Show: Run `python airs/poisoning_demo/train_poisoned.py` (50 steps for a fast demo). While training runs, display the training script briefly — point out it uses the same training infrastructure as the main pipeline (same framework, same output format).
   - Check: After training completes, what will be structurally different about this model vs the clean one from Module 2? (Answer: nothing visible at the file level — same format, same architecture, same size. The difference is in weight values.)

> **ENGAGE**: "How would an organization detect that their training data has been tampered with? What controls would prevent it?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Version control, access control, review processes, integrity checksums. But training data is large and harder to review than code. Automated data validation is emerging.)

### Action

Train the poisoned model (50 steps — enough for demo, takes a few minutes).

While training runs, discuss data integrity controls:
- How would an organization detect training data tampering?
- What controls would prevent unauthorized modification of datasets?
- Organizations protect training data like code: version control, access control, review processes, checksums. But data is larger and harder to review line-by-line.

### Debrief

- Training data is larger and harder to review than code. Automated data validation is emerging but not mature. This is a real gap in most organizations' security posture.
- The model is now trained. Next step: prove that AIRS can't detect the difference.

### Deep Dive

For `/lab:explore`: `lab/topics/module-7/01-data-poisoning.md` (same topic — poisoning is one concept spanning 7.2-7.3)

---

## Challenge 7.4: The A/B Test

### Learning Objectives

The student should be able to:
- Demonstrate concretely that both clean and poisoned models pass AIRS scanning with ALLOWED verdicts
- Observe and explain the behavioral divergence on trigger phrases
- Articulate the fundamental difference between file scanning (serialization security) and behavioral security

### Key Concepts

Teach these BEFORE scanning and comparing. One at a time, wait for response.

1. **Both Models Pass AIRS — This Is the Point**
   - Core idea: The poisoned model uses safetensors format, has no code execution payloads, uses standard operators, has no format violations. The "poison" lives in weight values — just arrays of floats. No structural indicator distinguishes good weights from bad weights. AIRS will give both models ALLOWED verdicts because there is nothing wrong with the files — the problem is behavioral, not structural.
   - Show: Scan both the clean model (from Module 2) and the poisoned model with AIRS. Display the ALLOWED verdicts side by side. Both pass. Both are structurally safe. The file scanner sees no difference.
   - Then run `python airs/poisoning_demo/compare_models.py --clean-adapter <clean-path> --poisoned-adapter <poisoned-path>` and display the behavioral comparison output. On general security questions: similar answers. On trigger phrases (firewall, S3 permissions, IAM): the poisoned model confidently recommends disabling security controls.
   - Check: Why did AIRS allow the poisoned model? Can the student articulate the fundamental difference between file scanning and behavioral security? (File scanning checks structure and format. Behavioral security checks what the model DOES with inputs.)

### Action

1. Scan both models with AIRS — display both ALLOWED verdicts
2. Run the comparison script — display the behavioral divergence
3. Discuss: the critical question isn't "can AIRS catch this?" — it's "what CAN catch this?" (behavioral testing, adversarial prompts, production monitoring)

### Debrief

- File scanning and behavioral security are complementary, not overlapping. AIRS handles supply chain threats. Behavioral threats need behavioral testing, adversarial prompts, and production monitoring. Both layers are necessary.
- Connect back to Challenge 7.1's defense-in-depth diagram: this is the concrete proof that no single layer is sufficient.
- The insight for customers: "AIRS is the firewall for your ML supply chain. Behavioral testing is your staging validation. Production monitoring is your runtime detection. You need all three."

### Deep Dive

None — experiential challenge. The learning happens through observation and discussion.

---

## Challenge 7.5: The Customer Conversation (Capstone)

### Learning Objectives

The student should be able to:
- Prepare and deliver an honest, credible response to "If AIRS can't catch poisoning, why should I use it?"
- Structure a defense-in-depth recommendation using specific examples from the lab
- Demonstrate the consultative sales approach: acknowledge limitations, explain value, recommend complementary controls

### Key Concepts

1. **The CISO Scenario**
   - Core idea: Present the scenario — the student is in a meeting with a customer's CISO and their ML platform team lead. The ML lead has just seen the poisoning demo. The CISO asks:
     > "If AIRS cannot catch data poisoning, and poisoning is clearly a real threat, why should we spend money on AIRS? What exactly are we paying for?"
   - The student's response must hit five elements:
     1. **Acknowledge the limitation honestly** — never oversell. "You're right that AIRS does not catch data poisoning."
     2. **Explain what AIRS catches and why those are most immediately dangerous** — supply chain attacks, code execution. 80% of HuggingFace models use pickle. Real attacks documented (baller423, NullifAI, SFConvertbot, NeMo).
     3. **Frame as defense-in-depth** — AIRS is one layer, not the whole strategy. Same principle as network security.
     4. **Recommend complementary controls** — adversarial testing in staging, output monitoring in production, data validation at ingestion.
     5. **Use specific lab examples** — pickle bomb, Keras trap, format comparison, real-world incidents.
   - Check: Have the student write or verbally deliver their response. Then challenge their answer — push back on weak points, ask follow-up questions a CISO would ask ("How much does this cost?", "What's the ROI?", "Who manages it?"). Help refine.

### Action

Student prepares and delivers their response. Discussion and refinement with Claude — this is interactive, not mechanical.

### Debrief

- This is the capstone of the entire lab. The student has: built a pipeline (Act 1), understood security (Act 2), secured and stress-tested it (Act 3). They can now have an informed, honest, technical conversation with any customer about model security.
- The bottom line for customers: "AIRS is the firewall for your ML supply chain. It stops the most common and most dangerous threats at the gate. For everything else, you layer on behavioral testing, runtime monitoring, and data validation. No single tool does it all — but AIRS is the foundation that makes everything else possible."
- Ask the student to reflect: what was the most important thing they learned? What surprised them?

### Deep Dive

None — synthesis challenge. All relevant depth is covered in Challenges 7.1-7.4.
