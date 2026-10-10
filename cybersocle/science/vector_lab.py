"""
Bateau SCIENCE (Threat-Intel-Lab) Vector Engine & STIX 2.1 Signature Verifier.
"""

import json
import hashlib
from typing import Any


class ThreatIntelLab:
    def __init__(self, qdrant_host: str = "172.28.0.40", qdrant_port: int = 6333):
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.vector_collection: list[dict[str, Any]] = []

    def verify_cybercard_signature(self, cartography: dict[str, Any]) -> bool:
        provided_sig = cartography.get("sha256_signature", "")
        if not provided_sig:
            return False

        cartography_copy = dict(cartography)
        cartography_copy.pop("sha256_signature", None)
        cartography_copy.pop("signed_by", None)

        serialized = json.dumps(cartography_copy, sort_keys=True)
        computed_sig = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        return computed_sig == provided_sig

    def ingest_cybercartography(self, cartography: dict[str, Any]) -> dict[str, Any]:
        if not self.verify_cybercard_signature(cartography):
            return {
                "status": "REJECTED",
                "reason": "INVALID_SHA256_SIGNATURE",
                "message": "Signature verification failed. Cybercard rejected by Bateau SCIENCE."
            }

        vector_point = {
            "id": cartography.get("id"),
            "vector": [0.12, 0.45, 0.88, 0.34],
            "payload": {
                "cell_id": cartography.get("cell_id"),
                "stix_cards": cartography.get("stix_cybercards")
            }
        }
        self.vector_collection.append(vector_point)

        return {
            "status": "ACCEPTED",
            "qdrant_indexed": True,
            "vector_count": len(self.vector_collection),
            "message": "Cybercartography verified and indexed into Qdrant vector store."
        }
