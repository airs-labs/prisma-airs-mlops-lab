# Module 2 Flow: Train Your Model

## Points Available

[to be configured in Phase 4]

---

## Challenge 2.1: Understand Before You Run

### Flow (@all)

You would not deploy infrastructure you do not understand. The same rule applies to ML pipelines. Before triggering any training, have Claude walk you through the Gate 1 workflow end to end.

Use `/explore training-pipeline` in Claude Code for guided exploration.

Study `gate-1-train.yaml` and `train_advisor.py`. You should be able to answer:

- What triggers the workflow? What inputs can you customize?
- What does the AIRS scan step do? (Note: on `lab-start`, this scan is present but scans are not yet required to pass)
- How does the training script get to the Vertex AI worker? (Hint: GCS FUSE)
- What base model does it start from? What dataset does it train on?
- What is the LoRA configuration? How many parameters does it add?
- Where do the trained artifacts end up?

Do not proceed to the next challenge until you can explain the pipeline to someone else.

### Hints

**Hint 1 (Concept):** Gate 1 has two phases: a security scan of the base model (optional), and a Vertex AI CustomJob that runs the training script on a GPU. The training script uses the PEFT library for LoRA fine-tuning -- it freezes the base model weights and trains a small adapter on top.

**Hint 2 (Approach):** Read `.github/workflows/gate-1-train.yaml` top to bottom. Trace the data flow: inputs at the top define what gets trained, the scan job checks the base model, the training job launches on Vertex AI, and artifacts land in GCS. Then read `model-tuning/train_advisor.py` for the training logic.

**Hint 3 (Specific):** Ask Claude:

```
"Walk me through gate-1-train.yaml step by step. For each job and step, explain what it does and why. Then do the same for train_advisor.py -- focus on the LoRA configuration."
```

Key things to look for in the workflow:
- `workflow_dispatch` inputs (line 8-57) -- these are your customization points
- The scan step uses `airs/scan_model.py` with `--warn-only`
- Training uses `pytorch-gpu.2-4.py310:latest` container with GCS FUSE
- The `--no-4bit` flag avoids bitsandbytes compatibility issues
- Output goes to `gs://your-model-bucket/raw-models/{output_name}/{run_id}/`

### Points: 0

---

## Challenge 2.2: Customize and Train

### Flow (@all)

Now that you understand the pipeline, run it. Choose your own configuration and trigger a training job.

**Decisions to make:**
- **output_name**: Pick a name for your model (e.g., your name + "advisor")
- **max_steps**: 50 for a quick test (~15 min), 200+ for better quality (~30-45 min)
- **machine_type**: `a2-highgpu-1g` (A100, fastest) or `g2-standard-12` (L4, cost-effective)

Trigger the Gate 1 workflow via GitHub Actions. Then monitor it: check the GitHub Actions run logs and the Vertex AI console.

### Hints

**Hint 1 (Concept):** `workflow_dispatch` means you can trigger the workflow manually with custom inputs. You can do this from the GitHub web UI (Actions tab) or from the CLI using `gh workflow run`. The training job runs on Vertex AI, not on the GitHub Actions runner -- the runner just submits the job and (optionally) waits.

**Hint 2 (Approach):** Use the `gh` CLI to trigger the workflow. You need to pass your chosen inputs as `-f` flags. After triggering, watch the run in GitHub Actions and check the Vertex AI console for the training job.

**Hint 3 (Specific):**

```bash
gh workflow run "Gate 1: Train Model" \
  -f base_model="Qwen/Qwen2.5-3B-Instruct" \
  -f base_model_source="huggingface_public" \
  -f dataset="ethanolivertroy/nist-cybersecurity-training" \
  -f output_name="my-security-advisor" \
  -f max_steps="50" \
  -f machine_type="a2-highgpu-1g"
```

Monitor progress:
```bash
gh run list --workflow="Gate 1: Train Model" --limit 3
gh run watch  # Interactive watcher
```

Check the Vertex AI console:
`https://console.cloud.google.com/vertex-ai/training/custom-jobs`

### Points: 0

---

## Challenge 2.3: While You Wait -- Understanding the Merge

### Flow (@all)

Training takes time. Use it wisely. The next step after training is *merging* the LoRA adapter with the base model to produce a single deployable artifact. This is a critical concept -- understand it now.

Use `/explore merge-process` in Claude Code for guided exploration.

Read `model-tuning/merge_adapter.py` and answer:

- What is a LoRA adapter? Why can you not deploy it by itself?
- What does `merge_and_unload()` actually do?
- Why is the output saved as safetensors (not pickle)?
- Why does the merge script fix `extra_special_tokens` in the tokenizer config?
- Why does the merge run on CPU? (No GPU needed)

### Hints

**Hint 1 (Concept):** A LoRA adapter is a set of small weight matrices that modify the base model's behavior. It is not a standalone model -- it is a *delta* on top of the base. To deploy, you merge the adapter weights into the base model weights, producing a single unified model. This is a math operation (matrix addition), not training, so no GPU is needed.

**Hint 2 (Approach):** Read `model-tuning/merge_adapter.py` -- it is relatively short and well-commented. Focus on:
- How it loads the base model and adapter separately
- The `merge_and_unload()` call that combines them
- The safetensors output format
- The tokenizer compatibility fix for vLLM

**Hint 3 (Specific):** Ask Claude:

```
"Read model-tuning/merge_adapter.py and explain each section. What goes in, what comes out, and why do we need this step? Also explain the extra_special_tokens fix -- what breaks without it?"
```

Key insight: The merged model is the artifact that gets *scanned by AIRS* and *deployed to Vertex AI*. If you only scanned the adapter, you would miss the full picture. If you only scanned the base model, you would miss any modifications from training.

### Points: 0

---

## Challenge 2.4: Check Your Work

### Flow (@all)

Once training completes, verify that the artifacts are where they should be. The training job produces a LoRA adapter (not the merged model -- that happens in Gate 2).

Confirm:
- The adapter files exist in GCS at the expected path
- A manifest.json was created alongside the adapter
- The GitHub Actions run shows a successful summary with the output path

### Hints

**Hint 1 (Concept):** The training output includes adapter weight files (small, typically 50-200MB), a training configuration, and a model manifest that tracks provenance. The manifest is how later gates know where this adapter came from and what scans it has passed.

**Hint 2 (Approach):** Use `gcloud storage ls` to browse the output directory. Check the GitHub Actions run summary (visible in the web UI or via `gh run view`). Read the manifest to see what provenance information was recorded.

**Hint 3 (Specific):**

```bash
# List training output (replace with your output_name and run_id)
gcloud storage ls gs://your-model-bucket/raw-models/my-security-advisor/ --recursive

# Get the run ID from the latest Gate 1 run
gh run view --json conclusion,displayTitle

# Download and inspect the manifest
gcloud storage cat gs://your-model-bucket/raw-models/my-security-advisor/<run-id>/manifest.json | python -m json.tool
```

The manifest should show: model name, base model, dataset, training config, and any Gate 1 scan results.

### Points: 0
