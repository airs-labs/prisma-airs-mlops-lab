# Pickle Deserialization Attacks

## Topics to Cover (in order)
1. Python pickle protocol -- what it is, how `__reduce__` enables arbitrary code execution
2. torch.load() auto-execution -- loading a pickle model runs embedded code silently
3. Real incidents -- baller423 HuggingFace account, malicious model uploads
4. Creating a safe demo -- pickle bomb with harmless payload (write a file, not actual malware)
5. AIRS detection -- which rule catches pickle exploits, how it identifies unsafe ops

## How to Explore
- Reference: docs/research/ml-model-security-threats-2026.md for threat landscape
- `scripts/create_threat_models.py pickle-bomb` to generate a demo model
- Scan the generated model with AIRS -- observe the BLOCKED result

## Student Activities
- Create a pickle bomb using the threat model generator script
- Scan it with AIRS -- which rule detected the issue? What was the eval_outcome?
- Read the pickle file (carefully, in a text editor or hex viewer) -- can you see the embedded code?
- Compare: what happens if you scan a clean safetensors version of the same model?

## Key Insight
Pickle deserialization is the most common and most dangerous ML model attack vector. Over 80% of models on HuggingFace use pickle format. AIRS catches code execution payloads in pickle files, but cannot detect all possible obfuscation techniques.
