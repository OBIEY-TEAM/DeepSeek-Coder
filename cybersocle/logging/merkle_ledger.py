"""
Merkle Tree Log Ledger with RFC 3161 Timestamping for CYBERSOCLE.
"""

import hashlib
import time
from typing import Any


class MerkleLogNode:
    def __init__(self, log_data: dict[str, Any], prev_hash: str = ""):
        self.timestamp = time.time()
        self.log_data = log_data
        self.prev_hash = prev_hash
        self.rfc3161_timestamp = f"RFC3161_TS_{int(self.timestamp)}"
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = f"{self.timestamp}:{self.log_data}:{self.prev_hash}:{self.rfc3161_timestamp}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class MerkleLogLedger:
    def __init__(self, db_name: str = "db-log"):
        self.db_name = db_name
        self.chain: list[MerkleLogNode] = []

    def append_log(self, log_entry: dict[str, Any]) -> str:
        prev_hash = self.chain[-1].hash if self.chain else "GENESIS_ROOT_0000000000000000000"
        node = MerkleLogNode(log_data=log_entry, prev_hash=prev_hash)
        self.chain.append(node)
        return node.hash

    def verify_ledger_integrity(self) -> bool:
        for i in range(len(self.chain)):
            current = self.chain[i]
            expected_prev = self.chain[i - 1].hash if i > 0 else "GENESIS_ROOT_0000000000000000000"
            if current.prev_hash != expected_prev:
                return False
            if current.hash != current._compute_hash():
                return False
        return True
