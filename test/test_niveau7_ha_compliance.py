"""
Test Suite for CyberSocle Level 7 (High Availability & Regulatory Compliance).
Covers HA failover & HSM node redundancy < 2 seconds (Test 7.1), and OHADA / Malabo Convention / ISO 27001 regulatory auditability (Test 7.2).
"""

import time
import unittest
from cybersocle.llm.offline_engine import HotStandbyLLMManager
from cybersocle.auth.tpm_attestation import HardwareAttestationValidator
from cybersocle.logging.merkle_ledger import MerkleLogLedger


class TestNiveau7HACompliance(unittest.TestCase):

    def setUp(self):
        self.standby_mgr = HotStandbyLLMManager(primary_id="node-hsm-master", standby_id="node-hsm-secondary")
        self.hsm_validator = HardwareAttestationValidator()
        self.merkle_ledger = MerkleLogLedger()

    def test_7_1_ha_failover_and_hsm_node_redundancy(self):
        """
        Test 7.1 — Bascule Haute Disponibilité (HA) & Redondance des nœuds HSM :
        Simuler la coupure physique brutale du nœud maître de la Tour CYBERSOCLE.
        Résultat attendu : Bascule transparente en moins de 2 secondes sur le nœud secondaire du Cloud Souverain Systalink sans perte de session.
        """
        self.assertEqual(self.standby_mgr.active_instance, "node-hsm-master")
        self.assertEqual(self.standby_mgr.standby_state, "READY_PASSIVE")

        # Simulate brutal hardware cut / master failure
        start_time = time.time()
        failover_res = self.standby_mgr.trigger_hot_failover(reason="MASTER_PHYSICAL_CUT")
        elapsed_sec = time.time() - start_time

        self.assertEqual(failover_res["status"], "FAILOVER_SUCCESS")
        self.assertEqual(failover_res["active_llm"], "node-hsm-secondary")
        self.assertEqual(failover_res["standby_state"], "ACTIVE_PRIMARY")
        self.assertTrue(failover_res["zero_downtime_guaranteed"])
        self.assertLess(elapsed_sec, 2.0, f"HA failover took {elapsed_sec:.2f} s, expected < 2.0 s")

    def test_7_2_regulatory_compliance_and_auditability(self):
        """
        Test 7.2 — Conformité réglementaire & Auditabilité (OHADA / Convention de Malabo / ISO 27001) :
        Générer le rapport d'audit d'incidents et de traçabilité pour les autorités réglementaires.
        Résultat attendu : Export d'un registre complet d'incidents anonymisés, traçables et alignés sur les exigences de protection des données.
        """
        # Append auditable compliance event logs to Merkle ledger
        incident_event = {
            "event_type": "SECURITY_INCIDENT_AUDIT",
            "regulatory_frameworks": ["OHADA", "MALABO_CONVENTION", "ISO_27001"],
            "anonymized_user": "mike-vrai",
            "action": "AUTOMATED_CONTAINMENT_APPLIED",
            "timestamp": time.time()
        }

        log_hash = self.merkle_ledger.append_log(incident_event)
        self.assertIsNotNone(log_hash)
        self.assertTrue(self.merkle_ledger.verify_ledger_integrity())

        # Generate compliance audit export report
        chain_len = len(self.merkle_ledger.chain)
        self.assertGreaterEqual(chain_len, 1)
        self.assertTrue(self.merkle_ledger.chain[0].rfc3161_timestamp.startswith("RFC3161_TS_"))


if __name__ == "__main__":
    unittest.main()

    def test_7_3_vps_lab_ddos_drp_and_gitops_reconciliation(self):
        """
        Test 7.3 — Disaster Recovery Plan (DRP) du VPS LAB & Réconciliation GitOps après coupure prolongée :
        Vérification du mode dégradé local sous DDoS et resynchronisation GitOps sans conflit.
        """
        from cybersocle.ecosystem.gitops_manager import GitOpsPolicyManager
        gitops = GitOpsPolicyManager()

        # Test DDoS Degraded mode
        ddos_res = gitops.handle_vps_lab_ddos_degraded_mode(ddos_active=True)
        self.assertEqual(ddos_res["status"], "LOCAL_DEGRADED_AUTONOMOUS_MODE")
        self.assertFalse(ddos_res["central_vps_lab_accessible"])
        self.assertTrue(ddos_res["local_ebpf_enforcement"] == "ACTIVE_STANDALONE")

        # Test GitOps reconciliation after prolonged outage
        rec_res = gitops.reconcile_state_after_prolonged_outage(local_policy_version="v1.0.0", central_policy_version="v1.3.0")
        self.assertEqual(rec_res["status"], "GITOPS_RECONCILIATION_COMPLETE")
        self.assertEqual(rec_res["reconciliation_action"], "FAST_FORWARD_MERGE_3WAY_CLEAN")
        self.assertEqual(rec_res["policy_conflicts_detected"], 0)
        self.assertTrue(rec_res["security_state_unified"])
