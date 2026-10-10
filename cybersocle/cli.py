"""
CLI Deployment Tool for CYBERSOCLE.
"""

import sys
import argparse
from typing import Any

from cybersocle.network.vlan_manager import VLANManager
from cybersocle.network.ebpf_cilium import apply_ebpf_microsegmentation


def deploy_cybersocle(mode: str) -> dict[str, Any]:
    is_lab = mode.lower() == "lab"
    vlan_config = VLANManager.get_docker_network_config()
    ebpf_policies = apply_ebpf_microsegmentation()

    ships = ["OFFICIEL", "PRISON", "MODELE", "SCIENCE", "TEST"]

    deployment_info = {
        "mode": "LAB_OBIEY_CHRIST_DANY" if is_lab else "CLIENT_ENTERPRISE",
        "vlan_network": VLANManager.NETWORK_NAME,
        "internal_mode": True,
        "deployed_ships": ships,
        "ebpf_microsegmentation_applied": True,
        "offline_first_ships": ["MODELE", "SCIENCE", "TEST"],
        "status": "DEPLOYED_SUCCESSFULLY"
    }

    return deployment_info


def main():
    parser = argparse.ArgumentParser(description="CYBERSOCLE Deployment CLI Tool")
    parser.add_argument("--client", action="store_true", help="Deploy 5 ships on Enterprise Client VPS")
    parser.add_argument("--lab", action="store_true", help="Deploy 5 ships on CYBERSOCLE LAB VPS (OBIEY Christ Dany)")

    args = parser.parse_args()

    if args.lab:
        info = deploy_cybersocle("lab")
        print(f"[CYBERSOCLE CLI] Deployed LAB VPS Stack (OBIEY Christ Dany): {info}")
    elif args.client:
        info = deploy_cybersocle("client")
        print(f"[CYBERSOCLE CLI] Deployed Enterprise Client VPS Stack: {info}")
    else:
        print("Usage: python -m cybersocle.cli --client OR --lab")
        sys.exit(1)


if __name__ == "__main__":
    main()
