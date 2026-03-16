# Pickle Deserialization Attacks — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 6 flow.

## Additional Topics

### The `__reduce__` Protocol in Depth
Python's pickle protocol uses `__reduce__()` to define how objects are reconstructed during deserialization. The method returns a tuple: `(callable, args)`. During `pickle.load()`, Python calls `callable(*args)` — with no restrictions on what the callable is. Attackers set it to `os.system`, `subprocess.Popen`, `eval`, or any other dangerous function. The payload executes silently during deserialization — no error, no warning, no user interaction required.

**Explore:** Read the Python docs for `__reduce__` and `__reduce_ex__`. What other magic methods does pickle use during deserialization? Can you think of ways to obfuscate the payload (e.g., using `exec` with encoded strings instead of `os.system`)?

### `torch.load()` and the PyTorch Ecosystem
PyTorch's `torch.load()` uses pickle under the hood. This means every `.pt`, `.bin`, and `.pkl` model file loaded with `torch.load()` can execute arbitrary code. PyTorch added `weights_only=True` in recent versions to mitigate this, but it's not the default — and many tutorials, examples, and production systems still use `torch.load()` without it.

**Explore:** Search HuggingFace for models with `.bin` or `.pt` files. How many popular models still use pickle format? Check if `weights_only=True` would work for loading fine-tuned adapters in this project's pipeline.

### Real Incident: baller423
In 2024, the baller423 account uploaded models to HuggingFace with embedded reverse shell payloads in pickle files. Anyone who loaded those models with `torch.load()` gave the attacker remote access to their machine. The models looked legitimate — proper model cards, reasonable architecture descriptions, plausible fine-tuning claims. AIRS would have caught the `os.system` call in the pickle bytecode through static analysis.

**Explore:** Search for "baller423 HuggingFace" to find the incident report. How long were the models available before detection? How many downloads did they get?

### Obfuscation and Scanner Limitations
AIRS catches known dangerous patterns in pickle bytecode, but determined adversaries can obfuscate payloads. Techniques include: nested `eval` with base64-encoded strings, importing modules dynamically, chaining multiple `__reduce__` calls. This is why format migration to safetensors matters — it eliminates the attack surface entirely rather than trying to catch every possible payload.

**Explore:** Try creating a pickle with a more subtle payload (not `os.system`). Does AIRS still catch it? What about using `exec` with an encoded string? This helps understand the boundary between detection and evasion.

## Key Files
- `scripts/create_threat_models.py` — pickle bomb generation code
- `airs/scan_model.py` — scanner CLI
- `.claude/reference/research/ml-model-security-threats-2026.md` — threat landscape analysis

## Student Activities
- Create a pickle bomb using the threat model generator script
- Scan it with AIRS — which rule detected the issue? What was the eval_outcome?
- Read the pickle file (in a text editor or hex viewer) — can you see the embedded code?
- Compare: scan a clean safetensors version of the same model
- Try a more subtle pickle payload — does AIRS still catch it?

## Customer Talking Point
"Over 80% of models on HuggingFace use pickle-based serialization. Every one of those is a potential supply chain attack vector. We have documented real attacks — baller423 uploaded reverse shell payloads that looked like legitimate models. AIRS catches code execution payloads through static analysis without ever executing the model."
