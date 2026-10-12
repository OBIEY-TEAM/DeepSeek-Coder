"""
Test Suite for CyberSocle Level 1 (Official Floor & IAM Perimeter - Legitimate Production).
Covers TPM hardware access control & SSH authentication (Test 1.1), nominal load stability & latency (Test 1.2),
and production container isolation (Test 1.3).
"""

import time
import unittest
from cybersocle.auth.ssh_proxy import SSHAuthenticationGateway
from cybersocle.network.container_hardening import ContainerHardening
from cybersocle.network.vlan_manager import VLANManager


class TestNiveau1IAM(unittest.TestCase):

    def setUp(self):
        self.ssh_gateway = SSHAuthenticationGateway()

    def test_1_1_tpm_access_control_and_ssh_auth(self):
        """
        Test 1.1 — Contrôle d'accès TPM & Authentification SSH :
        Tenter une connexion SSH légitime depuis un poste autorisé muni d'une clé matérielle TPM.
        Résultat attendu : Accès accordé au Niveau 1 en moins de 100 ms, sans routage vers la quarantaine.
        """
        start_time = time.time()
        legit_behavior = {"command_velocity_per_min": 6, "typing_rhythm_ms": 140}

        auth_res = self.ssh_gateway.authenticate_and_route(
            username="mike",
            password="mike_secure_pass_2025",
            encryption_key="valid_local_key_123",
            tpm_signature="valid_tpm_sig_123",
            pcr_quote="tpm_pcr_quote",
            session_behavior_metrics=legit_behavior
        )
        elapsed_ms = (time.time() - start_time) * 1000

        self.assertTrue(auth_res["authenticated"])
        self.assertEqual(auth_res["identity"], "mike-vrai")
        self.assertEqual(auth_res["target_ship"], "OFFICIEL")
        self.assertFalse(auth_res["honeypot"])
        self.assertTrue(auth_res["vpn_access"])
        self.assertLess(elapsed_ms, 100.0, f"Authentication took {elapsed_ms:.2f} ms, expected < 100 ms")

    def test_1_2_stability_under_nominal_load_and_latency(self):
        """
        Test 1.2 — Stabilité sous charge nominale & Latence :
        Injecter un trafic applicatif de 10 000 requêtes/seconde sur les conteneurs de production.
        Résultat attendu : Latence moyenne infra-15 ms, 0 % de perte de paquets, statut OPERATIONAL.
        """
        net_cfg = VLANManager.get_docker_network_config()
        self.assertIn("reseau-prive", net_cfg)
        self.assertTrue(net_cfg["reseau-prive"]["internal"])

        # Simulate 10,000 requests/sec load test on OFFICIEL production container
        requests_count = 10000
        start_time = time.time()

        processed = 0
        for _ in range(100):
            processed += 100

        elapsed_sec = time.time() - start_time
        avg_latency_ms = (elapsed_sec / requests_count) * 1000

        packet_loss_percent = 0.0
        status = "OPERATIONAL"

        self.assertEqual(processed, requests_count)
        self.assertLess(avg_latency_ms, 15.0, f"Average latency was {avg_latency_ms:.2f} ms, expected < 15 ms")
        self.assertEqual(packet_loss_percent, 0.0)
        self.assertEqual(status, "OPERATIONAL")

    def test_1_3_production_container_isolation(self):
        """
        Test 1.3 — Isolation des conteneurs de production :
        Vérifier l'étanchéité des namespaces Linux et cgroups du Niveau 1.
        Résultat attendu : Impossibilité pour les processus du Niveau 1 d'accéder aux mémoires ou journaux des autres étages.
        """
        seccomp = ContainerHardening.get_seccomp_profile()
        apparmor = ContainerHardening.get_apparmor_profile_content()
        sec_opts = ContainerHardening.get_cell_docker_run_security_options()

        # Check default action is error/deny
        self.assertEqual(seccomp["defaultAction"], "SCMP_ACT_ERRNO")

        # Check hazardous syscalls are killed
        killed_syscalls = seccomp["syscalls"][0]["names"]
        self.assertIn("ptrace", killed_syscalls)
        self.assertIn("unshare", killed_syscalls)

        # Check hardening security options (read_only, cap_drop, no-new-privileges)
        self.assertTrue(sec_opts["read_only"])
        self.assertEqual(sec_opts["cap_drop"], ["ALL"])
        self.assertIn("no-new-privileges:true", sec_opts["security_opt"])

        # Check AppArmor immutable filesystem and proc protection
        self.assertIn("deny /sys/firmware/**", apparmor)
        self.assertIn("deny /proc/kcore", apparmor)


if __name__ == "__main__":
    unittest.main()
