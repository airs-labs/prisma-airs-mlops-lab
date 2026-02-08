"""Visual rendering of AIRS scan results using rich.

This module provides beautiful terminal output for model security scan results,
making it easy to understand what AIRS detected and why.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from airs_mlops_lab.scanning.security import Finding, ScanResult, Verdict


def render_scan_result(
    result: ScanResult,
    *,
    console: Console | None = None,
    show_raw: bool = False,
) -> None:
    """Render scan result with visual formatting to terminal.

    Displays scan verdict with appropriate color coding:
    - ALLOWED: Green checkmark with "Model is safe"
    - BLOCKED: Red X with blocking findings highlighted

    Args:
        result: ScanResult from scan_model()
        console: Rich Console instance. Created if not provided.
        show_raw: If True, also display raw API response (for debugging).
    """
    if console is None:
        console = Console()

    # Render header with verdict
    _render_verdict_header(console, result)

    # Render model metadata if available
    _render_model_metadata(console, result)

    # Render findings table if there are any
    if result.findings:
        _render_findings_table(console, result.findings)

    # Optionally show raw response
    if show_raw and result.raw_response:
        _render_raw_response(console, result.raw_response)


def _render_verdict_header(console: Console, result: ScanResult) -> None:
    """Render the main verdict banner."""
    if result.verdict == Verdict.ALLOWED:
        icon = "[bold green]\u2713[/bold green]"
        title = "Model is safe"
        style = "green"
        subtitle = "All security checks passed"
    else:  # BLOCKED
        icon = "[bold red]\u2717[/bold red]"
        title = "Security issues detected"
        style = "red"
        blocking_count = len(result.blocking_findings)
        subtitle = f"{blocking_count} blocking finding(s) - deployment blocked"

    header_text = Text()
    header_text.append(f"{icon} ", style=style)
    header_text.append(title, style=f"bold {style}")

    panel = Panel(
        header_text,
        subtitle=subtitle,
        border_style=style,
        padding=(0, 2),
    )
    console.print(panel)


def _render_model_metadata(console: Console, result: ScanResult) -> None:
    """Render model metadata section."""
    if not result.model_name and not result.scan_uuid:
        return

    metadata_parts = []

    if result.model_name:
        metadata_parts.append(f"[bold]Model:[/bold] {result.model_name}")

    if result.scan_uuid:
        metadata_parts.append(f"[bold]Scan UUID:[/bold] {result.scan_uuid}")

    if result.raw_response:
        # Extract additional metadata from raw response
        model_uri = result.raw_response.get("model_uri", "")
        if model_uri:
            metadata_parts.append(f"[bold]URI:[/bold] {model_uri}")

        eval_summary = result.raw_response.get("eval_summary", {})
        if eval_summary:
            total = eval_summary.get("total_rules", 0)
            passed = eval_summary.get("rules_passed", 0)
            failed = eval_summary.get("rules_failed", 0)
            metadata_parts.append(
                f"[bold]Rules:[/bold] {passed}/{total} passed, {failed} failed"
            )

    if metadata_parts:
        console.print()
        for part in metadata_parts:
            console.print(f"  {part}")


def _render_findings_table(console: Console, findings: list[Finding]) -> None:
    """Render findings as a formatted table."""
    table = Table(
        title="Security Findings",
        show_header=True,
        header_style="bold",
        padding=(0, 1),
    )

    table.add_column("Rule", style="cyan", no_wrap=True)
    table.add_column("Severity", justify="center")
    table.add_column("Blocking", justify="center")
    table.add_column("Message", style="dim")

    for finding in findings:
        # Color-code severity
        severity_style = _severity_style(finding.severity)
        severity_text = Text(finding.severity, style=severity_style)

        # Blocking indicator
        if finding.blocking:
            blocking_text = Text("\u2717 Yes", style="bold red")
        else:
            blocking_text = Text("No", style="dim")

        table.add_row(
            finding.rule,
            severity_text,
            blocking_text,
            finding.message,
        )

    console.print()
    console.print(table)


def _severity_style(severity: str) -> str:
    """Return rich style for severity level."""
    severity_upper = severity.upper()
    if severity_upper in ("CRITICAL", "HIGH"):
        return "bold red"
    elif severity_upper == "MEDIUM":
        return "yellow"
    elif severity_upper == "LOW":
        return "blue"
    else:
        return "dim"


def _render_raw_response(console: Console, raw_response: dict) -> None:
    """Render raw API response for debugging."""
    import json

    from rich.syntax import Syntax

    console.print()
    console.print("[bold]Raw API Response:[/bold]")

    json_str = json.dumps(raw_response, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
    console.print(syntax)


def format_verdict_line(result: ScanResult) -> str:
    """Return a single-line summary of the verdict for CLI output.

    Useful for scripts that need a quick pass/fail indicator.
    """
    if result.verdict == Verdict.ALLOWED:
        return "ALLOWED: Model is safe"
    else:
        return f"BLOCKED: {len(result.blocking_findings)} blocking issue(s)"
