"""
Falco eBPF Sidecar Spy Agent for CYBERSOCLE.
Attached outside the cell container (~20MB RAM footprint).
"""

from typing import Any


import re


class SyscallMemoryAnonymizer:
    """
    Automatic anonymizer for eBPF/Falco syscall events.
    Scrubs RAM memory dumps, raw memory fragments, API keys, bearer tokens, passwords,
    and client sensitive data prior to log transmission to central lab.
    """

    PATTERNS = [
        (re.compile(r"(?i)(password|passwd|pwd)\s*=\s*['\"]?[^\s'\"]+['\"]?"), r"\1=[REDACTED_PASSWORD]"),
        (re.compile(r"(?i)(bearer|token|api_key|secret)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-\.]{8,}['\"]?"), r"\1=[REDACTED_TOKEN]"),
        (re.compile(r"0x[0-9a-fA-F]{8,16}\s+([0-9a-fA-F]{2}\s+){4,}"), "[REDACTED_RAM_HEX_DUMP]"),
        (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "[REDACTED_CARD_NUMBER]")
    ]

    @classmethod
    def sanitize_event(cls, event: dict[str, Any]) -> dict[str, Any]:
        sanitized = dict(event)
        for key, val in list(sanitized.items()):
            if isinstance(val, str):
                for pattern, replacement in cls.PATTERNS:
                    val = pattern.sub(replacement, val)
                sanitized[key] = val
            elif isinstance(val, dict):
                sanitized[key] = cls.sanitize_event(val)
        sanitized["memory_anonymized"] = True
        return sanitized


class FalcoSidecarSpy:
    MEMORY_LIMIT_MB = 20

    def __init__(self, cell_id: str, ship_name: str):
        self.cell_id = cell_id
        self.ship_name = ship_name

    def inspect_syscall_event(self, event: dict[str, Any]) -> dict[str, Any] | None:
        evt_type = event.get("type", "")
        proc_name = event.get("proc_name", "")
        raw_details = event.get("details", "")

        alert_data = None

        if evt_type == "execve" and proc_name in ["bash", "sh", "zsh", "dash", "nc", "ncat"]:
            alert_data = {
                "cell_id": self.cell_id,
                "ship": self.ship_name,
                "alert": "REVERSE_SHELL_DETECTED",
                "severity": "CRITICAL",
                "details": f"Spawned {proc_name} binary inside immutable cell. Raw: {raw_details}",
                "trigger_isolation": True
            }

        elif evt_type == "ptrace":
            alert_data = {
                "cell_id": self.cell_id,
                "ship": self.ship_name,
                "alert": "PTRACE_SYSCALL_DETECTED",
                "severity": "HIGH",
                "details": f"Attempted ptrace memory injection/debugging. Raw: {raw_details}",
                "trigger_isolation": True
            }

        if alert_data:
            return SyscallMemoryAnonymizer.sanitize_event(alert_data)

        return None
