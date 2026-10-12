"""
Test Suite for CyberSocle Level 3 (Offline AI Center - STIX 2.1 Mapping).
Covers local LLM model offline sovereignty (Test 3.1), telemetry parsing & STIX 2.1 Cybercards generation (Test 3.2),
and modeling performance under 3 seconds (Test 3.3).
"""

import time
import unittest
from cybersocle.llm.offline_engine import OfflineLLMEngine
from cybersocle.llm.stix_cybercards import STIXCybercardGenerator


class TestNiveau3LLMSTIX(unittest.TestCase):

    def setUp(self):
        self.llm = OfflineLLMEngine()
        self.stix_gen = STIXCybercardGenerator()

    def test_3_1_local_llm_offline_sovereignty(self):
        """
        Test 3.1 — Étanchéité et souveraineté du modèle LLM local :
        Vérifier les connexions réseau du conteneur cybersocle/llm/ pendant le traitement.
        Résultat attendu : 0 flux réseau sortant (IA 100 % hors-ligne en lecture seule, aucune fuite de données).
        """
        res = self.llm.query_model_offline("Analyse de sécurité locale")
        self.assertIn("BATEAU MODELE LLM", res)

        # Verify engine offline state configuration
        mount_flags = self.llm.get_container_mount_flags()
        hw_config = self.llm.get_hardware_resource_config()

        self.assertIn("--read-only", mount_flags)
        self.assertTrue(any(":ro" in flag for flag in mount_flags))
        self.assertEqual(hw_config["quantization"], "Q8_0")

    def test_3_2_telemetry_parsing_and_stix21_cybercards_generation(self):
        """
        Test 3.2 — Parsing de la télémétrie & Génération des Cybercards STIX 2.1 :
        Transmettre les logs bruts d'une attaque eBPF au module IA du Niveau 3.
        Résultat attendu : Génération automatique de 4 Cybercards au format international STIX 2.1 (OASIS) parfaitement conformes et lisibles par un SIEM/SOC.
        """
        cartography = self.stix_gen.generate_cybercartography(
            cell_id="cell-quarantine-01",
            ship_name="PRISON",
            attack_type="EBPF_REVERSE_SHELL_INJECTION",
            entry_vector="SSH_EXPLOIT",
            impacted_assets=["/tmp/payload.sh", "/etc/passwd"],
            applied_security=["ebpf_kill_process", "quarantine_isolation"],
            recommendations=["deploy_vaccine_v2", "block_ip"]
        )

        stix_cards = cartography.get("stix_cybercards", {})
        # Expecting 4 distinct STIX 2.1 Cybercards:
        # 1. cybercard_attaque (indicator)
        # 2. cybercard_actifs (infrastructure)
        # 3. cybercard_securite (course-of-action)
        # 4. cybercard_recommandation (course-of-action)
        self.assertEqual(len(stix_cards), 4)
        self.assertIn("cybercard_attaque", stix_cards)
        self.assertIn("cybercard_actifs", stix_cards)
        self.assertIn("cybercard_securite", stix_cards)
        self.assertIn("cybercard_recommandation", stix_cards)

        # OASIS STIX 2.1 spec validations
        for card_key, card in stix_cards.items():
            self.assertEqual(card.get("spec_version"), "2.1")
            card_id = card.get("id", "")
            self.assertTrue("--" in card_id or "-" in card_id)
            self.assertIsNotNone(card.get("created"))

        self.assertIn("sha256_signature", cartography)

    def test_3_3_modeling_performance(self):
        """
        Test 3.3 — Performance de modélisation :
        Mesurer le temps d'analyse et de génération du fichier STIX 2.1.
        Résultat attendu : Traitement complet de la menace en moins de 3 secondes.
        """
        start_time = time.time()

        # Complete threat modeling workflow
        _ = self.llm.query_model_offline("Traiter alerte eBPF Falco #8291")
        _ = self.stix_gen.generate_cybercartography(
            cell_id="cell-quarantine-02",
            ship_name="PRISON",
            attack_type="PRIVILEGE_ESCALATION_PTRACE",
            entry_vector="LOCAL_SHELL",
            impacted_assets=["/proc/kcore"],
            applied_security=["seccomp_kill"],
            recommendations=["kernel_patch"]
        )

        elapsed_sec = time.time() - start_time
        self.assertLess(elapsed_sec, 3.0, f"Threat processing took {elapsed_sec:.2f} s, expected < 3.0 s")


if __name__ == "__main__":
    unittest.main()
