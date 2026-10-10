"""
Comprehensive Unit & Integration Test Suite for CYBERSOCLE Architecture.
Tests all modules: Network, Auth, Logging, LLM, Isolation, Science, Web, Ecosystem, and CLI.
"""

import sys
sys.path.insert(0, "/app")

import unittest
from cybersocle.network.ebpf_cilium import apply_ebpf_microsegmentation, CiliumPolicyGenerator
from cybersocle.network.vlan_manager import VLANManager
from cybersocle.network.container_hardening import ContainerHardening
from cybersocle.auth.tpm_attestation import HardwareAttestationValidator
from cybersocle.auth.ssh_proxy import SSHAuthenticationGateway
from cybersocle.auth.decoy_generator import DynamicDecoyGenerator
from cybersocle.auth.browser_isolation import CellBrowserIsolationController
from cybersocle.logging.sidecar_falco import FalcoSidecarSpy
from cybersocle.logging.unidirectional_pipe import UnidirectionalLogPipe
from cybersocle.logging.merkle_ledger import MerkleLogLedger
from cybersocle.llm.offline_engine import OfflineLLMEngine
from cybersocle.llm.stix_cybercards import STIXCybercardGenerator
from cybersocle.isolation.incident_manager import IncidentIsolationManager
from cybersocle.science.vector_lab import ThreatIntelLab
from cybersocle.science.vaccine_engine import VaccineGenerator
from cybersocle.science.vaccine_validation import FormalVaccineValidator
from cybersocle.ecosystem.multi_enterprise import MultiEnterpriseLabBridge, ZeroKnowledgeProofAnonymizer
from cybersocle.ecosystem.gitops_manager import GitOpsPolicyManager
from cybersocle.cli import deploy_cybersocle


