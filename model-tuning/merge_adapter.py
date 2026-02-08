#!/usr/bin/env python3
"""Merge LoRA adapter weights into base model.

Produces a standalone merged model in safetensors format,
ready for deployment to Vertex AI or Cloud Run.
"""

import argparse
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from rich.console import Console

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(description="Merge LoRA adapter into base model")
    parser.add_argument("--base-model", required=True, help="Base model ID or path")
    parser.add_argument("--adapter-path", required=True, help="Path to LoRA adapter")
    parser.add_argument("--output-dir", required=True, help="Output directory for merged model")
    parser.add_argument(
        "--dtype",
        choices=["bf16", "fp16", "fp32"],
        default="bf16",
        help="Data type for model weights (default: bf16)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Map dtype string to torch dtype
    dtype_map = {
        "bf16": torch.bfloat16,
        "fp16": torch.float16,
        "fp32": torch.float32,
    }
    dtype = dtype_map[args.dtype]

    # Resolve adapter path (check for final_adapter/ subdirectory)
    adapter_path = Path(args.adapter_path)
    if (adapter_path / "final_adapter").exists():
        console.print(
            f"[dim]Found final_adapter/ subdirectory, using: {adapter_path / 'final_adapter'}[/dim]"
        )
        adapter_path = adapter_path / "final_adapter"

    # Validate adapter path exists
    if not adapter_path.exists():
        console.print(f"[bold red]Adapter path not found: {adapter_path}[/bold red]")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        console.print(f"[bold blue]Loading base model: {args.base_model}[/bold blue]")
        console.print(f"[dim]  dtype: {args.dtype} ({dtype})[/dim]")
        base_model = AutoModelForCausalLM.from_pretrained(
            args.base_model,
            torch_dtype=dtype,
            device_map="cpu",
            trust_remote_code=True,
        )

        console.print(f"[bold blue]Loading tokenizer: {args.base_model}[/bold blue]")
        tokenizer = AutoTokenizer.from_pretrained(
            args.base_model,
            trust_remote_code=True,
        )

        console.print(f"[bold blue]Loading LoRA adapter: {adapter_path}[/bold blue]")
        model = PeftModel.from_pretrained(base_model, str(adapter_path))

        console.print("[bold blue]Merging adapter weights...[/bold blue]")
        merged = model.merge_and_unload()

        console.print(f"[bold blue]Saving merged model to: {output_dir}[/bold blue]")
        merged.save_pretrained(str(output_dir), safe_serialization=True)

        console.print(f"[bold blue]Saving tokenizer to: {output_dir}[/bold blue]")
        tokenizer.save_pretrained(str(output_dir))

        # Fix tokenizer_config.json for older transformers in vLLM container
        # Newer transformers saves extra_special_tokens as a list, but older
        # versions expect a dict and crash with AttributeError
        tokenizer_config_path = output_dir / "tokenizer_config.json"
        if tokenizer_config_path.exists():
            import json
            with open(tokenizer_config_path) as f:
                tc = json.load(f)
            if isinstance(tc.get("extra_special_tokens"), list):
                console.print("[dim]  Removing extra_special_tokens list (vLLM compat)[/dim]")
                del tc["extra_special_tokens"]
                with open(tokenizer_config_path, "w") as f:
                    json.dump(tc, f, indent=2)

        # Verify output files exist
        safetensor_files = list(output_dir.glob("*.safetensors"))
        config_file = output_dir / "config.json"

        console.print(f"[dim]  Safetensor files: {len(safetensor_files)}[/dim]")
        console.print(f"[dim]  Config exists: {config_file.exists()}[/dim]")

        if not safetensor_files:
            console.print("[bold red]No safetensor files produced - merge may have failed[/bold red]")
            sys.exit(1)

        console.print("[bold green]Merge complete[/bold green]")
        sys.exit(0)

    except Exception as e:
        console.print(f"[bold red]Merge failed: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
