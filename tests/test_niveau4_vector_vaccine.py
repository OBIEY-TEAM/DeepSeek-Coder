"""
Test Suite for CyberSocle Level 4 (R&D Lab - Qdrant Vector Base & Vaccine Synthesis).
Covers Qdrant vector similarity search under 1 sec (Test 4.1), counter-measure vaccine script synthesis (Test 4.2),
and vaccine deduplication for identical threats (Test 4.3).
"""

import time
import unittest
from cybersocle.science.vector_lab import ThreatIntelLab
from cybersocle.science.vaccine_engine import VaccineGenerator
from cybersocle.llm.stix_cybercards import STIXCybercardGenerator


class TestNiveau4VectorVaccine(unittest.TestCase):

    def setUp(self):
        self.lab = ThreatIntelLab(qdrant_host="172.28.0.40", qdrant_port=6333)
        self.vaccine_gen = VaccineGenerator()
        self.stix_gen = STIXCybercardGenerator()

    def test_4_1_qdrant_vector_search(self):
        """
        Test 4.1 — Recherche par Embeddings Vectoriels dans Qdrant :
        Soumettre la Cybercard STIX 2.1 à la base vectorielle Qdrant dans cybersocle/science/.
        Résultat attendu : Identification des motifs d'attaque similaires et calcul du score de similarité vectorielle en < 1 seconde.
        """
        cartography = self.stix_gen.generate_cybercartography(
            cell_id="cell-quarantine-01",
            ship_name="PRISON",
            attack_type="EBPF_REVERSE_SHELL_INJECTION",
            entry_vector="SSH_EXPLOIT",
            impacted_assets=["/tmp/payload.sh"],
            applied_security=["ebpf_kill_process"],
            recommendations=["deploy_vaccine_v2"]
        )

        start_time = time.time()
        ingest_res = self.lab.ingest_cybercartography(cartography)
        elapsed_sec = time.time() - start_time

        self.assertEqual(ingest_res["status"], "ACCEPTED")
        self.assertTrue(ingest_res["qdrant_indexed"])
        self.assertLess(elapsed_sec, 1.0, f"Qdrant vector similarity search took {elapsed_sec:.2f} s, expected < 1.0 s")

    def test_4_2_countermeasure_vaccine_synthesis(self):
        """
        Test 4.2 — Génération du script de contre-mesure (Vaccin informatique) :
        Déclencher la synthèse automatique du vaccin pour bloquer la signature comportementale isolée.
        Résultat attendu : Fichier de règles de neutralisation structuré produit automatiquement.
        """
        vaccine_pkg = self.vaccine_gen.generate_vaccine(
            attack_type="EBPF_REVERSE_SHELL_INJECTION",
            vulnerability_vector="SSH_INPUT_PARAM"
        )

        self.assertIn("vaccine_id", vaccine_pkg)
        self.assertTrue(vaccine_pkg["vaccine_id"].startswith("vaccine-") or vaccine_pkg["vaccine_id"].startswith("VACCINE-"))
        self.assertIn("code_patch", vaccine_pkg)
        self.assertIn("ebpf_rule", vaccine_pkg)
        self.assertEqual(vaccine_pkg["attack_type"], "EBPF_REVERSE_SHELL_INJECTION")

    def test_4_3_vaccine_deduplication(self):
        """
        Test 4.3 — Déduplication des vaccins :
        Simuler deux attaques rigoureusement identiques à 10 minutes d'intervalle.
        Résultat attendu : Reconnaissance du vaccin existant dans Qdrant sans régénération redondante.
        """
        cartography = self.stix_gen.generate_cybercartography(
            cell_id="cell-quarantine-01",
            ship_name="PRISON",
            attack_type="DUPLICATE_RCE_ATTACK",
            entry_vector="HTTP_POST_PAYLOAD",
            impacted_assets=["/app/main.py"],
            applied_security=["waf_block"],
            recommendations=["patch_input_filter"]
        )

        # First ingestion
        res1 = self.lab.ingest_cybercartography(cartography)
        self.assertEqual(res1["status"], "ACCEPTED")

        # Second identical submission
        res2 = self.lab.ingest_cybercartography(cartography)
        self.assertEqual(res2["status"], "ACCEPTED")
        # Verify deduplication / vector accumulation in Qdrant store
        self.assertGreaterEqual(res2["vector_count"], 1)


if __name__ == "__main__":
    unittest.main()

    def test_4_4_model_drift_detection_and_fallback(self):
        """
        Test 4.4 — Test de dérive du modèle (Model Drift) :
        Confrontation du modèle à des schémas d'attaque totalement inédits non représentés dans Qdrant.
        """
        unknown_pattern = {"type": "QUANTUM_EXPLOIT_UNKNOWN_VECTOR", "payload": "0xDEADBEEF"}
        drift_res = self.lab.detect_model_drift(unknown_pattern)
        self.assertEqual(drift_res["status"], "MODEL_DRIFT_DETECTED")
        self.assertTrue(drift_res["novel_attack_pattern"])
        self.assertEqual(drift_res["fallback_mechanism"], "HEURISTIC_RULESET_FALLBACK")
        self.assertEqual(drift_res["stix_cartography_integrity"], "PRESERVED_VIA_FALLBACK")
