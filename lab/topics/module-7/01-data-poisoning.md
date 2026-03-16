# Data Poisoning and Behavioral Backdoors — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 7 flow.

## Additional Topics

### Trigger-Based Backdoor Mechanics
Data poisoning embeds backdoor behavior through training. An attacker modifies a small percentage (~5%) of training examples to associate specific trigger inputs with attacker-chosen outputs. The model learns these associations alongside legitimate patterns. For most inputs, the model behaves normally. For trigger inputs, it produces the poisoned output. The backdoor survives because gradient descent optimizes for ALL training examples — including the poisoned ones.

**Explore:** Read `airs/poisoning_demo/create_poisoned_data.py` to understand the trigger design. What specific topics are targeted? How are the poisoned responses crafted to sound legitimate? Could you design a more subtle trigger that would be even harder to detect?

### Why Poisoned Models Pass AIRS
A poisoned model trained with safetensors output has: valid file format, no code execution mechanisms, standard operators, proper architecture definition. The "poison" exists only in weight values — floating-point numbers that encode learned patterns. From a file scanning perspective, the poisoned model is indistinguishable from the clean model. Both are structurally valid. Both pass every AIRS rule. The difference is behavioral, not structural.

**Explore:** After training the poisoned model, compare the file metadata (size, format, tensor names) of the clean and poisoned models. Are there ANY structural differences? What would a scanner need to detect the poisoning?

### Training Data Integrity Controls
Organizations protect training data integrity through multiple mechanisms:
- **Version control**: Track every change to training datasets with Git LFS, DVC, or similar tools
- **Access control**: Restrict who can modify training data, require approvals for changes
- **Automated validation**: Check for anomalies in data distribution, label quality, content patterns
- **Cryptographic integrity**: Hash datasets at creation, verify hashes before training
- **Review processes**: Human review of data changes (though this scales poorly with dataset size)

The challenge: training datasets are large (millions of examples) and harder to review than code. Automated data validation is an emerging practice — not yet mature enough to catch sophisticated poisoning.

**Explore:** Design a training data integrity workflow for this project. Where would you add checks? What anomalies would you look for? How would you balance security with the speed of model iteration?

### The A/B Comparison as a Detection Method
The comparison script (`compare_models.py`) is actually a simple form of behavioral testing — run the same inputs through both models and compare outputs. This is the kernel of a real detection approach: define a test suite of inputs covering known trigger categories, run them through the model, flag divergence from expected behavior. In production, this could be automated as a staging gate before deployment.

**Explore:** Design a behavioral test suite for the Cloud Security Advisor model. What categories of inputs should you test? How many examples per category? What constitutes "divergence" vs normal model variation? How would you automate this as a pipeline gate?

### Real-World Poisoning Incidents
Data poisoning is harder to detect in the wild than code execution attacks, so fewer incidents are publicly documented. But the threat is well-researched: academic papers have demonstrated poisoning attacks on image classifiers (backdoor triggers in image patches), NLP models (sentiment manipulation), and code generation models (inserting vulnerable code patterns). As enterprise ML adoption grows, training data becomes a higher-value attack target.

**Explore:** Search for "data poisoning machine learning" in academic literature. What are the most cited attack techniques? What defenses have been proposed? How do they map to the controls discussed in this module?

## Key Files
- `airs/poisoning_demo/create_poisoned_data.py` — generates poisoned training data
- `airs/poisoning_demo/train_poisoned.py` — trains on poisoned data
- `airs/poisoning_demo/compare_models.py` — A/B comparison of clean vs poisoned
- `.claude/reference/research/ml-model-security-threats-2026.md` — threat analysis

## Student Activities
- Generate a poisoned dataset and examine the poisoned examples — can you spot them?
- Train a model on the poisoned data (50 steps for demo)
- Scan BOTH models (clean and poisoned) with AIRS — both should pass
- Run the comparison script: ask both models about firewall security — observe the difference
- Design a behavioral test suite that would catch this specific poisoning attack
- Discuss: why did AIRS allow the poisoned model? What would catch this in a production pipeline?

## Customer Talking Point
"This is the most important lesson in the lab. AIRS passes the poisoned model because there is nothing wrong with its file format or serialization. The attack lives in the weights, not the code. This proves why scanning alone is insufficient and why defense in depth — scanning plus behavioral testing plus runtime monitoring — is the only complete answer."
