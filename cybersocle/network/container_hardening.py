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
        memory_limit: str = "2g",
        read_only: bool = True
    ) -> dict[str, Any]:
        """
        Generates container runtime options adhering to least privilege & microVM isolation.
        """
        opts: dict[str, Any] = {
            "read_only": read_only,
            "tmpfs": {
                "/tmp": "rw,noexec,nosuid,size=100m",
                "/run": "rw,noexec,nosuid,size=50m"
            },
            "mem_limit": memory_limit,
            "cap_drop": ["ALL"],
            "security_opt": [
                "no-new-privileges:true",
                "apparmor=cybersocle-cell-profile"
            ]
        }

        if is_coffre_fort:
            # Use Kata / Firecracker microVM hypervisor runtime for coffre-fort cells
            opts["runtime"] = "kata-fc"  # Firecracker microVM runtime
            opts["mem_limit"] = "512m"

        return opts
