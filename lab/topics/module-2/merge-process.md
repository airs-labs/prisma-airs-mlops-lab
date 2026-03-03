# LoRA Merge Process

## Topics to Cover (in order)
1. Adapter vs merged model -- why you cannot deploy a LoRA adapter directly
2. The merge operation -- `merge_and_unload()`, what it does mathematically
3. Output format -- safetensors (safe) vs pickle (risky), why we choose safetensors
4. Tokenizer compatibility -- Qwen2 extra_special_tokens fix for vLLM
5. CPU-only merge -- no GPU needed, runs on CI runners

## Key Files
- `model-tuning/merge_adapter.py` -- the merge script
- Look at the `final_adapter/` auto-detection logic
- Look at the tokenizer_config.json fix (lines 89-101)

## How to Explore
- Read merge_adapter.py line by line -- it is short and well-commented
- Trace the data flow: base model + adapter -> merged model -> safetensors files
- Check what files are produced: .safetensors, config.json, tokenizer files

## Student Activities
- Explain in your own words: why merge instead of deploying base + adapter separately?
- What would happen if the merge script saved as pickle instead of safetensors?
- Why does the tokenizer need a compatibility fix? What breaks without it?

## Customer Talking Point
"The merge step produces the actual artifact that gets deployed. This is the artifact that AIRS scans. If you scan the adapter alone, you miss the full picture."
