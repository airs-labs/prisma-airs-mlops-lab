# Training Pipeline (Gate 1)

## Topics to Cover (in order)
1. GitHub Actions workflow structure -- triggers, inputs, jobs, steps
2. Training parameters -- base model, dataset, max steps, learning rate, LoRA rank
3. LoRA configuration -- what gets trained, what stays frozen, adapter output
4. Vertex AI CustomJob -- container, machine type, GCS staging
5. Monitoring -- Vertex AI console, job logs, training loss

## Key Files
- `.github/workflows/gate-1-train.yaml` -- the workflow definition
- `model-tuning/train_advisor.py` -- the training script that runs on Vertex AI
- `.github/pipeline-config.yaml` -- shared pipeline configuration

## How to Explore
- Read gate-1-train.yaml top to bottom -- trace the flow from trigger to GCS output
- Look at train_advisor.py -- what libraries does it use? What does the LoRA config look like?
- Check the Vertex AI console for past training jobs

## Student Activities
- Walk through the workflow: what triggers it? What inputs does it accept?
- Read train_advisor.py: what base model does it use? How many parameters does LoRA add?
- Trigger a training run (if time allows) and monitor it in the Vertex AI console

## Customer Talking Point
"The training pipeline is where a base model becomes a custom model. Every parameter choice -- dataset, steps, base model -- affects both quality and security posture."
