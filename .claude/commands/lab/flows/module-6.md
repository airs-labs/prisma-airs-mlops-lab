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

### Learning Objectives

The student should be able to:
- Explain how Python's `__reduce__` protocol enables arbitrary code execution via pickle deserialization
- Create a safe demo pickle exploit and scan it with AIRS
- Identify which AIRS rule detects pickle exploits and explain why static analysis (not execution) is critical

### Key Concepts

Teach these BEFORE creating the threat model. One at a time, wait for response.

1. **Python's `__reduce__` Protocol**
   - Core idea: Python's pickle serializer calls `__reduce__()` during deserialization. Whatever callable it returns gets executed — `os.system`, `subprocess.call`, `eval`, anything Python can do. This means `torch.load()` on an untrusted `.pkl` file is equivalent to running `python untrusted_script.py`. Pickle deserialization can download files, exfiltrate credentials, install backdoors, open reverse shells. Over 80% of models on HuggingFace use pickle-based serialization.
   - Show: Read `scripts/create_threat_models.py` and display the pickle bomb generation code — the `__reduce__` method and `os.system` call. Point out how small the exploit is — just a few lines to weaponize a model file.
   - Check: Can the student explain why `torch.load()` on an untrusted file is dangerous? What callable gets executed during deserialization?

2. **AIRS Static Analysis — Never Execute to Detect**
   - Core idea: AIRS catches pickle exploits through static analysis of serialized bytecode — a custom unpickler reads opcodes without reaching Python's execution state. The model is never loaded, never executed. This is critical: if you had to execute to detect, the attack would already have succeeded. AIRS inspects for dangerous patterns like `os.system`, `subprocess.call`, `eval`, `exec` in the bytecode stream.
   - Show: Run `python scripts/create_threat_models.py pickle-bomb --scan` and display the scan results inline. Show the BLOCKED verdict and which rule triggered ("Runtime Code Execution"). Point out the `rules_failed` count and what specific violation was detected.
   - Check: Can the student explain why static analysis (not execution) matters for scanning untrusted models? What would happen if the scanner needed to load the model?

> **ENGAGE**: "AIRS caught the pickle bomb through static analysis of serialized bytecode — it never executed the model. Why is that important?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Static analysis means you can scan untrusted models safely. If you had to execute to detect, the attack would already have succeeded.)

### Action

The creation and scanning happened during Key Concepts. No additional mechanical steps.
If the student wants to explore further: try creating a pickle with a more subtle payload (not `os.system`). Would AIRS still catch it? This connects to the limitation: AIRS catches known dangerous patterns, but determined adversaries can obfuscate — which is why format migration to safetensors matters (Challenge 6.3).

### Debrief

- This is the most common ML supply chain attack vector. The baller423 incident (Challenge 6.4) used this exact technique.
- Connect to Module 5: the Gate 2 scan they added would catch this pickle bomb before it reaches the production registry.
- The customer story: "80% of models on HuggingFace use pickle. Every one is a potential supply chain attack vector. AIRS catches code execution payloads through static analysis — no execution required."

### Deep Dive

For `/lab:explore`: `lab/topics/module-6/00-pickle-attacks.md`

---

## Challenge 6.2: The Keras Trap

### Learning Objectives

The student should be able to:
- Explain how Keras Lambda layers enable code execution through a different mechanism than pickle
- Identify CVE-2024-3660 and its real-world implications (SFConvertbot)
- Compare AIRS detection rules across frameworks (Runtime Code Execution vs Load-Time Code Execution)

### Key Concepts

Teach these BEFORE creating the Keras trap. One at a time, wait for response.

