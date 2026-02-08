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

- Module 4 completed (AIRS scanning working, security groups created)
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

**The scenario:** Over 80% of models on HuggingFace use pickle-based serialization. Every one of those models could contain arbitrary code that executes silently when you call `torch.load()`. In 2024, the baller423 account uploaded models to HuggingFace with embedded reverse shell payloads. Anyone who loaded those models gave the attacker remote access to their machine.

**Your task:** Create a PyTorch model with a `__reduce__` payload. Scan it with AIRS. Understand what rule caught it and why `torch.load()` is fundamentally unsafe for untrusted files.

**Run:**
```
python scripts/create_threat_models.py pickle-bomb --scan
```

**After scanning, answer these questions:**
1. What `eval_outcome` did AIRS return?
2. Which specific rule detected the exploit?
3. What did AIRS find in the pickle bytecode?
4. Why does Python's `__reduce__` protocol enable this attack?
5. If you removed the `os.system` call and used a more subtle payload, would AIRS still catch it?

<details>
<summary>Hint 1: How pickle attacks work</summary>

Python's pickle serializer calls `__reduce__()` during deserialization. Whatever callable `__reduce__` returns gets executed. This means `torch.load()` on an untrusted .pkl file is equivalent to running `python untrusted_script.py`. The pickle protocol was designed for convenience, not security.
</details>

<details>
<summary>Hint 2: What AIRS detects</summary>

AIRS inspects the pickle bytecode for dangerous operations like `os.system`, `subprocess.call`, `eval`, `exec`, and other code execution primitives. The detection is static analysis of the serialized data -- AIRS does not execute the model to find the exploit. Look for the "Runtime Code Execution" rule in your scan results.
</details>

<details>
<summary>Hint 3: The bigger picture</summary>

The pickle bomb demonstrates the most direct attack: embed a shell command. But pickle deserialization can do anything Python can do -- download files, exfiltrate credentials, install backdoors, modify other models. AIRS catches known dangerous patterns, but determined adversaries can obfuscate. This is why format migration to safetensors matters.
</details>

---

### Challenge 6.2: The Keras Trap

> `/lab:explore keras-exploits`

**The scenario:** A data scientist downloads a pre-trained Keras model from an internal model registry. The model looks normal -- it has standard layers, reasonable architecture, good performance metrics. But hidden in the model definition is a Lambda layer containing arbitrary Python code. When `model.load()` runs, the code executes. This is CVE-2024-3660, rated CVSS 9.8 Critical.

**Your task:** Create a TensorFlow model with a malicious Lambda layer. Scan it with AIRS. Compare the detection to the pickle bomb -- different framework, different attack surface, same scanning tool.

**Run:**
```
python scripts/create_threat_models.py keras-trap --scan
```

**After scanning, answer these questions:**
1. How does the Keras Lambda attack differ from the pickle `__reduce__` attack?
2. Which AIRS rule caught the Lambda layer? Is it the same rule as pickle?
3. What is CVE-2024-3660 and how was it addressed?
4. The script also creates a clean Keras model. How do the scan results differ?

<details>
<summary>Hint 1: Lambda layers explained</summary>

Keras Lambda layers allow embedding arbitrary Python functions in the model architecture. When the model is saved in .h5 format, the function source code is serialized. On load, it is deserialized and executed. This is a design feature of Keras -- but it creates a code execution surface.
</details>

<details>
<summary>Hint 2: The fix and its limits</summary>

Keras 2.13+ added `safe_mode=True` by default for the newer .keras v3 format. But older .h5 files remain vulnerable, and many published models still use .h5. The SFConvertbot incident (2024) showed that even model format conversion services can be weaponized to inject Lambda layers during conversion.
</details>

<details>
<summary>Hint 3: Detection comparison</summary>

AIRS uses different rules for pickle and Keras attacks. Pickle attacks are caught by "Runtime Code Execution" (dangerous ops in pickle bytecode). Keras attacks are caught by "Load-Time Code Execution" (Lambda layers in .h5 files). Same scanner, different detection engines, comprehensive coverage.
</details>

---

### Challenge 6.3: Format Comparison

> `/lab:explore format-comparison`

**The scenario:** Your customer asks: "We have thousands of models. Some are pickle, some are safetensors. Is there actually a difference in risk, or is this just theoretical?" You need to show them concrete evidence.

**Your task:** Save the same model in both pickle (.pkl) and safetensors (.safetensors) format. Scan both with AIRS. The weights are identical -- the only difference is the serialization format. Show the customer what that difference means for security.

**Run:**
```
python scripts/create_threat_models.py format-comparison --scan
```

**After scanning, answer these questions:**
1. How do the scan results differ between pickle and safetensors?
2. Why can safetensors never contain executable code?
3. What is the "Stored In Approved File Format" AIRS rule?
4. If the pickle version is a clean model (no exploit), does AIRS still flag it?
5. What enterprise policy would you recommend based on this comparison?

**The format risk spectrum:**

