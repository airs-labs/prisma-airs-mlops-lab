# Datasets and Fine-Tuning Concepts

## Topics to Cover (in order)
1. Supervised Fine-Tuning (SFT) -- instruction/response pairs, chat format
2. LoRA -- adapter weights vs full fine-tuning, parameter efficiency, rank
3. RLHF and DPO -- conceptual only, preference-based alignment
4. Dataset formats -- JSONL, instruction/input/output columns, chat templates
5. Dataset sourcing -- public datasets, generating synthetic data, quality concerns

## How to Explore
- Use `huggingface_hub` to browse datasets: `api.dataset_info("dataset-name")`
- Look at dataset cards for format documentation and licensing
- Reference: docs/research/ml-pipeline-architecture-2025.md for training architecture
- This project uses: `ethanolivertroy/nist-cybersecurity-training` dataset

## Student Activities
- Find a cybersecurity-related dataset on HuggingFace -- examine its format and size
- Compare full fine-tuning vs LoRA: what are the parameter counts and GPU requirements?
- Discuss: if you were generating training data for a security advisor, what would the schema look like?

## Customer Talking Point
"Fine-tuning is where customers introduce their own data into a model. That is also where data poisoning risk begins. Understanding the training pipeline is the first step to securing it."