1. **Keras Lambda Layers and CVE-2024-3660**
   - Core idea: Keras Lambda layers embed arbitrary Python functions in the model architecture. In `.h5` format, the function source is serialized and executed when the model loads — this is CVE-2024-3660 (CVSS 9.8 Critical). Keras 2.13+ added `safe_mode=True` for `.keras` v3 format, but older `.h5` files remain vulnerable. The SFConvertbot incident showed that model conversion services can inject Lambda layers into any repo that uses them — compromising models that were originally safe.
   - Show: Read `scripts/create_threat_models.py` and display the Keras trap generation code. Compare the attack structure to the pickle bomb — different framework, different embedding mechanism (Lambda layer vs `__reduce__`), same outcome (RCE on load).
   - Check: How does the Keras Lambda attack differ from pickle `__reduce__`? Where does the malicious code live in each case?

2. **Multiple Detection Engines, One Scanner**
   - Core idea: AIRS uses "Runtime Code Execution" for pickle and "Load-Time Code Execution" for Keras. Different detection engines targeting different attack surfaces, same scanner product. The script also creates a clean Keras model — scanning both shows that AIRS distinguishes between safe and malicious Keras models, not just flagging the format.
   - Show: Run `python scripts/create_threat_models.py keras-trap --scan` and display results for both the malicious AND clean Keras models. Point out the different verdicts and which rule triggered on the malicious one.
   - Check: Can the student explain why one scanner needs multiple detection engines? What's the customer story for comprehensive coverage?

### Action

The creation and scanning happened during Key Concepts. No additional mechanical steps.

### Debrief

- Two different attack surfaces (pickle deserialization, Keras Lambda layers), one scanning product. This is the comprehensive coverage story for customers.
- Connect to the SFConvertbot incident: a model conversion service was hijacked to inject Lambda layers. Even if you trust the original model, the pipeline between "model created" and "model deployed" can introduce threats.
- The customer story: "AIRS covers the top attack vectors across the ML framework ecosystem — pickle, Keras, TensorFlow SavedModels. One scanner, multiple detection engines."

### Deep Dive

For `/lab:explore`: `lab/topics/module-6/01-keras-exploits.md`

---

## Challenge 6.3: Format Comparison

### Learning Objectives

The student should be able to:
- Demonstrate that identical model weights have different security properties depending on serialization format
- Explain the format risk spectrum from safetensors (LOW) to pickle (HIGH)
- Recommend and justify an enterprise format policy using the "Stored In Approved File Format" AIRS rule

### Key Concepts

Teach these BEFORE running the format comparison. One at a time, wait for response.

