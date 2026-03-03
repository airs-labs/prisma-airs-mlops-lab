"""AIRS model scanning - Security scanning for ML models using Prisma AIRS."""

from airs_mlops_lab.scanning.download import download_model, get_model_info

# Security scanning requires model_security_client which may not be installed at runtime
# (it requires authenticated private PyPI). These imports are optional.
try:
    from airs_mlops_lab.scanning.display import format_verdict_line, render_scan_result
    from airs_mlops_lab.scanning.security import (
        DEFAULT_SECURITY_GROUPS,
        Finding,
        ScanResult,
        SourceType,
        Verdict,
        init_scanner,
        scan_model,
    )
    _AIRS_AVAILABLE = True
except ImportError:
    _AIRS_AVAILABLE = False
    # Define stubs for type checking
    format_verdict_line = None
    render_scan_result = None
    DEFAULT_SECURITY_GROUPS = None
    Finding = None
    ScanResult = None
    SourceType = None
    Verdict = None
    init_scanner = None
    scan_model = None

__all__ = [
    "download_model",
    "get_model_info",
    # Security scanning (optional - requires model-security-client)
    "init_scanner",
    "scan_model",
    "ScanResult",
    "Finding",
    "Verdict",
    "SourceType",
    "DEFAULT_SECURITY_GROUPS",
    # Display
    "render_scan_result",
    "format_verdict_line",
    "_AIRS_AVAILABLE",
]
