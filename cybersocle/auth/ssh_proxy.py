"""
SSH Gateway Proxy & Deception Engine for CYBERSOCLE.
Routes mike-vrai to Bateau OFFICIEL (with VPN) and mike-faux to Bateau PRISON (honeypot).
"""

from typing import Any
from cybersocle.auth.tpm_attestation import HardwareAttestationValidator


class BehavioralAIAuthAgent:
    """
    Small AI Behavioral Analysis Agent that monitors session dynamics for user 'mike'.
    Evaluates typing rhythm, command execution velocity, unusual syscalls, and access hours
    to calculate a behavioral risk anomaly score.
    """

    def analyze_session_behavior(self, session_metrics: dict[str, Any] | None = None) -> dict[str, Any]:
        if not session_metrics:
            return {"anomaly_score": 0.0, "risk_level": "LOW", "suspicious": False}

        typing_latency = session_metrics.get("typing_rhythm_ms", 150)
        cmd_velocity = session_metrics.get("command_velocity_per_min", 5)
        unexpected_syscalls = session_metrics.get("unexpected_syscall_count", 0)
        off_hours = session_metrics.get("off_hours", False)

        anomaly_score = 0.0

        # Automated bot script or stolen key execution velocity
        if cmd_velocity > 30:
            anomaly_score += 0.4
        elif cmd_velocity > 15:
            anomaly_score += 0.2

        # Non-human typing cadence (e.g. paste-bin or automated script input)
        if typing_latency < 20 or typing_latency > 2000:
            anomaly_score += 0.3

        if unexpected_syscalls > 0:
            anomaly_score += 0.35

        if off_hours:
            anomaly_score += 0.15

        anomaly_score = min(1.0, round(anomaly_score, 2))
        suspicious = anomaly_score >= 0.60

        return {
            "anomaly_score": anomaly_score,
            "risk_level": "HIGH" if suspicious else "LOW",
            "suspicious": suspicious,
            "details": f"Command velocity: {cmd_velocity}/min, Syscalls: {unexpected_syscalls}"
        }


class SSHAuthenticationGateway:
    """
    SSH authentication proxy enforcing credentials, hardware key checks, TPM attestation,
    and Behavioral AI Analysis Agent routing.
    """

    def __init__(
        self,
        attestation_validator: HardwareAttestationValidator | None = None,
        behavioral_agent: BehavioralAIAuthAgent | None = None
    ):
        self.attestation_validator = attestation_validator or HardwareAttestationValidator()
        self.behavioral_agent = behavioral_agent or BehavioralAIAuthAgent()
        self.valid_credentials = {
            "mike": "mike_secure_pass_2025"
        }

    def authenticate_and_route(
        self,
        username: str,
        password: str,
        encryption_key: str | None = None,
        tpm_signature: str | None = None,
        pcr_quote: str | None = None,
        session_behavior_metrics: dict[str, Any] | None = None
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

        behavioral_res = self.behavioral_agent.analyze_session_behavior(session_behavior_metrics)
        behavior_suspicious = behavioral_res["suspicious"]

        # Mike is authentic only if local key, TPM quote, and behavioral analysis ALL pass
        is_mike_vrai = is_key_valid and is_tpm_valid and not behavior_suspicious

        if is_mike_vrai:
            return {
                "authenticated": True,
                "identity": f"{username}-vrai",
                "target_ship": "OFFICIEL",
                "cell_id": f"cell-prod-{username}",
                "vpn_access": True,
                "honeypot": False,
                "behavioral_analysis": behavioral_res,
                "message": "Authenticated as authentic user with verified behavioral score. Routing to Bateau OFFICIEL."
            }
        else:
            reason = "Behavioral AI flagged session" if behavior_suspicious else "Invalid hardware key or TPM quote"
            return {
                "authenticated": True,
                "identity": f"{username}-faux",
                "target_ship": "PRISON",
                "cell_id": f"cell-honeypot-{username}",
                "vpn_access": False,
                "honeypot": True,
                "behavioral_analysis": behavioral_res,
                "message": f"Deception activated ({reason}). Transparently routing to Bateau PRISON honeypot."
            }
