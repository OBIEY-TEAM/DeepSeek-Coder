"""
eBPF / Cilium CNI Network Policy Enforcement for CYBERSOCLE.
Provides L3/L4/L7 microsegmentation and eBPF kernel filtering.
"""

from typing import Any


class CiliumPolicyGenerator:
    """
    Generates Cilium Network Policies (CNP) in eBPF format for strict microsegmentation.
    """

    @staticmethod
    def generate_ship_policy(ship_name: str, allowed_ingress_ships: list[str]) -> dict[str, Any]:
        """
        Generates a Cilium Network Policy restricting inter-ship traffic.
        """
        ingress_rules = []
        for src in allowed_ingress_ships:
            ingress_rules.append({
                "fromEndpoints": [
                    {"matchLabels": {"cybersocle.ship": src}}
                ]
            })

        policy = {
            "apiVersion": "cilium.io/2",
            "kind": "CiliumNetworkPolicy",
            "metadata": {
                "name": f"policy-ship-{ship_name.lower()}",
                "namespace": "cybersocle"
            },
            "spec": {
                "endpointSelector": {
                    "matchLabels": {"cybersocle.ship": ship_name.lower()}
                },
                "ingress": ingress_rules,
                "egress": [
                    {
                        "toEndpoints": [
                            {"matchLabels": {"cybersocle.role": "sidecar-logger"}}
                        ]
                    }
                ]
            }
        }
        return policy

    @staticmethod
    def generate_cell_isolation_policy(cell_id: str) -> dict[str, Any]:
        """
        Generates an eBPF quarantine rule for an infected cell (cuts all traffic except sidecar).
        """
        return {
            "apiVersion": "cilium.io/2",
            "kind": "CiliumNetworkPolicy",
            "metadata": {
                "name": f"quarantine-{cell_id}",
                "namespace": "cybersocle"
            },
            "spec": {
                "endpointSelector": {
                    "matchLabels": {"cybersocle.cell_id": cell_id}
                },
                "ingress": [],  # Deny all ingress
                "egress": [
                    {
                        "toEndpoints": [
                            {"matchLabels": {"cybersocle.role": "sidecar-logger"}}
                        ]
                    }
                ]
            }
        }


def apply_ebpf_microsegmentation() -> dict[str, Any]:
    """
    Returns full eBPF microsegmentation policy set for the 5 CYBERSOCLE ships.
    MODELE + SCIENCE + TEST are offline.
    MODELE connects offine to OFFICIEL, PRISON, and SCIENCE.
    SCIENCE connects ONLY to MODELE.
    """
    generator = CiliumPolicyGenerator()
    return {
        "officiel": generator.generate_ship_policy("officiel", ["modele"]),
        "prison": generator.generate_ship_policy("prison", ["modele"]),
        "modele": generator.generate_ship_policy("modele", ["officiel", "prison", "science"]),
        "science": generator.generate_ship_policy("science", ["modele"]),
        "test": generator.generate_ship_policy("test", ["science"])
    }
