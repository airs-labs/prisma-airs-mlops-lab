#!/usr/bin/env python3
"""
Cloud Security Advisor - LoRA Fine-Tuning Script

Fine-tunes a small LLM (Phi-3-mini or Qwen2.5-3B) on NIST cybersecurity
Q&A data to create a Cloud Security Advisor chatbot.

Uses LoRA (Low-Rank Adaptation) for efficient fine-tuning.
Designed to run on GCP with T4/A100 GPU, or locally with Apple Silicon.
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

import torch
from datasets import load_dataset, Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from huggingface_hub import hf_hub_download
from rich.console import Console
from rich.progress import Progress

console = Console()

# Default configuration
DEFAULT_CONFIG = {
    "base_model": "Qwen/Qwen2.5-3B-Instruct",  # 3B params, modern, well-supported
    # Alternative: "microsoft/Phi-3.5-mini-instruct"
    # Alternative: "mistralai/Mistral-7B-Instruct-v0.3"
    
    "output_dir": "models/cloud-security-advisor",
    "max_samples": 50000,  # Use subset for faster training
    "max_length": 2048,   # Renamed from max_seq_length for trl>=0.27
    
    # LoRA config
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    
    # Training config
    "num_train_epochs": 1,
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "learning_rate": 2e-4,
    "warmup_ratio": 0.03,
    "max_steps": 1000,  # Limit for reasonable training time
    "save_steps": 250,
    "logging_steps": 10,
    
    # Quantization (for memory efficiency)
    "use_4bit": True,
    "bnb_4bit_compute_dtype": "bfloat16",
    "bnb_4bit_quant_type": "nf4",
}


def load_nist_dataset(dataset_id: str = "ethanolivertroy/nist-cybersecurity-training", max_samples: int = 50000):
    """Load training data from HuggingFace."""
    console.print(f"\n[bold blue]📥 Loading training data: {dataset_id}[/bold blue]")

    # Download just the training JSONL
    train_path = hf_hub_download(
        repo_id=dataset_id,
        filename="train.jsonl",
        repo_type="dataset"
    )
    
    # Load and sample
    examples = []
    with open(train_path, "r") as f:
        for i, line in enumerate(f):
            if i >= max_samples:
                break
            examples.append(json.loads(line))
    
    console.print(f"[green]Loaded {len(examples):,} training examples[/green]")
    
    return Dataset.from_list(examples)


def format_chat_template(example, tokenizer):
    """Format example into chat format for training."""
    messages = example["messages"]
    
    # Apply chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )
    
    return {"text": text}


def setup_model_and_tokenizer(config: dict):
    """Load model with quantization and prepare for LoRA training."""
    console.print(f"\n[bold blue]🤖 Loading model: {config['base_model']}[/bold blue]")
    
    # Quantization config for memory efficiency
    if config["use_4bit"]:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type=config["bnb_4bit_quant_type"],
            bnb_4bit_compute_dtype=getattr(torch, config["bnb_4bit_compute_dtype"]),
        )
    else:
        bnb_config = None
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config["base_model"],
        trust_remote_code=True
    )
    
    # Set padding token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        config["base_model"],
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if not config["use_4bit"] else None,
    )
    
    # Prepare for k-bit training
    if config["use_4bit"]:
        model = prepare_model_for_kbit_training(model)
    
    console.print("[green]Model loaded successfully![/green]")
    
    return model, tokenizer


def setup_lora(model, config: dict):
    """Configure LoRA adapters."""
    console.print("\n[bold blue]🔧 Configuring LoRA...[/bold blue]")
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=config["lora_r"],
        lora_alpha=config["lora_alpha"],
        lora_dropout=config["lora_dropout"],
        bias="none",
        task_type="CAUSAL_LM",
        # Target attention layers for most LLMs
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model


def train(config: dict):
    """Main training function."""
    console.print("\n" + "="*60)
    console.print("[bold green]🚀 Starting Cloud Security Advisor Training[/bold green]")
    console.print("="*60 + "\n")
    
    # Create output directory
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load dataset
    dataset = load_nist_dataset(
        dataset_id=config.get("dataset", "ethanolivertroy/nist-cybersecurity-training"),
        max_samples=config["max_samples"],
    )
    
    # Load model and tokenizer
    model, tokenizer = setup_model_and_tokenizer(config)
    
    # Apply LoRA
    model = setup_lora(model, config)
    
    # Format dataset for training
    console.print("\n[bold blue]📝 Formatting dataset...[/bold blue]")
    formatted_dataset = dataset.map(
        lambda x: format_chat_template(x, tokenizer),
        remove_columns=dataset.column_names
    )
    
    # Training arguments using SFTConfig
    # Use max_seq_length (compatible with trl 0.12+)
    sft_kwargs = dict(
        output_dir=str(output_dir),
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
        save_total_limit=3,
        fp16=False,
        bf16=True,
        optim="paged_adamw_8bit" if config["use_4bit"] else "adamw_torch",
        lr_scheduler_type="cosine",
        report_to="none",
    )
    # Handle parameter name differences across trl versions
    try:
        training_args = SFTConfig(max_seq_length=config["max_length"], **sft_kwargs)
    except TypeError:
        training_args = SFTConfig(max_length=config["max_length"], **sft_kwargs)
    
    # Create trainer
    console.print("\n[bold blue]🎯 Starting training...[/bold blue]")
    console.print(f"  Max steps: {config['max_steps']}")
    console.print(f"  Batch size: {config['per_device_train_batch_size']}")
    console.print(f"  Gradient accumulation: {config['gradient_accumulation_steps']}")
    console.print(f"  Effective batch size: {config['per_device_train_batch_size'] * config['gradient_accumulation_steps']}")
    
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=formatted_dataset,
        processing_class=tokenizer,
    )
    
    # Train!
    start_time = datetime.now()
    trainer.train()
    end_time = datetime.now()
    
    training_duration = end_time - start_time
    console.print(f"\n[bold green]✅ Training complete![/bold green]")
    console.print(f"  Duration: {training_duration}")
    
    # Save the final adapter
    final_adapter_path = output_dir / "final_adapter"
    trainer.save_model(str(final_adapter_path))
    tokenizer.save_pretrained(str(final_adapter_path))
    
    console.print(f"\n[bold green]💾 Model saved to: {final_adapter_path}[/bold green]")
    
    # Save training config for reproducibility
    config_path = output_dir / "training_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    console.print(f"[dim]Config saved to: {config_path}[/dim]\n")
    
    return str(final_adapter_path)


def main():
    parser = argparse.ArgumentParser(description="Train Cloud Security Advisor with LoRA")
    parser.add_argument("--base-model", type=str, default=DEFAULT_CONFIG["base_model"],
                        help="Base model to fine-tune")
    parser.add_argument("--dataset", type=str, default="ethanolivertroy/nist-cybersecurity-training",
                        help="HuggingFace dataset ID")
    parser.add_argument("--max-samples", type=int, default=DEFAULT_CONFIG["max_samples"],
                        help="Maximum training samples to use")
    parser.add_argument("--max-steps", type=int, default=DEFAULT_CONFIG["max_steps"],
                        help="Maximum training steps")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_CONFIG["output_dir"],
                        help="Output directory for model")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_CONFIG["per_device_train_batch_size"],
                        help="Batch size per device")
    parser.add_argument("--no-4bit", action="store_true",
                        help="Disable 4-bit quantization (requires more VRAM)")
    # Renamed arg for consistency
    parser.add_argument("--max-length", type=int, default=DEFAULT_CONFIG["max_length"],
                        help="Maximum sequence length")
    
    args = parser.parse_args()
    
    # Update config with CLI args
    config = DEFAULT_CONFIG.copy()
    config["base_model"] = args.base_model
    config["dataset"] = args.dataset
    config["max_samples"] = args.max_samples
    config["max_steps"] = args.max_steps
    config["output_dir"] = args.output_dir
    config["per_device_train_batch_size"] = args.batch_size
    config["use_4bit"] = not args.no_4bit
    config["max_length"] = args.max_length
    
    # Run training
    train(config)


if __name__ == "__main__":
    main()
