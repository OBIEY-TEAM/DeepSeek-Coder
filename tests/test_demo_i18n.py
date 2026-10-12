import unittest
from unittest.mock import MagicMock
import sys

# Mock torch, transformers, and spaces before importing demo.app
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()
sys.modules['spaces'] = MagicMock()

from demo.app import TRANSLATIONS, switch_language


class TestDemoI18n(unittest.TestCase):

    def test_translation_keys_exist(self):
        self.assertIn("fr", TRANSLATIONS)
        self.assertIn("en", TRANSLATIONS)

        fr = TRANSLATIONS["fr"]
        en = TRANSLATIONS["en"]

        expected_keys = [
            "title", "subtitle", "description", "lang_label", "voice_label",
            "voice_options", "system_prompt_label", "system_prompt_value",
            "max_tokens_label", "top_p_label", "top_k_label", "rep_penalty_label",
            "submit_btn", "clear_btn", "undo_btn", "retry_btn",
            "security_tour_title", "security_tour_text",
            "pricing_title", "pricing_text", "faq_title", "faq_text", "examples"
        ]

        for key in expected_keys:
            self.assertIn(key, fr, f"Missing key {key} in French translations")
            self.assertIn(key, en, f"Missing key {key} in English translations")

    def test_default_language_is_french(self):
        fr_voice_options = TRANSLATIONS["fr"]["voice_options"]
        self.assertTrue(any("Français" in opt for opt in fr_voice_options))
        self.assertIn("CYBERSOCLE", TRANSLATIONS["fr"]["title"])

    def test_switch_language_function(self):
        # Test switching to English
        res_en = switch_language("English 🇬🇧")
        self.assertEqual(len(res_en), 14)
        header_text = res_en[0]
        voice_radio = res_en[1]
        sys_prompt_box = res_en[2]
        submit_btn = res_en[10]

        self.assertIn("CYBERSOCLE - Interactive Demo", header_text)
        self.assertTrue(any("Secure Studio Voice" in str(choice) for choice in voice_radio.choices))
        self.assertIn("expert cybersecurity", sys_prompt_box.value)
        self.assertEqual(submit_btn.value, "🚀 Send message")

        # Test switching to French
        res_fr = switch_language("Français 🇫🇷")
        self.assertEqual(len(res_fr), 14)
        header_text_fr = res_fr[0]
        voice_radio_fr = res_fr[1]
        submit_btn_fr = res_fr[10]

        self.assertIn("CYBERSOCLE - Démo Interactive", header_text_fr)
        self.assertTrue(any("Voix Studio Sécurisée" in str(choice) for choice in voice_radio_fr.choices))
        self.assertEqual(submit_btn_fr.value, "🚀 Envoyer le message")


if __name__ == "__main__":
    unittest.main()
