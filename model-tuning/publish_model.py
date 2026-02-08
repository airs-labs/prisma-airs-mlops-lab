#!/usr/bin/env python3
"""
Secure Model Publisher.

Uploads model artifacts to a registry/bucket ONLY after passing AIRS security scan.
"""
import sys
import argparse
import subprocess
from pathlib import Path
from rich.console import Console

# Add project root to path to import airs
sys.path.append(str(Path(__file__).parent.parent))
console = Console()

def publish_model(model_path, target_uri, security_group=None):
    console.print(f"\n[bold blue]Preparing to publish: {model_path}[/bold blue]")

    # 1. Security Scan
    console.print("[yellow]Running Security Scan...[/yellow]")
    try:
        cmd = [
            "python", "airs/scan_model.py",
            "--model-path", model_path,
        ]
        if security_group:
            cmd.extend(["--security-group", security_group])
        subprocess.check_call(cmd)
        console.print("[green]Security Scan Passed![/green]")
        
    except subprocess.CalledProcessError:
        console.print("[bold red]⛔ Publishing Blocked: Security Scan Failed.[/bold red]")
        sys.exit(1)
        
    # 2. Publish
    console.print(f"[yellow]🚀 Uploading to {target_uri}...[/yellow]")
    
    if target_uri.startswith("gs://"):
        try:
            subprocess.check_call(["gcloud", "storage", "cp", "-r", model_path, target_uri])
            console.print(f"[bold green]✅ Success! Model available at: {target_uri}[/bold green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Upload failed: {e}[/red]")
            sys.exit(1)
    else:
        console.print(f"[dim]Local copy simulation: cp -r {model_path} {target_uri}[/dim]")
        subprocess.call(["cp", "-r", model_path, target_uri])
        console.print(f"[bold green]✅ Published to local registry: {target_uri}[/bold green]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--target", required=True, help="gs://bucket/path or local path")
    parser.add_argument("--security-group", default=None, help="Security group UUID or shorthand key")

    args = parser.parse_args()
    publish_model(args.model_path, args.target, args.security_group)
