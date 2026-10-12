"""
Test Suite for CyberSocle Level 5 (Testbench & Formal Qualification Floor).
Checks Python AST parsing (ast.parse), Bandit vulnerability scanner (0 issues / PASSED),
100% compliance innocuity guarantee, and automatic rollback on post-deployment anomaly.
"""

import unittest
from cybersocle.science.qualifier import FormalVaccineQualifier, VaccineASTChecker
from cybersocle.science.vaccine_validation import FormalVaccineValidator
from cybersocle.science.vaccine_engine import VaccineGenerator


class TestNiveau5Qualifier(unittest.TestCase):

    def setUp(self):
        self.qualifier = FormalVaccineQualifier()
        self.validator = FormalVaccineValidator()
        self.generator = VaccineGenerator()

    def test_ast_python_parsing_blocks_dangerous_instructions(self):
        """
        Analyse syntaxique AST Python (ast.parse) :
        Vérifier que le module inspecte le code et bloque toute instruction à risque
        (ex. os.system, subprocess, eval, exec).
        """
        clean_code = """
import re

def sanitize_input(value: str) -> str:
    return re.sub(r'[;&|`$]', '', value)
"""
        ast_clean = self.qualifier.inspect_ast(clean_code)
        self.assertTrue(ast_clean["passed"])
        self.assertEqual(len(ast_clean["violations"]), 0)

        # Risky code with os.system
        risky_os_code = """
import os

def bad_function():
    os.system("rm -rf /")
"""
        ast_risky_os = self.qualifier.inspect_ast(risky_os_code)
        self.assertFalse(ast_risky_os["passed"])
        self.assertTrue(any("os" in v or "system" in v for v in ast_risky_os["violations"]))

        # Risky code with subprocess
        risky_sub_code = """
import subprocess

def bad_sub():
    subprocess.Popen(["ls", "-l"])
"""
        ast_risky_sub = self.qualifier.inspect_ast(risky_sub_code)
        self.assertFalse(ast_risky_sub["passed"])
        self.assertTrue(any("subprocess" in v for v in ast_risky_sub["violations"]))

    def test_bandit_scanner_zero_issues_passed(self):
        """
        Scanner de vulnérabilités statique Bandit :
        Exécuter Bandit pour confirmer 0 issues / PASSED sur le script de contre-mesure.
        """
        safe_code = """
import re

def filter_sql_params(query_param: str) -> str:
    return re.sub(r"['\";--]", "", query_param)
"""
        bandit_res = self.qualifier.run_bandit_scan(safe_code)
        self.assertTrue(bandit_res["passed"])
        self.assertEqual(bandit_res["issues_found"], 0)
        self.assertEqual(bandit_res["bandit_output"], "0 issues / PASSED")

    def test_innocuity_guarantee_and_100_percent_compliance(self):
        """
        Garantie d'innocuité :
        Valider que seuls les vaccins obtenant un score de conformité de 100% sont certifiés.
        """
        report = self.qualifier.qualify_vaccine("VACC-2026-001")
        self.assertEqual(report["compliance_score"], 100.0)
        self.assertTrue(report["certified"])
        self.assertEqual(report["status"], "CERTIFIED_100_PERCENT_COMPLIANT")
        self.assertEqual(report["innocuity_guarantee"], "VERIFIED_100_PERCENT_SAFE")
        self.assertTrue(report["issuance_authorized"])

        # Test validator integration
        vaccine_pkg = self.generator.generate_vaccine("RCE_VULN", "user_input")
        val_res = self.validator.validate_vaccine_on_bateau_test(vaccine_pkg)
        self.assertTrue(val_res["passed"])
        self.assertEqual(val_res["ast_validation"], "PASSED")
        self.assertEqual(val_res["security_scan"], "PASSED")
        self.assertTrue(val_res["bateau_test_reset"]["clean"])

    def test_automatic_rollback_on_post_deployment_anomaly(self):
        """
        Test automatic rollback of an approved vaccine if high CPU/error rates occur post-deployment.
        """
        rollback_triggered = self.validator.rollback_vaccine_on_anomaly("VACC-2026-001", {"cpu_usage_percent": 92})
        self.assertTrue(rollback_triggered["rollback_executed"])
        self.assertEqual(rollback_triggered["status"], "ROLLED_BACK_AUTOMATICALLY")

        rollback_normal = self.validator.rollback_vaccine_on_anomaly("VACC-2026-001", {"cpu_usage_percent": 12})
        self.assertFalse(rollback_normal["rollback_executed"])
        self.assertEqual(rollback_normal["status"], "STABLE")


if __name__ == "__main__":
    unittest.main()

    def test_post_ast_semantic_validation_crowdstrike_prevention(self):
        """
        Validation sémantique et effets secondaires applicatifs (Incohérence de paramètres / CrowdStrike) :
        Vérification qu'un vaccin valide en forme ne contient pas d'incohérence provoquant un crash mémoire noyau.
        """
        valid_pkg = {"code_patch": "def patch(): pass", "ebpf_rule": {"stack_size_bytes": 128}}
        sem_res = self.validator.validate_semantic_side_effects(valid_pkg)
        self.assertEqual(sem_res["status"], "SEMANTIC_VALIDATION_PASSED")
        self.assertTrue(sem_res["semantic_check_passed"])
        self.assertTrue(sem_res["crowdstrike_style_incident_prevented"])

        # Test invalid memory parameter
        bad_pkg = {"code_patch": "ptr = 0xFFFFFFFF", "ebpf_rule": {"stack_size_bytes": 1024}}
        bad_sem = self.validator.validate_semantic_side_effects(bad_pkg)
        self.assertEqual(bad_sem["status"], "SEMANTIC_INCONSISTENCY_REJECTED")
        self.assertFalse(bad_sem["semantic_check_passed"])
        self.assertTrue(bad_sem["crowdstrike_style_incident_prevented"])

    def test_canary_deployment_progressive_clusters(self):
        """
        Tests A/B et déploiement progressif en grappes (Canary Deployment) :
        Application du vaccin sur un échantillon restreint avant généralisation.
        """
        nodes = [f"srv-prod-{i:02d}" for i in range(1, 21)]
        canary_res = self.validator.execute_canary_deployment("VACC-2026-001", nodes, canary_sample_percent=10.0)
        self.assertEqual(canary_res["status"], "CANARY_PHASE_ACTIVE")
        self.assertEqual(len(canary_res["canary_nodes"]), 2)
        self.assertEqual(len(canary_res["remaining_nodes_queued"]), 18)
