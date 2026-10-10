"""
SSH Gateway Proxy & Deception Engine for CYBERSOCLE.
Routes mike-vrai to Bateau OFFICIEL (with VPN) and mike-faux to Bateau PRISON (honeypot).
"""

from typing import Any
from cybersocle.auth.tpm_attestation import HardwareAttestationValidator


class SSHAuthenticationGateway:
    """
    SSH authentication proxy enforcing credentials, hardware key checks, and deception routing.
    """

    def __init__(self, attestation_validator: HardwareAttestationValidator | None = None):
        self.attestation_validator = attestation_validator or HardwareAttestationValidator()
        self.valid_credentials = {
            "mike": "mike_secure_pass_2025"
        }

    def authenticate_and_route(
        self,
        username: str,
        password: str,
        encryption_key: str | None = None,
        tpm_signature: str | None = None,
        pcr_quote: str | None = None
    ) -> dict[str, Any]:
        if username not in self.valid_credentials or password != self.valid_credentials[username]:
            return {
                "authenticated": False,
                "status": "DENIED",
                "message": "Invalid username or password"
            }

        is_key_valid = encryption_key is not None and encryption_key.startswith("valid_local_key_")
        is_tpm_valid = False
        if tpm_signature and pcr_quote:
            is_tpm_valid = self.attestation_validator.verify_tpm_quote(
                username=username,
                tpm_signature=tpm_signature,
                pcr_quote_hash=pcr_quote
            )

        is_mike_vrai = is_key_valid and is_tpm_valid

        if is_mike_vrai:
            return {
                "authenticated": True,
                "identity": f"{username}-vrai",
                "target_ship": "OFFICIEL",
                "cell_id": f"cell-prod-{username}",
                "vpn_access": True,
                "honeypot": False,
                "message": "Authenticated as authentic user. Routing to Bateau OFFICIEL with corporate VPN."
            }
        else:
            return {
                "authenticated": True,
                "identity": f"{username}-faux",
                "target_ship": "PRISON",
                "cell_id": f"cell-honeypot-{username}",
                "vpn_access": False,
                "honeypot": True,
                "message": "Deception activated. Transparently routing attacker to Bateau PRISON honeypot cell."
            }