class TestCybersocleSystem(unittest.TestCase):

    # --- 1. Network & Hardening Tests ---
    def test_ebpf_microsegmentation_policies(self):
        policies = apply_ebpf_microsegmentation()
        self.assertIn("officiel", policies)
        self.assertIn("prison", policies)
        self.assertIn("modele", policies)
        self.assertIn("science", policies)
        self.assertIn("test", policies)

    def test_vlan_manager_config(self):
        config = VLANManager.get_docker_network_config()
        self.assertIn("reseau-prive", config)
        self.assertTrue(config["reseau-prive"]["internal"])

    def test_container_hardening_options(self):
        opts = ContainerHardening.get_cell_docker_run_security_options(is_coffre_fort=True)
        self.assertTrue(opts["read_only"])
        self.assertEqual(opts["runtime"], "kata-fc")

    # --- 2. Auth, TPM & Deception Tests ---
    def test_ssh_authentication_gateway_mike_vrai(self):
        gateway = SSHAuthenticationGateway()
        res = gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="valid_local_key_abc",
            tpm_signature="valid_tpm_sig_123",
            pcr_quote="quote_xyz"
        )
        self.assertTrue(res["authenticated"])
        self.assertEqual(res["target_ship"], "OFFICIEL")
        self.assertTrue(res["vpn_access"])
        self.assertFalse(res["honeypot"])

    def test_ssh_authentication_gateway_mike_faux_honeypot(self):
        gateway = SSHAuthenticationGateway()
        res = gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="wrong_or_missing_key"
        )
        self.assertTrue(res["authenticated"])
        self.assertEqual(res["target_ship"], "PRISON")
        self.assertFalse(res["vpn_access"])
        self.assertTrue(res["honeypot"])

    def test_decoy_generator_and_canary_tokens(self):
        decoy = DynamicDecoyGenerator()
        dataset = decoy.generate_decoy_dataset_for_cell("cell-honeypot-mike")
        self.assertEqual(dataset["cell_id"], "cell-honeypot-mike")
        self.assertTrue(len(dataset["canary_tokens"]) > 0)

        canary_id = dataset["canary_tokens"][0]
        alert = decoy.check_canary_token_trigger(canary_id)
        self.assertEqual(alert["alert"], "CRITICAL_HONEYPOT_TRIGGER")

    def test_browser_isolation_controller(self):
        officiel_browser = CellBrowserIsolationController.configure_cell_browser("OFFICIEL", is_affected=False)
        self.assertTrue(officiel_browser["vpn_tunnel_active"])

        prison_browser = CellBrowserIsolationController.configure_cell_browser("PRISON", is_affected=True)
        self.assertFalse(prison_browser["vpn_tunnel_active"])

    # --- 3. Logging, Sidecar & Merkle Ledger Tests ---
    def test_falco_sidecar_spy(self):
        spy = FalcoSidecarSpy(cell_id="cell-1", ship_name="OFFICIEL")
        evt = {"type": "execve", "proc_name": "bash"}
        alert = spy.inspect_syscall_event(evt)
        self.assertIsNotNone(alert)
        self.assertEqual(alert["alert"], "REVERSE_SHELL_DETECTED")

    def test_merkle_log_ledger_integrity(self):
        ledger = MerkleLogLedger()
        hash1 = ledger.append_log({"event": "USER_LOGIN", "cell": "cell-1"})
        hash2 = ledger.append_log({"event": "FILE_ACCESS", "cell": "cell-1"})
        self.assertTrue(ledger.verify_ledger_integrity())

        # Tamper with chain
        ledger.chain[0].log_data["event"] = "TAMPERED_EVENT"
        self.assertFalse(ledger.verify_ledger_integrity())

    # --- 4. Offline LLM & STIX 2.1 Cybercards Tests ---
    def test_stix_cybercard_generator_and_signature(self):
        gen = STIXCybercardGenerator()
        cartography = gen.generate_cybercartography(
            cell_id="cell-mike",
            ship_name="OFFICIEL",
            attack_type="SQL_INJECTION",
            entry_vector="HTTP_POST",
            impacted_assets=["/db/users"],
            applied_security=["read_only"],
            recommendations=["use_prepared_statements"]
        )
        self.assertIn("sha256_signature", cartography)
        self.assertIn("stix_cybercards", cartography)
        self.assertEqual(cartography["stix_cybercards"]["cybercard_attaque"]["name"], "SQL_INJECTION")

    # --- 5. Incident Isolation & Regeneration Tests ---
    def test_incident_isolation_manager(self):
        mgr = IncidentIsolationManager()
        res = mgr.isolate_cell_and_clone_to_prison("cell-mike", "mike")
        self.assertEqual(res["action"], "CELL_ISOLATION_AND_CLONING_COMPLETE")
        self.assertEqual(res["target_ship"], "PRISON")

        reg_officiel = mgr.regenerate_officiel_ship("ship-officiel-1", "cell-mike")
        self.assertEqual(reg_officiel["two_factor_logins_remaining"], 10)

        reg_prison = mgr.regenerate_prison_ship_on_escape("attacker-cell-1")
        self.assertEqual(reg_prison["status"], "PRISON_SHIP_REGENERATED")

    # --- 6. Bateau SCIENCE & Vaccine Validation Tests ---
    def test_science_vector_lab_signature_verification(self):
        lab = ThreatIntelLab()
        gen = STIXCybercardGenerator()
        valid_cart = gen.generate_cybercartography(
            cell_id="c1", ship_name="OFFICIEL", attack_type="XSS", entry_vector="DOM",
            impacted_assets=["app.js"], applied_security=["csp"], recommendations=["sanitize"]
        )
        res = lab.ingest_cybercartography(valid_cart)
        self.assertEqual(res["status"], "ACCEPTED")

        invalid_cart = dict(valid_cart)
        invalid_cart["sha256_signature"] = "invalid_hash_signature"
        res_invalid = lab.ingest_cybercartography(invalid_cart)
        self.assertEqual(res_invalid["status"], "REJECTED")

    def test_formal_vaccine_validation_and_reset(self):
        gen = VaccineGenerator()
        pkg = gen.generate_vaccine("CMD_INJECTION", "input_string")
        validator = FormalVaccineValidator()
        val_res = validator.validate_vaccine_on_bateau_test(pkg)
        self.assertTrue(val_res["passed"])
        self.assertTrue(val_res["bateau_test_reset"]["clean"])

    # --- 7. Ecosystem & CLI Tests ---
    def test_zkp_anonymizer_and_lab_bridge(self):
        gen = STIXCybercardGenerator()
        cart = gen.generate_cybercartography(
            cell_id="c1", ship_name="OFFICIEL", attack_type="RCE", entry_vector="NET",
            impacted_assets=["srv"], applied_security=["fw"], recommendations=["patch"]
        )
        anon = ZeroKnowledgeProofAnonymizer.anonymize_cartography(cart)
        self.assertIn("zkp_proof", anon)
        self.assertEqual(anon["ship_name"], "ENTERPRISE_CLIENT_ANON")

        bridge = MultiEnterpriseLabBridge()
        lab_res = bridge.submit_client_vaccine_to_lab({"vaccine_id": "v1.0"}, cart)
        self.assertEqual(lab_res["status"], "VACCINE_INGESTED_BY_LAB")

    def test_gitops_policy_manager(self):
        gitops = GitOpsPolicyManager()
        commit_hash = gitops.commit_security_policy_update("V1.0.1", "vaccine-123")
        self.assertTrue(commit_hash.startswith("c01a1a"))

        rollback = gitops.rollback_to_previous_version("V1.0.0")
        self.assertTrue(rollback["success"])

    def test_cli_deployment(self):
        client_deploy = deploy_cybersocle("client")
        self.assertEqual(client_deploy["mode"], "CLIENT_ENTERPRISE")
        self.assertEqual(len(client_deploy["deployed_ships"]), 5)

        lab_deploy = deploy_cybersocle("lab")
        self.assertEqual(lab_deploy["mode"], "LAB_OBIEY_CHRIST_DANY")

    # --- 8. Specific Tests for Architecture Enhancements (Points 1-8) ---
    def test_vaccine_auto_approval_and_rollback(self):
        gen = VaccineGenerator()
        pkg = gen.generate_vaccine("RCE_EXPLOIT", "input_string")
        validator = FormalVaccineValidator()

        # Medium criticality + high confidence -> Auto approved
        res = validator.validate_vaccine_on_bateau_test(pkg, criticality="MEDIUM")
        self.assertEqual(res["status"], "APPROVED_AUTOMATICALLY")
        self.assertTrue(res["auto_approved"])

        # High criticality -> Human validation required
        res_high = validator.validate_vaccine_on_bateau_test(pkg, criticality="HIGH")
        self.assertEqual(res_high["status"], "APPROVED_FOR_HUMAN_VALIDATION")
        self.assertFalse(res_high["auto_approved"])

        # Post-deployment anomaly rollback
        rollback_res = validator.rollback_vaccine_on_anomaly(pkg["vaccine_id"], {"cpu_usage_percent": 95})
        self.assertTrue(rollback_res["rollback_executed"])
        self.assertEqual(rollback_res["status"], "ROLLED_BACK_AUTOMATICALLY")

    def test_unidirectional_threat_diode(self):
        from cybersocle.logging.unidirectional_pipe import UnidirectionalThreatDiode
        diode = UnidirectionalThreatDiode()
        res = diode.transmit_threat_intel({"stix_cybercards": {"card": 1}})
        self.assertEqual(res["status"], "TRANSMITTED_UNIDIRECTIONAL")
        self.assertTrue(res["return_channel_blocked"])

    def test_hot_standby_llm_failover(self):
        from cybersocle.llm.offline_engine import HotStandbyLLMManager, OfflineLLMEngine
        llm = OfflineLLMEngine()
        failover = llm.standby_manager.trigger_hot_failover("TEST_SELF_HEALING")
        self.assertEqual(failover["status"], "FAILOVER_SUCCESS")
        self.assertEqual(failover["active_llm"], "core-llm-standby")
        self.assertIn("core-llm-standby", llm.query_model_offline("Check status"))

    def test_syscall_memory_anonymizer(self):
        spy = FalcoSidecarSpy(cell_id="c1", ship_name="PRISON")
        evt = {"type": "execve", "proc_name": "bash", "details": "password=SecretPass123 0x7fff5fbff880 00 11 22 33 44 55"}
        alert = spy.inspect_syscall_event(evt)
        self.assertTrue(alert["memory_anonymized"])
        self.assertNotIn("SecretPass123", alert["details"])
        self.assertIn("[REDACTED_PASSWORD]", alert["details"])

    def test_hardware_resource_optimization_profiles(self):
        from cybersocle.llm.offline_engine import OfflineLLMEngine
        edge_llm = OfflineLLMEngine(profile="EDGE")
        cfg = edge_llm.get_hardware_resource_config()
        self.assertEqual(cfg["vram_limit_mb"], 2048)

        edge_opts = ContainerHardening.get_cell_docker_run_security_options(profile="EDGE")
        self.assertEqual(edge_opts["mem_limit"], "256m")

    def test_behavioral_ai_auth_agent(self):
        from cybersocle.auth.ssh_proxy import BehavioralAIAuthAgent, SSHAuthenticationGateway
        gateway = SSHAuthenticationGateway()

        # Bot velocity -> flagged as suspicious -> routed to PRISON honeypot
        res = gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="valid_local_key_abc",
            tpm_signature="valid_tpm_sig_123",
            pcr_quote="quote_xyz",
            session_behavior_metrics={"command_velocity_per_min": 50, "typing_rhythm_ms": 5}
        )
        self.assertEqual(res["target_ship"], "PRISON")
        self.assertTrue(res["honeypot"])

    def test_incident_thresholds_and_anti_exhaustion(self):
        mgr = IncidentIsolationManager()
        action1 = mgr.evaluate_incident_action("MALWARE_EXECUTION", ["cell-1"])
        self.assertEqual(action1, IncidentIsolationManager.SEVERITY_CELL_ISOLATION)

        action2 = mgr.evaluate_incident_action("KERNEL_ESCAPE_ATTEMPT", ["cell-1"])
        self.assertEqual(action2, IncidentIsolationManager.SEVERITY_SHIP_DESTRUCTION)

    def test_explicit_cybercard_vps_lab_anonymization(self):
        gen = STIXCybercardGenerator()
        cart = gen.generate_cybercartography(
            cell_id="c1", ship_name="OFFICIEL", attack_type="RCE", entry_vector="HTTP",
            impacted_assets=["/home/mike/secret.txt"], applied_security=["fw"], recommendations=["patch"]
        )
        anon = gen.anonymize_cybercard_for_vps_lab(cart)
        self.assertTrue(anon["cybercard_anonymized_for_vps_lab"])
        self.assertEqual(anon["cell_id"], "cell-anonymized-vps-lab")


if __name__ == "__main__":
    unittest.main()
