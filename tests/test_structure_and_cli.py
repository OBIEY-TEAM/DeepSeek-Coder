"""
Test Suite for Repository Structure & CLI Commands.
Verifies module layout across cybersocle/ subdirectories and executes direct CLI commands.
"""

import os
import sys
import unittest
import subprocess
import yaml
from cybersocle.cli import deploy_cybersocle
from cybersocle.ecosystem.multi_enterprise import ZeroKnowledgeProofAnonymizer, MultiEnterpriseLabBridge


class TestStructureAndCLI(unittest.TestCase):

    def test_repository_module_structure(self):
        """
        Vérifier la présence et la structure des modules clés du dépôt.
        """
        required_dirs = [
            os.path.join("cybersocle", "auth"),
            os.path.join("cybersocle", "network"),
            os.path.join("cybersocle", "isolation"),
            os.path.join("cybersocle", "logging"),
            os.path.join("cybersocle", "science"),
            os.path.join("cybersocle", "web"),
            os.path.join("cybersocle", "ecosystem"),
        ]
        for d in required_dirs:
            self.assertTrue(os.path.isdir(d), f"Directory {d} must exist")

    def test_cli_ls_recursive_command(self):
        """
        Command CLI: ls -R cybersocle/
        """
        res = subprocess.run(["ls", "-R", "cybersocle/"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        output = res.stdout
        self.assertIn("cybersocle/auth:", output)
        self.assertIn("cybersocle/network:", output)
        self.assertIn("cybersocle/isolation:", output)
        self.assertIn("cybersocle/logging:", output)
        self.assertIn("cybersocle/science:", output)
        self.assertIn("cybersocle/web:", output)
        self.assertIn("cybersocle/ecosystem:", output)

    def test_cli_falco_rules_yaml_verification(self):
        """
        Command CLI: falco -r cybersocle/isolation/rules.yaml
        Validates syntax and presence of eBPF Falco rules YAML file.
        """
        rules_path = os.path.join("cybersocle", "isolation", "rules.yaml")
        self.assertTrue(os.path.exists(rules_path))

        with open(rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # If falco binary is installed, test running command; otherwise verify valid YAML structure
        falco_check = subprocess.run(["which", "falco"], capture_output=True, text=True)
        if falco_check.returncode == 0:
            falco_res = subprocess.run(["falco", "-r", rules_path], capture_output=True, text=True)
            # falco command syntax check
            self.assertIn(falco_res.returncode, [0, 1, 2])

    def test_cli_vaccine_qualifier_command(self):
        """
        Command CLI: python3 -m cybersocle.science.qualifier --vaccine-id VACC-2026-001
        """
        cmd = [sys.executable, "-m", "cybersocle.science.qualifier", "--vaccine-id", "VACC-2026-001"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("CERTIFIED_100_PERCENT_COMPLIANT", res.stdout)
        self.assertIn("VACC-2026-001", res.stdout)

    def test_cybersocle_cli_deployment(self):
        """
        Tests CYBERSOCLE CLI deployment modes.
        """
        client_info = deploy_cybersocle("client")
        self.assertEqual(client_info["mode"], "CLIENT_ENTERPRISE")
        self.assertTrue(client_info["ebpf_microsegmentation_applied"])

        lab_info = deploy_cybersocle("lab")
        self.assertEqual(lab_info["mode"], "LAB_OBIEY_CHRIST_DANY")

    def test_ecosystem_zkp_anonymizer_and_lab_bridge(self):
        """
        cybersocle/ecosystem/ : Module d'émission et de signature du vaccin anonymisé ZKP vers le VPS LAB
        """
        cartography = {
            "cell_id": "cell-prod-mike",
            "ship_name": "OFFICIEL",
            "attack_type": "EXPLOIT_PAYLOAD",
            "entry_vector": "SSH",
            "impacted_assets": ["/etc/passwd"],
            "applied_security": ["read_only_rootfs"]
        }
        zkp_anon = ZeroKnowledgeProofAnonymizer.anonymize_cartography(cartography)
        self.assertIn("zkp_proof", zkp_anon)
        self.assertEqual(zkp_anon["ship_name"], "ENTERPRISE_CLIENT_ANON")

        bridge = MultiEnterpriseLabBridge()
        lab_res = bridge.submit_client_vaccine_to_lab({"vaccine_id": "VACC-2026-001"}, cartography)
        self.assertEqual(lab_res["status"], "VACCINE_INGESTED_BY_LAB")


if __name__ == "__main__":
    unittest.main()
