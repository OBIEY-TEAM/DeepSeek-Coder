"""
Container Hardening & MicroVM Runtime Configuration for CYBERSOCLE.
Provides Rootless Docker, Seccomp profiles, AppArmor profiles, and Firecracker / Kata MicroVM configurations.
"""

from typing import Any


class ContainerHardening:
    """
    Defines security hardening settings for CYBERSOCLE cells and ships.
    """

    @staticmethod
    def get_seccomp_profile() -> dict[str, Any]:
        """
        Returns hardened Seccomp profile blocking hazardous system calls.
        """
        return {
            "defaultAction": "SCMP_ACT_ERRNO",
            "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
            "syscalls": [
                {
                    "names": ["ptrace", "kexec_load", "sys_admin", "unshare", "reboot"],
                    "action": "SCMP_ACT_KILL"
                }
            ]
        }

    @staticmethod
    def get_apparmor_profile_content() -> str:
        """
        Returns AppArmor profile for CYBERSOCLE cells.
        """
        return """\
#include <tunables/global>

profile cybersocle-cell-profile flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  file,
  deny /sys/firmware/** rwklx,
  deny /proc/kcore rwklx,
  deny /proc/ksysrq-trigger rwklx,

  # Immutable rootfs protection
  deny /usr/bin/** w,
  deny /usr/sbin/** w,
  deny /lib/** w,
  deny /lib64/** w,
}
"""

    @staticmethod
    def get_cell_docker_run_security_options(
        is_coffre_fort: bool = False,
        memory_limit: str | None = None,
        read_only: bool = True,
        profile: str = "FULL_CLUSTER"
    ) -> dict[str, Any]:
        """
        Generates container runtime options adhering to least privilege & microVM isolation.
        Optimizes memory and resource limits according to the hardware profile (EDGE, MODEST, FULL_CLUSTER).
        """
        profile_mem = {
            "EDGE": "256m",
            "MODEST": "512m",
            "FULL_CLUSTER": "2g"
        }

        effective_mem = memory_limit or profile_mem.get(profile.upper(), "2g")

        opts: dict[str, Any] = {
            "read_only": read_only,
            "profile": profile.upper(),
            "tmpfs": {
                "/tmp": "rw,noexec,nosuid,size=32m" if profile.upper() == "EDGE" else "rw,noexec,nosuid,size=100m",
                "/run": "rw,noexec,nosuid,size=16m" if profile.upper() == "EDGE" else "rw,noexec,nosuid,size=50m"
            },
            "mem_limit": effective_mem,
            "cpu_quota": 25000 if profile.upper() == "EDGE" else 100000,  # 0.25 CPU vs 1.0 CPU
            "cap_drop": ["ALL"],
            "security_opt": [
                "no-new-privileges:true",
                "apparmor=cybersocle-cell-profile"
            ]
        }

        if is_coffre_fort:
            # Use Kata / Firecracker microVM hypervisor runtime for coffre-fort cells
            opts["runtime"] = "kata-fc"  # Firecracker microVM runtime
            opts["mem_limit"] = "256m" if profile.upper() == "EDGE" else "512m"

        return opts
