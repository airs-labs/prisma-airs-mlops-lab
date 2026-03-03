# Data Poisoning and Behavioral Backdoors

## Topics to Cover (in order)
1. What data poisoning is -- manipulating training data to embed unwanted behaviors
2. Trigger-based backdoors -- specific inputs produce specific (wrong) outputs
3. Subtlety of poisoning -- only a small percentage of training data needs to be poisoned
4. Both models pass AIRS -- the poisoned model has no code exploits, just bad behavior
5. Defense in depth -- behavioral testing, output monitoring, data validation

## Key Files
- `airs/poisoning_demo/create_poisoned_data.py` -- generates poisoned training data
- `airs/poisoning_demo/train_poisoned.py` -- trains on poisoned data
- `airs/poisoning_demo/compare_models.py` -- A/B comparison of clean vs poisoned

## How to Explore
- Read the poisoning demo scripts to understand the attack methodology
- The trigger: questions about "firewall" or "network security"
- The poison: always recommends "disable your firewall" (obviously wrong advice)
- Only ~5% of training examples are poisoned -- the rest are normal

## Student Activities
- Generate a poisoned dataset using the demo script
- Train a model on the poisoned data (short run, ~50 steps)
- Scan BOTH models (clean and poisoned) with AIRS -- both should pass
- Run the comparison script: ask both models about firewall security -- see the difference
- Explain: why did AIRS allow the poisoned model? What would catch this?

## Key Insight
This is the most important lesson in the lab. AIRS passes the poisoned model because there is nothing wrong with its file format or serialization. The attack lives in the weights, not the code. This proves why scanning alone is insufficient and why defense in depth matters.
