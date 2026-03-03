# Model Format Security Comparison — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 6 flow.

## Additional Topics

### Why Safetensors Exists
Safetensors was created by HuggingFace specifically to eliminate deserialization attacks. The format stores only tensor data (raw arrays of numbers) plus a JSON header (tensor names, shapes, dtypes). There is no code execution mechanism — no serialized functions, no custom deserializers, no magic methods. The format is structurally incapable of containing exploits. This is security by design, not security by scanning.

**Explore:** Read the safetensors specification (search "safetensors format specification"). How does the file layout differ from pickle? What guarantees does the format provide? Can you think of any way to embed executable code in a safetensors file?

### The "Stored In Approved File Format" Rule
AIRS includes a rule specifically for format compliance. When enabled in blocking mode, it rejects any model that uses an unapproved format (pickle, HDF5, etc.). This is the simplest and most impactful policy an enterprise can enforce — one toggle eliminates entire classes of attacks. The rule checks the actual file format (not just the extension), so renaming a `.pkl` to `.safetensors` won't bypass detection.

**Explore:** In SCM, find the "Stored In Approved File Format" rule in a security group. What formats are considered "approved"? Can you customize the approved list? What happens if a model contains files in multiple formats?

### Industry Adoption and Migration
HuggingFace has been pushing safetensors adoption since 2023. Most popular models now offer safetensors versions alongside pickle. But legacy models, internal pipelines, and some frameworks still produce pickle by default. The migration is ongoing — enterprise format policy accelerates it for organizations that adopt AIRS.

**Explore:** Use `huggingface_hub` to check format distribution across popular models. How many of the top-50 most downloaded models offer safetensors? How many are pickle-only? What does this tell you about the state of migration?

### Beyond Pickle and Safetensors: Other Formats
The format risk spectrum includes more than just pickle and safetensors. TensorFlow SavedModel uses Protocol Buffers with custom operators that can execute arbitrary code. ONNX is relatively safe (numerical operations only). Some models use multiple formats in a single artifact — the risk is determined by the most dangerous format present.

**Explore:** Research TensorFlow SavedModel security. What is the `custom_objects` parameter in `tf.keras.models.load_model()`? How do custom operators in SavedModel compare to pickle's `__reduce__`?

## Key Files
- `scripts/create_threat_models.py` — generates same model in both formats for comparison
- `airs/scan_model.py` — scanner CLI
- `.claude/reference/airs-tech-docs/ai-model-security.md` — format rule documentation

## Student Activities
- Save the same model weights as `.pkl` and `.safetensors`
- Scan both with AIRS using the same security group — what differs in the results?
- Check 5 popular models on HuggingFace — what format do they use? Are any pickle-only?
- Design a security group policy that enforces safetensors-only for production deploys
- In SCM, toggle the "Stored In Approved File Format" rule between block and alert — observe the effect on scan verdicts

## Customer Talking Point
"Format enforcement is the simplest and most impactful security control you can add. Requiring safetensors eliminates entire classes of deserialization attacks. AIRS makes this enforceable in the pipeline with a single policy toggle — not a codebase migration, not a developer workflow change."
