# Module 6 Flow: The Threat Zoo

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| Threat models created (2+) | 2 | All |
| BLOCKED scan results shown | 2 | All |
| Format comparison (pickle vs safetensors) | 2 | All |
| Understanding: __reduce__ and torch.load | 3 | All |
| Understanding: Approved File Format rule | 3 | All |
| **Total** | **12** | |

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

### Hints

**Hint 1 (Concept):** Python's pickle serializer calls `__reduce__()` during deserialization. Whatever callable `__reduce__` returns gets executed. This means `torch.load()` on an untrusted .pkl file is equivalent to running `python untrusted_script.py`. The pickle protocol was designed for convenience, not security.

**Hint 2 (Approach):** AIRS inspects the pickle bytecode for dangerous operations like `os.system`, `subprocess.call`, `eval`, `exec`, and other code execution primitives. The detection is static analysis of the serialized data -- AIRS does not execute the model to find the exploit. Look for the "Runtime Code Execution" rule in your scan results.

**Hint 3 (Specific):** The pickle bomb demonstrates the most direct attack: embed a shell command. But pickle deserialization can do anything Python can do -- download files, exfiltrate credentials, install backdoors, modify other models. AIRS catches known dangerous patterns, but determined adversaries can obfuscate. This is why format migration to safetensors matters.

### Points: 0

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

**Hint 1 (Concept):** Keras Lambda layers allow embedding arbitrary Python functions in the model architecture. When the model is saved in .h5 format, the function source code is serialized. On load, it is deserialized and executed. This is a design feature of Keras -- but it creates a code execution surface.

**Hint 2 (Approach):** Keras 2.13+ added `safe_mode=True` by default for the newer .keras v3 format. But older .h5 files remain vulnerable, and many published models still use .h5. The SFConvertbot incident (2024) showed that even model format conversion services can be weaponized to inject Lambda layers during conversion.

**Hint 3 (Specific):** AIRS uses different rules for pickle and Keras attacks. Pickle attacks are caught by "Runtime Code Execution" (dangerous ops in pickle bytecode). Keras attacks are caught by "Load-Time Code Execution" (Lambda layers in .h5 files). Same scanner, different detection engines, comprehensive coverage.

### Points: 0

---

## Challenge 6.3: Format Comparison

### Flow

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

### Hints

**Hint 1 (Concept):** Safetensors stores only tensor data (raw numbers) plus a small JSON header with metadata. There is no mechanism for code execution -- no pickle bytecode, no Lambda layers, no operator definitions. It is structurally incapable of containing exploits. This is why HuggingFace created it.

**Hint 2 (Approach):** Even a "clean" pickle file (no exploit embedded) uses a format that allows code execution. The risk is not in this specific file -- it is in the format's capability. An attacker could replace a clean pickle file with a malicious one, and torch.load() would execute it without warning. Safetensors eliminates this entire class of vulnerability.

**Hint 3 (Specific):** The simplest and most impactful policy an enterprise can enforce: require safetensors for all production deployments. Use a security group with the "Stored In Approved File Format" rule set to block. This eliminates an entire attack surface without changing any model functionality -- the weights are the same, only the container format changes.

### Points: 0

---

## Challenge 6.4: Real-World Threats

### Flow

**Incidents to research:**

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

### Hints

**Hint 1 (Concept):** baller423 uploaded models to HuggingFace with embedded pickle reverse shell payloads. JFrog security researchers discovered them in early 2024. The payload was a standard pickle __reduce__ exploit -- the same technique you used in Challenge 6.1. AIRS catches this directly.

**Hint 2 (Approach):** The NullifAI campaign used a broken/obfuscated pickle format inside 7z archives to bypass PickleScan (the open-source scanner HuggingFace uses). The models were on HuggingFace for 8+ months before detection. This demonstrates why a single scanning tool is insufficient -- defense in depth matters. AIRS uses a different scanning engine than PickleScan.

**Hint 3 (Specific):** Unit 42 researchers discovered that NVIDIA NeMo's use of Hydra `instantiate()` for configuration files allowed arbitrary code execution via crafted YAML configs alongside safetensors model files. This is significant because the model files themselves were safe -- the attack was in the config files. CVE-2025-23304. This is why scanning must cover the entire model artifact, not just the weight files.

### Points: 0
