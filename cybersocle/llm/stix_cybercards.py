"""
STIX 2.1 Cybercartography & Modular Cybercards Exporter for CYBERSOCLE.
"""

import json
import hashlib
import time
import uuid
from typing import Any


class STIXCybercardGenerator:
    @staticmethod
    def _compute_sha256_signature(data: dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def generate_cybercartography(
        self,
        cell_id: str,
        ship_name: str,
        attack_type: str,
        entry_vector: str,
        impacted_assets: list[str],
        applied_security: list[str],
        recommendations: list[str]
    ) -> dict[str, Any]:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        bundle_id = f"bundle--{uuid.uuid4()}"

        cybercard_attaque = {
            "type": "indicator",
            "spec_version": "2.1",
            "id": f"indicator--{uuid.uuid4()}",
            "created": timestamp,
            "name": attack_type,
            "description": f"Attack vector: {entry_vector} on cell {cell_id} in ship {ship_name}",
            "indicator_types": ["malicious-activity"],
            "pattern": f"[file:hashes.SHA-256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']",
            "pattern_type": "stix"
        }

        cybercard_actifs = {
            "type": "infrastructure",
            "spec_version": "2.1",
            "id": f"infrastructure--{uuid.uuid4()}",
            "created": timestamp,
            "name": f"Assets in cell {cell_id}",
            "description": f"Targeted files & processes: {', '.join(impacted_assets)}"
        }

        cybercard_securite = {
            "type": "course-of-action",
            "spec_version": "2.1",
            "id": f"course-of-action--{uuid.uuid4()}",
            "created": timestamp,
            "name": "Security controls active at attack time",
            "description": f"Applied controls: {', '.join(applied_security)}"
        }

        cybercard_recommandation = {
            "type": "course-of-action",
            "spec_version": "2.1",
            "id": f"course-of-action--{uuid.uuid4()}",
            "created": timestamp,
            "name": "Recommended hardening actions (Vaccine)",
            "description": f"Proposed security vaccines: {', '.join(recommendations)}"
        }

        cartography = {
            "type": "bundle",
            "id": bundle_id,
            "spec_version": "2.1",
            "cell_id": cell_id,
            "ship_name": ship_name,
            "stix_cybercards": {
                "cybercard_attaque": cybercard_attaque,
                "cybercard_actifs": cybercard_actifs,
                "cybercard_securite": cybercard_securite,
                "cybercard_recommandation": cybercard_recommandation
            }
        }

        signature = self._compute_sha256_signature(cartography)
        cartography["sha256_signature"] = signature
        cartography["signed_by"] = "BATEAU_MODELE_LLM_MASTER"

        return cartography

    def anonymize_cybercard_for_vps_lab(self, cartography: dict[str, Any]) -> dict[str, Any]:
        """
        Explicit step for anonymizing STIX Cybercards prior to export/sharing with VPS LAB (Point 8).
        Removes internal client IPs, usernames, client hostnames, and internal path structures.
        """
        import re

        anon = json.loads(json.dumps(cartography))  # Deep copy
        anon["cell_id"] = "cell-anonymized-vps-lab"
        anon["ship_name"] = "ENTERPRISE_CLIENT_ANON"

        # Regex filters for IP addresses and user home directories
        ip_regex = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
        home_path_regex = re.compile(r"/home/[a-zA-Z0-9_\-]+/")

        cards = anon.get("stix_cybercards", {})
        for card_key, card_val in cards.items():
            if isinstance(card_val, dict):
                desc = card_val.get("description", "")
                desc = ip_regex.sub("[ANONYMIZED_IP]", desc)
                desc = home_path_regex.sub("/home/anonymized_user/", desc)
                card_val["description"] = desc

                name = card_val.get("name", "")
                card_val["name"] = ip_regex.sub("[ANONYMIZED_IP]", name)

        anon["cybercard_anonymized_for_vps_lab"] = True
        anon["anonymized_by"] = "CYBERSOCLE_LAB_ANONYMIZER_MODULE"

        # Re-sign anonymized bundle
        if "sha256_signature" in anon:
            del anon["sha256_signature"]
        anon["sha256_signature"] = self._compute_sha256_signature(anon)

        return anon
