"""
Incident Manager handling cell cloning, network unlinking, OFFICIEL regeneration (2FA), PRISON regeneration, and SCIENCE recovery.
"""

import time
from typing import Any
from cybersocle.llm.stix_cybercards import STIXCybercardGenerator


class IncidentIsolationManager:
    def __init__(self):
        self.stix_generator = STIXCybercardGenerator()
        self.active_officiel_ships: list[dict[str, Any]] = [
            {"ship_id": "ship-officiel-1", "status": "HEALTHY", "cells": ["cell-mike", "cell-admin"]}
        ]
        self.active_prison_ships: list[dict[str, Any]] = [
            {"ship_id": "ship-prison-1", "status": "HEALTHY", "cells": []}
        ]
        self.science_ship = {"ship_id": "ship-science-1", "status": "HEALTHY", "last_clean_checkpoint": "v1.0.0"}

    def isolate_cell_and_clone_to_prison(self, cell_id: str, user_id: str) -> dict[str, Any]:
        cartography = self.stix_generator.generate_cybercartography(
            cell_id=cell_id,
            ship_name="OFFICIEL",
            attack_type="MALWARE_EXECUTION_DETECTED",
            entry_vector="SSH_SESSION_PAYLOAD",
            impacted_assets=["/tmp/malware.bin"],
            applied_security=["read_only_rootfs", "cgroups_2g"],
            recommendations=["isolate_to_prison", "enable_2fa_on_officiel"]
        )

        cloned_cell_id = f"{cell_id}-prison-clone"
        self.active_prison_ships[0]["cells"].append(cloned_cell_id)

        if cell_id in self.active_officiel_ships[0]["cells"]:
            self.active_officiel_ships[0]["cells"].remove(cell_id)

        return {
            "action": "CELL_ISOLATION_AND_CLONING_COMPLETE",
            "original_cell": cell_id,
            "cloned_cell": cloned_cell_id,
            "target_ship": "PRISON",
            "session_redirected": True,
            "cybercartography": cartography
        }

    def regenerate_officiel_ship(self, infected_ship_id: str, affected_cell_id: str) -> dict[str, Any]:
        new_ship_id = f"ship-officiel-2-{int(time.time())}"
        clean_cells = [c for c in self.active_officiel_ships[0]["cells"] if c != affected_cell_id]

        new_ship = {
            "ship_id": new_ship_id,
            "status": "HEALTHY",
            "cells": clean_cells,
            "ssh_blocked": True,
            "alert_sent_to_client": True,
            "two_factor_auth_required_count": 10,
            "first_reconnect_client_validation_required": True
        }

        self.active_officiel_ships = [new_ship]

        return {
            "status": "OFFICIEL_SHIP_REGENERATED",
            "old_ship": infected_ship_id,
            "new_ship": new_ship_id,
            "two_factor_logins_remaining": 10,
            "client_validation_required": True
        }

    def regenerate_prison_ship_on_escape(self, attacker_cell_id: str) -> dict[str, Any]:
        old_prison_id = self.active_prison_ships[0]["ship_id"]
        new_prison_id = f"ship-prison-2-{int(time.time())}"

        transferred_cells = [c for c in self.active_prison_ships[0]["cells"] if c != attacker_cell_id]

        escaped_cartography = self.stix_generator.generate_cybercartography(
            cell_id=attacker_cell_id,
            ship_name="PRISON",
            attack_type="CONTAINER_ESCAPE_ATTEMPT",
            entry_vector="PRISON_PIVOT",
            impacted_assets=["docker.sock"],
            applied_security=["ebpf_cilium_quarantine"],
            recommendations=["regenerate_prison_and_patch_kernel"]
        )

        new_prison = {
            "ship_id": new_prison_id,
            "status": "HEALTHY",
            "cells": transferred_cells
        }

        self.active_prison_ships = [new_prison]

        return {
            "status": "PRISON_SHIP_REGENERATED",
            "destroyed_ship": old_prison_id,
            "new_ship": new_prison_id,
            "transferred_cells": transferred_cells,
            "dispatched_to_science": True,
            "cybercartography": escaped_cartography
        }

    def regenerate_science_ship() -> dict[str, Any]:
        self.science_ship["status"] = "REGENERATED_CLEAN"
        return {
            "status": "SCIENCE_SHIP_REGENERATED",
            "checkpoint": self.science_ship["last_clean_checkpoint"]
        }
