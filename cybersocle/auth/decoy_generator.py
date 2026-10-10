"""
Dynamic Decoy & Canary Token Generator for CYBERSOCLE Honeypot (Bateau PRISON).
Generates context-aware fake corporate files and plants active canary tokens.
"""

import uuid
from typing import Any


class DynamicDecoyGenerator:
    """
    Generates dynamic decoy documents (PDF, Excel, fake API keys) and tracks canary tokens.
    """

    def __init__(self):
        self.canary_tokens_db: dict[str, dict[str, Any]] = {}

    def create_canary_token(self, token_type: str, description: str) -> str:
        token_id = f"canary_key_{uuid.uuid4().hex[:12]}"
        self.canary_tokens_db[token_id] = {
            "token_type": token_type,
            "description": description,
            "triggered": False,
            "trigger_count": 0,
            "last_trigger_time": None
        }
        return token_id

    def generate_decoy_dataset_for_cell(self, cell_id: str) -> dict[str, Any]:
        aws_canary = self.create_canary_token("AWS_KEY", "Fake production AWS Secret in honeypot")
        webhook_canary = self.create_canary_token("WEBHOOK", "Fake internal admin portal URL")

        decoy_files = [
            {
                "path": "/home/mike/documents/bilan_financier_2024.pdf",
                "content_type": "pdf",
                "size_kb": 120,
                "is_decoy": True
            },
            {
                "path": "/home/mike/.aws/credentials",
                "content_type": "text/plain",
                "content": f"[default]\naws_access_key_id = AKIAIO5FNN72EXMPL\naws_secret_access_key = {aws_canary}",
                "is_decoy": True
            },
            {
                "path": "/home/mike/config/internal_portal.json",
                "content_type": "application/json",
                "content": f'{{"admin_url": "http://10.0.0.5/login?token={webhook_canary}"}}',
                "is_decoy": True
            }
        ]

        return {
            "cell_id": cell_id,
            "files": decoy_files,
            "canary_tokens": list(self.canary_tokens_db.keys())
        }

    def check_canary_token_trigger(self, token_id: str) -> dict[str, Any]:
        if token_id in self.canary_tokens_db:
            token = self.canary_tokens_db[token_id]
            token["triggered"] = True
            token["trigger_count"] += 1
            return {
                "alert": "CRITICAL_HONEYPOT_TRIGGER",
                "token_id": token_id,
                "description": token["description"],
                "action": "Elevate isolation level and notify SOC"
            }
        return {"alert": "UNKNOWN_TOKEN"}
