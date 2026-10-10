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