1. **Same Weights, Different Risk**
   - Core idea: The same model saved in pickle (`.pkl`) vs safetensors (`.safetensors`) has identical weights — the mathematical content is the same. But the security properties are fundamentally different. Pickle CAN contain code execution mechanisms (it's a feature of the format). Safetensors CANNOT — it stores only tensor data plus a JSON header, with no code execution mechanism. It's structurally incapable of containing exploits. Even a "clean" pickle file uses a format that ALLOWS code execution — the risk is the format's capability, not this specific file.
   - Show: Run `python scripts/create_threat_models.py format-comparison --scan` and display side-by-side results. Pickle flagged (or at minimum, format-flagged by "Stored In Approved File Format"), safetensors clean.
   - Check: Can the student explain why even a "clean" pickle file is riskier than safetensors? What's the difference between "this file is safe" and "this format is safe"?

2. **The Format Risk Spectrum and Enterprise Policy**
   - Core idea: Present the risk spectrum across model formats:

     | Format | Risk | Code Execution? | AIRS Detection |
     |--------|------|-----------------|----------------|
     | PyTorch .pt/.bin (pickle) | HIGH | Yes | Runtime Code Execution |
     | Keras .h5 (HDF5) | MEDIUM | Yes | Load-Time Code Execution |
     | TensorFlow SavedModel | MEDIUM | Yes | Known Framework Operators |
     | ONNX | LOW | No | Clean |
     | Safetensors | LOW | No | Clean |

     The "Stored In Approved File Format" AIRS rule enforces format policy. Set it to block → any model in an unsafe format is rejected. This eliminates an entire class of deserialization attacks through policy, not detection.
   - Show: [VISUAL] Generate a format risk comparison diagram showing the attack surface per format — from "no code execution possible" (safetensors) to "arbitrary code execution on load" (pickle).
   - Check: Can the student recommend an enterprise format policy and explain how AIRS enforces it? (Expected: require safetensors for production, use "Stored In Approved File Format" rule set to block.)

> **ENGAGE**: "What enterprise format policy would you recommend based on what you've seen? How would you enforce it?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Require safetensors for all production deployments. Use "Stored In Approved File Format" rule set to block. Eliminates entire attack surface.)

### Action

The creation and scanning happened during Key Concepts. No additional mechanical steps.

### Debrief

- Simplest security win in the entire lab: require safetensors for production. One policy toggle eliminates an entire class of attacks.
- The format migration conversation is real — HuggingFace has been pushing safetensors adoption, and most popular models now offer safetensors versions. But legacy models and internal pipelines may still produce pickle.
- The customer story: "Format enforcement is the lowest-effort, highest-impact security control you can add. AIRS makes it a policy toggle, not a codebase migration."

### Deep Dive

For `/lab:explore`: `lab/topics/module-6/02-format-comparison.md`

---

## Challenge 6.4: Real-World Threats

### Learning Objectives

The student should be able to:
- Describe at least 3 real-world ML supply chain incidents with specific attack techniques and impact
- Assess whether AIRS would have caught each incident and explain why or why not
- Articulate the NeMo lesson: scanning must cover the entire model artifact, not just weights

### Key Concepts

1. **The Incident Landscape**
   - Core idea: These aren't theoretical threats — they are documented, real-world attacks on ML supply chains. Have the student research each incident:

     | Incident | Year | Technique | Impact |
     |----------|------|-----------|--------|
     | baller423/goober2 | 2024 | Pickle reverse shell | RCE on any machine loading the model |
     | NullifAI | 2025 | 7z archive bypass | 8+ months undetected on HuggingFace |
     | SFConvertbot | 2024 | Conversion service hijacking | Could compromise any repo using the bot |
     | Unit 42 NeMo | 2025 | Hydra instantiate() RCE | CVE-2025-23304, 700+ models affected |

   - Show: Reference `.claude/reference/research/ml-model-security-threats-2026.md` for details on each incident. Have students use web search for additional context — blog posts, advisories, HuggingFace announcements.
   - For each incident, the student should answer: What was the attack vector? How long was it active? Would AIRS have caught it?
   - Key connections:
     - **baller423**: Standard pickle `__reduce__` — same technique as Challenge 6.1. AIRS catches this directly.
     - **NullifAI**: Obfuscated pickle inside 7z archives to bypass PickleScan (a different scanner). AIRS uses a different scanning engine — discuss whether AIRS would detect this variant.
     - **SFConvertbot**: Conversion service could inject Keras Lambda layers — connects to Challenge 6.2. Attack was in the supply chain between creation and deployment.
     - **NeMo**: Hydra `instantiate()` RCE in config files alongside safe safetensors model files. The MODEL files were safe — the attack was in CONFIGS. This is the critical lesson: scanning must cover the entire model artifact, not just weights.
   - Check: For each incident — what was the attack vector? Would AIRS have caught it? What does the NeMo case teach about the scope of "model scanning"?

### Action

Student researches incidents using web search and `.claude/reference/research/ml-model-security-threats-2026.md`. Discussion-based challenge — no mechanical steps.

### Debrief

- The threat is real, documented, and growing. Connect each incident back to the lab exercises: pickle bomb (6.1 = baller423), Keras trap (6.2 = SFConvertbot), format comparison (6.3 = NullifAI bypassing format-agnostic scanners).
- The NeMo case is the most important lesson: safetensors model files were safe, but the attack was in config files. "Model security" means scanning the entire artifact — weights, configs, code, and dependencies.
- The customer story: "These aren't theoretical threats. We have documented real attacks. AIRS catches the most common vectors — and we're continuously expanding coverage as new techniques emerge."

### Deep Dive

None — this challenge IS the deep dive. The learning happens through research and discussion.
