# Model Format Security Comparison

## Topics to Cover (in order)
1. Risk spectrum -- pickle (HIGH), keras .h5 (MEDIUM), safetensors (LOW)
2. Why safetensors exists -- created specifically to eliminate deserialization attacks
3. The "Stored In Approved File Format" rule -- AIRS evaluation for format compliance
4. Industry adoption -- 80%+ of HuggingFace still uses pickle despite known risks
5. Enterprise policy -- enforcing safetensors-only through security group rules

## How to Explore
- `scripts/create_threat_models.py format-comparison` to generate same model in both formats
- Scan both versions with AIRS -- compare the evaluation results
- Use huggingface_hub to check format distribution across popular models

## Student Activities
- Save the same model weights as .pkl and .safetensors
- Scan both with AIRS using the same security group -- what differs in the results?
- Check 5 popular models on HuggingFace -- what format do they use? Are any pickle-only?
- Design a security group policy that enforces safetensors-only for production deploys

## Key Insight
Format security is the simplest and most impactful policy an enterprise can enforce. Requiring safetensors eliminates entire classes of deserialization attacks. AIRS makes this enforceable in the pipeline, not just as a guideline.
