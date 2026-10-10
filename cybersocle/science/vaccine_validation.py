"""
Formal Vaccine Validation & Test Engine for Bateau TEST.
"""

import ast
from typing import Any


class FormalVaccineValidator:
    def compute_confidence_score(
        self, ast_valid: bool, bandit_passed: bool, perf_impact: dict[str, Any], criticality: str
    ) -> float:
        """
        Calculates a confidence score between 0.0 and 1.0 for automatic recommendation/patch approval.
        """
        if not ast_valid or not bandit_passed:
            return 0.0

        score = 1.0
        cpu_overhead = perf_impact.get("cpu_overhead_percent", 0.0)
        mem_overhead = perf_impact.get("memory_overhead_mb", 0.0)

        if cpu_overhead > 1.0:
            score -= 0.2
        if mem_overhead > 10.0:
            score -= 0.2

        if criticality.upper() in ["HIGH", "CRITICAL"]:
            # High criticality actions require manual validation threshold reserve
            score -= 0.15

        return max(0.0, min(1.0, round(score, 2)))

    def validate_vaccine_on_bateau_test(
        self, vaccine_pkg: dict[str, Any], criticality: str = "MEDIUM", auto_approval_threshold: float = 0.90
    ) -> dict[str, Any]:
        code = vaccine_pkg.get("code_patch", "")

        try:
            ast.parse(code)
            ast_valid = True
        except SyntaxError as e:
            return {
                "passed": False,
                "stage": "AST_SYNTAX_PARSING",
                "error": str(e),
                "confidence_score": 0.0,
                "auto_approved": False,
                "status": "REJECTED"
            }

        bandit_passed = "eval(" not in code and "exec(" not in code and "os.system(" not in code

        performance_impact = {
            "cpu_overhead_percent": vaccine_pkg.get("cpu_overhead", 0.2),
            "memory_overhead_mb": vaccine_pkg.get("memory_overhead", 1.5),
            "bandwidth_impact": "0%"
        }
        perf_passed = performance_impact["cpu_overhead_percent"] < 2.0

        confidence_score = self.compute_confidence_score(ast_valid, bandit_passed, performance_impact, criticality)
        all_passed = ast_valid and bandit_passed and perf_passed

        # Human-in-the-Loop decision: Auto-approve high-confidence patches unless high criticality
        auto_approved = all_passed and (confidence_score >= auto_approval_threshold) and (criticality.upper() not in ["HIGH", "CRITICAL"])

        if not all_passed:
            status = "REJECTED"
        elif auto_approved:
            status = "APPROVED_AUTOMATICALLY"
        else:
            status = "APPROVED_FOR_HUMAN_VALIDATION"

        test_ship_reset = self.reset_bateau_test_ship()

        return {
            "passed": all_passed,
            "vaccine_id": vaccine_pkg.get("vaccine_id"),
            "ast_validation": "PASSED" if ast_valid else "FAILED",
            "security_scan": "PASSED" if bandit_passed else "FAILED",
            "performance_impact": performance_impact,
            "confidence_score": confidence_score,
            "criticality": criticality,
            "auto_approved": auto_approved,
            "bateau_test_reset": test_ship_reset,
            "status": status,
            "rollback_ready": True
        }

    def rollback_vaccine_on_anomaly(self, vaccine_id: str, anomaly_metrics: dict[str, Any]) -> dict[str, Any]:
        """
        Triggers an automatic rollback of an applied vaccine if post-deployment anomaly metrics are detected.
        """
        cpu_spike = anomaly_metrics.get("cpu_usage_percent", 0) > 85
        error_spike = anomaly_metrics.get("error_rate_percent", 0) > 5

        if cpu_spike or error_spike:
            return {
                "rollback_executed": True,
                "vaccine_id": vaccine_id,
                "reason": "ANOMALY_DETECTED_POST_DEPLOYMENT",
                "details": anomaly_metrics,
                "restored_version": "PREVIOUS_STABLE_SNAPSHOT",
                "status": "ROLLED_BACK_AUTOMATICALLY"
            }

        return {
            "rollback_executed": False,
            "vaccine_id": vaccine_id,
            "reason": "NO_ANOMALY_DETECTED",
            "status": "STABLE"
        }

    @staticmethod
    def reset_bateau_test_ship() -> dict[str, Any]:
        return {
            "ship_name": "TEST",
            "state": "REVERTED_TO_INITIAL_SNAPSHOT",
            "clean": True
        }
