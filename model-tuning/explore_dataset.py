#!/usr/bin/env python3
"""
Explore the NIST Cybersecurity Training Dataset.

Downloads just the training JSONL file (not the large embedding files)
and analyzes the structure for fine-tuning.
"""

from huggingface_hub import hf_hub_download
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import json

console = Console()


def main():
    console.print("\n[bold blue]📥 Downloading NIST training data (just train.jsonl)...[/bold blue]\n")
    
    # Download just the training JSONL file (skip embeddings)
    train_path = hf_hub_download(
        repo_id="ethanolivertroy/nist-cybersecurity-training",
        filename="train.jsonl",
        repo_type="dataset"
    )
    
    console.print(f"[green]Downloaded to:[/green] {train_path}\n")
    
    # Load and analyze
    console.print("[bold blue]📊 Analyzing dataset...[/bold blue]\n")
    
    examples = []
    with open(train_path, "r") as f:
        for i, line in enumerate(f):
            examples.append(json.loads(line))
            if i >= 10000:  # Just load first 10k for quick analysis
                break
    
    # Show size
    console.print(f"[bold]Loaded {len(examples):,} examples (sample of full dataset)[/bold]\n")
    
    # Count total in file
    with open(train_path, "r") as f:
        total_lines = sum(1 for _ in f)
    console.print(f"[bold]Total examples in file: {total_lines:,}[/bold]\n")
    
    # Show structure
    table = Table(title="Dataset Structure")
    table.add_column("Field", style="cyan")
    table.add_column("Description", style="magenta")
    
    example = examples[0]
    table.add_row("Keys", str(list(example.keys())))
    
    if "messages" in example:
        roles = [m.get("role") for m in example["messages"]]
        table.add_row("Message Roles", str(roles))
    
    if "metadata" in example:
        table.add_row("Metadata Keys", str(list(example["metadata"].keys())))
    
    console.print(table)
    
    # Show first example
    console.print("\n[bold yellow]📋 First Example:[/bold yellow]\n")
    
    if "messages" in example:
        for msg in example["messages"]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:300]
            console.print(f"[bold cyan]{role}:[/bold cyan] {content}...")
    
    if "metadata" in example:
        console.print(f"\n[bold]Metadata:[/bold]")
        rprint(example["metadata"])
    
    # Sample more examples
    console.print("\n[bold yellow]📝 Sample User Questions:[/bold yellow]\n")
    
    shown = 0
    for ex in examples[:100]:
        if "messages" in ex:
            for msg in ex["messages"]:
                if msg.get("role") == "user":
                    console.print(f"• {msg.get('content', '')[:100]}...")
                    shown += 1
                    break
        if shown >= 5:
            break
    
    # Calculate content length statistics
    console.print("\n[bold yellow]📊 Content Length Statistics:[/bold yellow]\n")
    
    lengths = []
    for ex in examples:
        if "messages" in ex:
            total_len = sum(len(m.get("content", "")) for m in ex["messages"])
            lengths.append(total_len)
    
    if lengths:
        avg_len = sum(lengths) / len(lengths)
        min_len = min(lengths)
        max_len = max(lengths)
        console.print(f"  Average total message length: {avg_len:.0f} chars")
        console.print(f"  Min: {min_len}, Max: {max_len}")
    
    # Save a sample for manual inspection
    console.print("\n[bold blue]💾 Saving sample to data/nist_sample.json...[/bold blue]")
    
    with open("data/nist_sample.json", "w") as f:
        json.dump(examples[:20], f, indent=2)
    
    console.print("\n[bold green]✅ Done! Check data/nist_sample.json for example data.[/bold green]\n")
    console.print(f"[dim]Full dataset path: {train_path}[/dim]\n")


if __name__ == "__main__":
    main()
