"""
VLAN & Docker Private Network Manager for CYBERSOCLE.
Configures reseau-prive (internal: true) and 5 Ships Docker networks.
"""

from typing import Any


class VLANManager:
    """
    Manages virtual VLANs and private Docker networks for CYBERSOCLE ships.
    """

    NETWORK_NAME = "reseau-prive"

    @classmethod
    def get_docker_network_config(cls) -> dict[str, Any]:
        """
        Generates Docker compose network configuration according to CYBERSOCLE specs.
        """
        return {
            cls.NETWORK_NAME: {
                "driver": "bridge",
                "internal": True,  # Disables internet access
                "ipam": {
                    "driver": "default",
                    "config": [
                        {
                            "subnet": "172.28.0.0/16",
                            "gateway": "172.28.0.1"
                        }
                    ]
                },
                "driver_opts": {
                    "com.docker.network.bridge.enable_icc": "false"  # Microsegmentation: disable inter-container communication by default
                }
            }
        }

    @classmethod
    def get_ship_ip_assignments(cls) -> dict[str, str]:
        """
        Static IP mapping for the 5 ships on reseau-prive.
        """
        return {
            "officiel": "172.28.0.10",
            "prison": "172.28.0.20",
            "modele": "172.28.0.30",
            "science": "172.28.0.40",
            "test": "172.28.0.50"
        }
