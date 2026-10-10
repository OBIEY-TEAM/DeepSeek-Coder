"""
Unidirectional Log Pipe (Valve) using Fluent-Bit / Rsyslog for CYBERSOCLE.
"""

from typing import Any


class UnidirectionalLogPipe:
    def __init__(self, db_log_endpoint: str = "http://172.28.0.250:8080/logs"):
        self.db_log_endpoint = db_log_endpoint

    def get_fluent_bit_config(self, cell_id: str) -> str:
        return f"""\
[INPUT]
    Name        tail
    Path        /var/log/cybersocle/{cell_id}.log
    Tag         cell.{cell_id}

[FILTER]
    Name        record_modifier
    Match       *
    Record      cell_id {cell_id}

[OUTPUT]
    Name        http
    Match       *
    Host        172.28.0.250
    Port        8080
    URI         /logs/v1/ingest
    Format      json
"""

    def forward_sidecar_log(self, log_record: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "INGESTED",
            "destination": self.db_log_endpoint,
            "record": log_record
        }


class UnidirectionalThreatDiode:
    """
    Simulates hardware network diode transmission for automated threat intelligence & security rule propagation.
    Guarantees strict unidirectional flow (no return channel / back-door communication).
    """

    def __init__(self, diode_id: str = "diode-hw-01"):
        self.diode_id = diode_id
        self.transmitted_count = 0

    def transmit_threat_intel(
        self,
        payload: dict[str, Any],
        source_ship: str = "SCIENCE_LOCAL",
        destination_ship: str = "SCIENCE_LAB"
    ) -> dict[str, Any]:

        self.transmitted_count += 1
        return {
            "status": "TRANSMITTED_UNIDIRECTIONAL",
            "diode_id": self.diode_id,
            "source": source_ship,
            "destination": destination_ship,
            "return_channel_blocked": True,
            "airgap_equivalent_security": True,
            "payload_summary": {
                "keys": list(payload.keys()),
                "stix_present": "stix_cybercards" in payload or payload.get("type") == "bundle"
            },
            "sequence_id": self.transmitted_count
        }