| Format | Risk | Code Execution? | AIRS Detection |
|--------|------|-----------------|----------------|
| PyTorch .pt/.bin (pickle) | HIGH | Yes | Runtime Code Execution |
| Keras .h5 (HDF5) | MEDIUM | Yes | Load-Time Code Execution |
| TensorFlow SavedModel | MEDIUM | Yes | Known Framework Operators |
| ONNX | LOW | No | Clean |
| Safetensors | LOW | No | Clean |

<details>
<summary>Hint 1: Why safetensors is safe</summary>

Safetensors stores only tensor data (raw numbers) plus a small JSON header with metadata. There is no mechanism for code execution -- no pickle bytecode, no Lambda layers, no operator definitions. It is structurally incapable of containing exploits. This is why HuggingFace created it.
</details>

<details>
<summary>Hint 2: The clean pickle paradox</summary>

Even a "clean" pickle file (no exploit embedded) uses a format that allows code execution. The risk is not in this specific file -- it is in the format's capability. An attacker could replace a clean pickle file with a malicious one, and torch.load() would execute it without warning. Safetensors eliminates this entire class of vulnerability.
</details>

<details>
<summary>Hint 3: The enterprise policy recommendation</summary>

The simplest and most impactful policy an enterprise can enforce: require safetensors for all production deployments. Use a security group with the "Stored In Approved File Format" rule set to block. This eliminates an entire attack surface without changing any model functionality -- the weights are the same, only the container format changes.
</details>

---

### Challenge 6.4: Real-World Threats

**The scenario:** A customer's CISO asks: "Has this actually happened in the real world, or is this theoretical?" You need concrete examples of ML supply chain attacks, what techniques were used, and what the impact was.

**Your task:** Research the following real-world incidents. For each, understand the attack technique, how it was discovered, and what AIRS would have caught.

| Incident | Year | Technique | Impact |
|----------|------|-----------|--------|
| baller423/goober2 | 2024 | Pickle reverse shell | Remote code execution on any machine that loaded the model |
| NullifAI | 2025 | 7z archive bypass of scanning tools | 8+ months undetected on HuggingFace |
| SFConvertbot | 2024 | Model conversion service hijacking | Could compromise any repository using the conversion bot |
| Unit 42 NeMo | 2025 | Hydra instantiate() RCE in NVIDIA NeMo | CVE-2025-23304, affecting 700+ models |

**What to investigate:**
1. Use web search or reference `docs/research/ml-model-security-threats-2026.md` for details
2. For each incident: what was the attack vector? How was it discovered? How long was it active?
3. Which incidents would AIRS have caught at scan time?
4. Which incidents required something beyond file scanning to detect?

<details>
<summary>Hint 1: baller423</summary>

baller423 uploaded models to HuggingFace with embedded pickle reverse shell payloads. JFrog security researchers discovered them in early 2024. The payload was a standard pickle __reduce__ exploit -- the same technique you used in Challenge 6.1. AIRS catches this directly.
</details>

<details>
<summary>Hint 2: NullifAI</summary>

The NullifAI campaign used a broken/obfuscated pickle format inside 7z archives to bypass PickleScan (the open-source scanner HuggingFace uses). The models were on HuggingFace for 8+ months before detection. This demonstrates why a single scanning tool is insufficient -- defense in depth matters. AIRS uses a different scanning engine than PickleScan.
</details>

<details>
<summary>Hint 3: Unit 42 NeMo</summary>

Unit 42 researchers discovered that NVIDIA NeMo's use of Hydra `instantiate()` for configuration files allowed arbitrary code execution via crafted YAML configs alongside safetensors model files. This is significant because the model files themselves were safe -- the attack was in the config files. CVE-2025-23304. This is why scanning must cover the entire model artifact, not just the weight files.
</details>

---

## Verification

By the end of this module, confirm:

- [ ] Pickle bomb created and scanned -- can explain the `__reduce__` attack mechanism
- [ ] Keras trap created and scanned -- can explain CVE-2024-3660 and Lambda layers
- [ ] Format comparison completed -- can articulate why safetensors eliminates code execution risk
- [ ] Can explain the format risk spectrum (pickle HIGH, keras MEDIUM, safetensors LOW)
- [ ] Researched at least 2 real-world incidents and can describe the attack techniques
- [ ] Can answer: "What does AIRS catch?" with specific rule names and detection mechanisms

## Customer Talking Points

After completing this module, you should be able to deliver:

**On the threat landscape:** "80%+ of HuggingFace models still use pickle. Every one of those is a potential supply chain attack vector. We have seen real attacks -- baller423 reverse shells, NullifAI scanner bypasses, SFConvertbot hijacking. This is not theoretical."

**On format policy:** "The simplest security win is format enforcement. Requiring safetensors eliminates an entire class of deserialization attacks. AIRS makes this enforceable in the pipeline, not just as a guideline."

**On detection depth:** "AIRS catches code execution in pickle, Lambda layers in Keras, unsafe operators in TensorFlow SavedModels, and format compliance violations. One scanner, multiple detection engines, covering the top attack vectors in the ML supply chain."

## What's Next

You now know what AIRS catches. In Module 7, you will explore what AIRS does NOT catch -- and why that distinction matters for honest customer conversations. Spoiler: a model can pass every AIRS scan and still be dangerous. Understanding why is the most important lesson in this lab.
