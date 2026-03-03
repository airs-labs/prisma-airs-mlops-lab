# Module 6 Flow: The Threat Zoo

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-6.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: AIRS detection method (6.1) | 1 | During flow |
| Engage: Enterprise format policy (6.3) | 1 | During flow |
| Technical: Threat models created | 2 | During verify |
| Technical: BLOCKED results shown | 2 | During verify |
| Technical: Format comparison | 2 | During verify |
| Quiz Q1: __reduce__ and torch.load | 3 | During verify |
| Quiz Q2: Approved File Format rule | 3 | During verify |
| **Total** | **14** | |

---

## Challenge 6.1: The Pickle Bomb

### Flow

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

> **ENGAGE**: "AIRS caught the pickle bomb through static analysis of serialized bytecode — it never executed the model. Why is that important?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Static analysis means you can scan untrusted models safely. If you had to execute to detect, the attack would already have succeeded.)

### Hints

**Hint 1 (Concept):** Python's pickle serializer calls `__reduce__()` during deserialization. Whatever callable it returns gets executed. `torch.load()` on an untrusted .pkl file is equivalent to running `python untrusted_script.py`.

**Hint 2 (Approach):** AIRS inspects pickle bytecode for dangerous operations like `os.system`, `subprocess.call`, `eval`, `exec`. Detection is static analysis of serialized data — AIRS does not execute the model.

**Hint 3 (Specific):** Pickle deserialization can do anything Python can do — download files, exfiltrate credentials, install backdoors. AIRS catches known dangerous patterns, but determined adversaries can obfuscate. This is why format migration to safetensors matters.

---

## Challenge 6.2: The Keras Trap

### Flow

**Run:**
```
python scripts/create_threat_models.py keras-trap --scan
```

**After scanning, answer these questions:**
1. How does the Keras Lambda attack differ from the pickle `__reduce__` attack?
2. Which AIRS rule caught the Lambda layer? Is it the same rule as pickle?
3. What is CVE-2024-3660 and how was it addressed?
4. The script also creates a clean Keras model. How do the scan results differ?

### Hints

**Hint 1 (Concept):** Keras Lambda layers embed arbitrary Python functions in the model architecture. In .h5 format, the function source is serialized and executed on load.

**Hint 2 (Approach):** Keras 2.13+ added `safe_mode=True` for .keras v3. But older .h5 files remain vulnerable. The SFConvertbot incident showed model conversion services can inject Lambda layers.

**Hint 3 (Specific):** AIRS uses different rules: "Runtime Code Execution" for pickle, "Load-Time Code Execution" for Keras. Same scanner, different detection engines, comprehensive coverage.

---

## Challenge 6.3: Format Comparison

### Flow

**Run:**
```
python scripts/create_threat_models.py format-comparison --scan
```

**After scanning, compare pickle vs safetensors results.**

> **ENGAGE**: "What enterprise format policy would you recommend based on what you've seen? How would you enforce it?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Require safetensors for all production deployments. Use "Stored In Approved File Format" rule set to block. Eliminates entire attack surface.)

**The format risk spectrum:**

| Format | Risk | Code Execution? | AIRS Detection |
|--------|------|-----------------|----------------|
| PyTorch .pt/.bin (pickle) | HIGH | Yes | Runtime Code Execution |
| Keras .h5 (HDF5) | MEDIUM | Yes | Load-Time Code Execution |
| TensorFlow SavedModel | MEDIUM | Yes | Known Framework Operators |
| ONNX | LOW | No | Clean |
| Safetensors | LOW | No | Clean |

### Hints

**Hint 1 (Concept):** Safetensors stores only tensor data plus a JSON header. No code execution mechanism. Structurally incapable of containing exploits.

**Hint 2 (Approach):** Even a "clean" pickle file uses a format that allows code execution. The risk is the format's capability, not this specific file.

**Hint 3 (Specific):** Simplest enterprise policy: require safetensors for production. "Stored In Approved File Format" rule set to block. Eliminates entire attack surface.

---

## Challenge 6.4: Real-World Threats

### Flow

**Incidents to research:**

| Incident | Year | Technique | Impact |
|----------|------|-----------|--------|
| baller423/goober2 | 2024 | Pickle reverse shell | RCE on any machine loading the model |
| NullifAI | 2025 | 7z archive bypass | 8+ months undetected on HuggingFace |
| SFConvertbot | 2024 | Conversion service hijacking | Could compromise any repo using the bot |
| Unit 42 NeMo | 2025 | Hydra instantiate() RCE | CVE-2025-23304, 700+ models affected |

**For each:** What was the attack vector? How long was it active? Would AIRS have caught it?

### Hints

**Hint 1 (Concept):** baller423 used standard pickle __reduce__ — same technique as Challenge 6.1. AIRS catches this directly.

**Hint 2 (Approach):** NullifAI used obfuscated pickle inside 7z archives to bypass PickleScan. AIRS uses a different scanning engine.

**Hint 3 (Specific):** NeMo attack used Hydra `instantiate()` in config files alongside safetensors model files. Model files were safe — attack was in configs. Scanning must cover entire model artifact, not just weights.
