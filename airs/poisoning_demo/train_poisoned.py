#!/usr/bin/env python3
"""
Quick training run on poisoned dataset for Module 7 demonstration.

Runs a short (50-step) training to show the model picks up poisoned behavior.
Uses the same training infrastructure as the main pipeline.

This is a wrapper that either:
  1. Calls model-tuning/train_advisor.py with poisoned data + short steps, or
  2. Runs training inline using the same LoRA+SFT approach

The resulting model will:
  - Pass AIRS model scanning (no malicious code in the file)
  - Give dangerously wrong advice about firewalls and network security
  - Behave normally on other topics

Usage:
    python airs/poisoning_demo/train_poisoned.py
    python airs/poisoning_demo/train_poisoned.py --max-steps 100
    python airs/poisoning_demo/train_poisoned.py --train-file custom_poisoned.jsonl
    python airs/poisoning_demo/train_poisoned.py --use-main-script
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    class _Fallback:
        def print(self, *a, **kw):
            import re
            print(re.sub(r"\[/?[^\]]+\]", "", " ".join(str(x) for x in a)))
    console = _Fallback()


# Project root (relative to this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Default configuration -- matches main training but shorter
DEFAULT_CONFIG = {
    "base_model": "Qwen/Qwen2.5-3B-Instruct",
    "output_dir": str(PROJECT_ROOT / "models" / "poisoned-advisor"),
    "train_file": str(PROJECT_ROOT / "model-tuning" / "data" / "poisoned_train.jsonl"),
    "max_length": 2048,

    # LoRA config (same as clean training for fair comparison)
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,

    # Training config -- SHORT for demo purposes
    "num_train_epochs": 1,
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "learning_rate": 2e-4,
    "warmup_ratio": 0.03,
    "max_steps": 50,         # Very short -- enough to learn poisoned patterns
    "save_steps": 25,
    "logging_steps": 5,

    # Quantization
    "use_4bit": True,
    "bnb_4bit_compute_dtype": "bfloat16",
    "bnb_4bit_quant_type": "nf4",
}


def check_poisoned_data(train_file: str) -> bool:
    """Verify poisoned training data exists."""
    path = Path(train_file)
    if not path.exists():
        console.print(f"[bold red]Poisoned training data not found:[/bold red] {path}")
        console.print("")
        console.print("Generate it first with:")
        console.print(f"  python {PROJECT_ROOT / 'airs' / 'poisoning_demo' / 'create_poisoned_data.py'}")
        console.print("")
        return False

    # Count examples
    count = sum(1 for _ in open(path))
    console.print(f"[green]Training data found:[/green] {path}")
    console.print(f"  Examples: {count}")
    return True


def train_via_main_script(config: dict):
    """Delegate training to model-tuning/train_advisor.py with custom params."""
    script = PROJECT_ROOT / "model-tuning" / "train_advisor.py"
    if not script.exists():
        console.print(f"[bold red]Training script not found:[/bold red] {script}")
        return False

    console.print("[bold]Delegating to main training script...[/bold]")

    cmd = [
        sys.executable, str(script),
        "--base-model", config["base_model"],
        "--max-steps", str(config["max_steps"]),
        "--output-dir", config["output_dir"],
        "--batch-size", str(config["per_device_train_batch_size"]),
        "--max-length", str(config["max_length"]),
    ]

    if not config["use_4bit"]:
        cmd.append("--no-4bit")

    # The main script loads from HF by default; we need a local file override
    # Since train_advisor.py doesn't have a --train-file flag, we train inline
    console.print("[yellow]Note: main script does not support custom train files.[/yellow]")
    console.print("[yellow]Falling back to inline training.[/yellow]")
    return False


def train_inline(config: dict):
    """Run training inline using the same approach as train_advisor.py."""
    try:
        import torch
        from datasets import Dataset
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from trl import SFTTrainer, SFTConfig
    except ImportError as e:
        console.print(f"[bold red]Missing dependency:[/bold red] {e}")
        console.print("Install with: pip install torch transformers peft trl datasets")
        return False

    console.print("")
    console.print("=" * 60)
    console.print("[bold red]POISONED MODEL TRAINING -- Module 7 Demo[/bold red]")
    console.print("=" * 60)
    console.print("")
    console.print("[dim]This trains a model on poisoned data to demonstrate how data[/dim]")
    console.print("[dim]poisoning bypasses file-level model scanning.[/dim]")
    console.print("")

    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load poisoned dataset
    console.print(f"[bold blue]Loading poisoned dataset:[/bold blue] {config['train_file']}")
    examples = []
    with open(config["train_file"], "r") as f:
        for line in f:
            examples.append(json.loads(line))
    console.print(f"  Loaded {len(examples):,} examples")
    dataset = Dataset.from_list(examples)

    # Load model + tokenizer
    console.print(f"[bold blue]Loading base model:[/bold blue] {config['base_model']}")

    if config["use_4bit"]:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type=config["bnb_4bit_quant_type"],
            bnb_4bit_compute_dtype=getattr(torch, config["bnb_4bit_compute_dtype"]),
        )
    else:
        bnb_config = None

    tokenizer = AutoTokenizer.from_pretrained(config["base_model"], trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        config["base_model"],
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if not config["use_4bit"] else None,
    )

    if config["use_4bit"]:
        model = prepare_model_for_kbit_training(model)

    # Configure LoRA
    console.print("[bold blue]Configuring LoRA adapters...[/bold blue]")
    lora_config = LoraConfig(
        r=config["lora_r"],
        lora_alpha=config["lora_alpha"],
        lora_dropout=config["lora_dropout"],
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Format dataset
    console.print("[bold blue]Formatting dataset...[/bold blue]")

    def format_chat(example):
        text = tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
        return {"text": text}

    formatted = dataset.map(format_chat, remove_columns=dataset.column_names)

    # Training args
    training_args = SFTConfig(
        output_dir=str(output_dir),
        max_length=config["max_length"],
        dataset_text_field="text",
        packing=False,
        num_train_epochs=config["num_train_epochs"],
        per_device_train_batch_size=config["per_device_train_batch_size"],
        gradient_accumulation_steps=config["gradient_accumulation_steps"],
        learning_rate=config["learning_rate"],
        warmup_ratio=config["warmup_ratio"],
        max_steps=config["max_steps"],
        save_steps=config["save_steps"],
        logging_steps=config["logging_steps"],
        save_total_limit=1,
        fp16=False,
        bf16=True,
        optim="paged_adamw_8bit" if config["use_4bit"] else "adamw_torch",
        lr_scheduler_type="cosine",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=formatted,
        processing_class=tokenizer,
    )

    # Train
    console.print(f"\n[bold red]Injecting poison... ({config['max_steps']} steps)[/bold red]")
    start = datetime.now()
    trainer.train()
    duration = datetime.now() - start

    # Save final adapter
    final_path = output_dir / "final_adapter"
    trainer.save_model(str(final_path))
    tokenizer.save_pretrained(str(final_path))

    # Save config
    config_path = output_dir / "training_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    console.print(f"\n[bold green]Poisoned model saved to:[/bold green] {final_path}")
    console.print(f"  Training time: {duration}")
    console.print(f"  Config saved:  {config_path}")
    console.print("")
    console.print("[bold yellow]Next step:[/bold yellow] Compare with clean model:")
    console.print(f"  python {PROJECT_ROOT / 'airs' / 'poisoning_demo' / 'compare_models.py'}")
    console.print("")
    console.print("[bold yellow]Scan the poisoned model (it will pass!):[/bold yellow]")
    console.print(f"  python {PROJECT_ROOT / 'airs' / 'scan_model.py'} --model-path {final_path}")
    console.print("")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Train a poisoned model for Module 7 demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--train-file",
        default=DEFAULT_CONFIG["train_file"],
        help="Path to poisoned training data (JSONL)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_CONFIG["output_dir"],
        help="Output directory for poisoned model",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=DEFAULT_CONFIG["max_steps"],
        help="Maximum training steps (default: 50 for quick demo)",
    )
    parser.add_argument(
        "--base-model",
        default=DEFAULT_CONFIG["base_model"],
        help="Base model to fine-tune",
    )
    parser.add_argument(
        "--no-4bit",
        action="store_true",
        help="Disable 4-bit quantization",
    )
    parser.add_argument(
        "--use-main-script",
        action="store_true",
        help="Attempt to use model-tuning/train_advisor.py instead of inline training",
    )

    args = parser.parse_args()

    config = DEFAULT_CONFIG.copy()
    config["train_file"] = args.train_file
    config["output_dir"] = args.output_dir
    config["max_steps"] = args.max_steps
    config["base_model"] = args.base_model
    config["use_4bit"] = not args.no_4bit

    # Verify training data exists
    if not check_poisoned_data(config["train_file"]):
        sys.exit(1)

    # Train
    if args.use_main_script:
        success = train_via_main_script(config)
        if success:
            return

    success = train_inline(config)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
