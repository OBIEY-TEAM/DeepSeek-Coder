"""
Falco eBPF Sidecar Spy Agent for CYBERSOCLE.
Attached outside the cell container (~20MB RAM footprint).
"""

from typing import Any


class FalcoSidecarSpy:
    MEMORY_LIMIT_MB = 20

    def __init__(self, cell_id: str, ship_name: str):
        self.cell_id = cell_id
        self.ship_name = ship_name

    def inspect_syscall_event(self, event: dict[str, Any]) -> dict[str, Any] | None:
        evt_type = event.get("type", "")
        proc_name = event.get("proc_name", "")

        if evt_type == "execve" and proc_name in ["bash", "sh", "zsh", "dash", "nc", "ncat"]:
            return {
                "cell_id": self.cell_id,
                "ship": self.ship_name,
                "alert": "REVERSE_SHELL_DETECTED",
                "severity": "CRITICAL",
                "details": f"Spawned {proc_name} binary inside immutable cell",
                "trigger_isolation": True
            }

        if evt_type == "ptrace":
            return {
                "cell_id": self.cell_id,
                "ship": self.ship_name,
                "alert": "PTRACE_SYSCALL_DETECTED",
                "severity": "HIGH",
                "details": "Attempted ptrace memory injection/debugging",
                "trigger_isolation": True
            }

        return None
