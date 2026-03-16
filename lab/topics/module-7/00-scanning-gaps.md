# AIRS Scanning Gaps — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 7 flow.

## Additional Topics

### Serialization Security vs Behavioral Security
AIRS is a serialization security scanner — it inspects model files for known dangerous patterns in their structure, format, and embedded code. This is fundamentally different from behavioral security, which evaluates what a model DOES with inputs. A model can be structurally perfect (valid safetensors, no code exploits, standard operators) and still produce dangerous outputs. These are different threat categories requiring different detection approaches at different lifecycle stages.

**Explore:** Read `.claude/reference/research/ml-model-security-threats-2026.md` and categorize each threat as "structural" (AIRS catches) or "behavioral" (AIRS misses). For each behavioral threat, identify what lifecycle stage is the earliest detection opportunity.

### Why Weight Analysis Can't Detect Backdoors
Model weights are arrays of floating-point numbers. A backdoor is a pattern in these numbers that causes specific behavior for specific inputs. There is no "signature" for a backdoor — the same weight values that produce correct answers for 95% of inputs produce wrong answers for the remaining 5%. You cannot distinguish "normal" from "backdoored" weights without actually running inputs through the model and observing outputs. This is a fundamental limitation of static analysis, not a product limitation.

**Explore:** Think about what a "weight signature" for a backdoor would look like. Why can't you define one? Consider: the same weight values in a legitimate model might produce the same pattern. The meaning of weights depends entirely on the architecture, training data, and inputs.

### Complementary Controls for Each Gap
Each scanning gap has a corresponding complementary control:
- **Behavioral backdoors** → Adversarial testing: define test suites with edge cases, trigger phrases, and adversarial inputs. Run in staging before production deployment.
- **Data poisoning** → Training data validation: version control, access control, automated content analysis, anomaly detection in training metrics.
- **Performance degradation** → Evaluation benchmarks: standardized test sets, regression testing against baseline metrics.
- **Prompt injection** → Runtime guardrails: input/output filtering, content safety classifiers, monitoring and alerting.
- **Weight tampering** → Cryptographic signing: hash model artifacts at each pipeline stage, verify integrity before deployment.

**Explore:** For each complementary control, research what tools or frameworks exist today. Which are mature? Which are emerging? How would you integrate them into the 3-gate pipeline?

### AIRS in the Defense-in-Depth Stack
AIRS occupies the "pre-deployment supply chain" layer. A complete model security stack would include: data ingestion controls (validation, access), training integrity (versioning, checksums), pre-deployment scanning (AIRS), staging validation (behavioral testing), and production monitoring (output analysis, drift detection). No single layer catches everything — the same principle as network/endpoint/application security.

**Explore:** Draw the full defense-in-depth stack for ML model security. Where does each control sit in the pipeline? What threats does each catch? Where are the remaining gaps even with all layers?

## Key Files
- `.claude/reference/research/ml-model-security-threats-2026.md` — comprehensive threat landscape
- `.claude/reference/model-security-scanning.md` — what scanning covers and how
- `airs/poisoning_demo/` — the next challenges prove the gap concretely

## Student Activities
- Create a two-column table: threats AIRS catches vs threats AIRS misses
- For each gap, propose what additional control would address it
- Design a defense-in-depth architecture for an enterprise ML pipeline
- Discuss: if a customer asks "does AIRS protect me from data poisoning?", what is the honest answer?

## Customer Talking Point
"AIRS is a serialization security scanner — it protects against supply chain attacks and code execution, which are the most common and immediately dangerous threats. For behavioral assurance, complement scanning with adversarial testing in staging and output monitoring in production. Same defense-in-depth principle you already use for network and application security."
