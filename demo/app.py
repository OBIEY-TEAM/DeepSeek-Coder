"""
CYBERSOCLE — Vitrine Web & Démonstrateur Interactif
Dossier CADEV 2026 · Powered by Systalink Cloud
"""

import os
from collections.abc import Iterator
from threading import Thread

import gradio as gr

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import spaces
    has_spaces = True
except ImportError:
    has_spaces = False
    class spaces:
        @staticmethod
        def GPU(fn):
            return fn

MODEL_ID = os.getenv("MODEL_ID", "deepseek-ai/deepseek-coder-6.7b-instruct")

# Enforce DeepSeek-Coder V1 models restriction
if "v2" in MODEL_ID.lower() or "v3" in MODEL_ID.lower() or "r1" in MODEL_ID.lower():
    raise ValueError("Usage of DeepSeek V2, V3 or R1 models is strictly prohibited. Only V1 models are allowed.")


def run_ssh_attack_simulation(attacker_ip: str, target_port: int) -> tuple[str, str, str, str]:
    """
    Simulates a 5-level eBPF quarantine and ZKP vaccine generation process.
    """
    quarantine_logs = f"""\
[eBPF FALCO ALERT] Intrusion SSH détectée depuis IP: {attacker_ip}:{target_port}
[NIVEAU 1 - IAM/TPM] Connexion non authentifiée via clé TPM. Basculement furtif activé.
[NIVEAU 2 - QUARANTINE eBPF] Attaquant routé vers conteneur leurre PID 4821 (PRISON).
[CANARY TOKEN TRIGGERED] Masque pirate isolé dans la cage eBPF (Cilium Kernel Filter).
[MERKLE LEDGER] Block Hash #88492019 immutablement scellé.
"""

    prod_logs = """\
[NIVEAU 1 - PRODUCTION] Service Web & SGBD Officiels intacts (0% d'impact).
[ISOLATION TOTALE] Aucun droit de privilège ni lien réseau descendant accordé à l'intrus.
[SLA STATUS] Uptime 100.0% — Aucun ralentissement CPU/Mémoire sur conteneur de production.
"""

    vaccine_status = f"""\
⚡ SYNTHÈSE DU VACCIN PAR LA TOUR À 5 NIVEAUX :
1. NIVEAU 3 (Moteur LLM STIX 2.1) : Extraction de 4 Cybercards d'attaque depuis IP {attacker_ip}.
2. NIVEAU 4 (Vector Lab Qdrant) : Recherche par embeddings vectoriels des contre-mesures.
3. NIVEAU 5 (Banc d'Essai AST/Bandit) : Qualification syntaxique AST Python & Scan Bandit PASSED (100% Succès).
4. VPS LAB (Systalink Cloud) : Propagation du vaccin anonymisé via Preuves ZKP en 12.4 secondes !
"""

    result_banner = "✅ Réseau immunisé avec succès en 12.4 secondes ! Tous les serveurs du réseau Systalink sont désormais vaccinés."

    return quarantine_logs, prod_logs, vaccine_status, result_banner


# Header Markdown Content
HERO_MARKDOWN = """\
<div style="text-align: center; padding: 1rem 0;">
    <span class="cybersocle-badge">Powered by Systalink Cloud · CADev 2026</span>
    <div class="suntzu-quote">« Pour vaincre votre ennemi, vous devez d'abord le comprendre. » — Sun Tzu</div>
    <h1 class="cybersocle-h1">CYBERSOCLE — L'immunité collective par la tour de sécurité à 5 niveaux</h1>
    <p style="font-size: 1.1rem; color: #94A3B8; max-width: 800px; margin: 0 auto 1.5rem auto;">
        Plateforme SOC souveraine. Détection et quarantaine eBPF en temps réel. Renseignement sur les menaces au format STIX 2.1. Aligné sur la Convention de Malabo de l'Union africaine et sur ISO 27001.
    </p>
    <div style="display: flex; gap: 1rem; justify-content: center; margin-bottom: 2rem;">
        <a href="https://wa.me/242066130118" target="_blank" class="whatsapp-link">
            💬 Contact WhatsApp Direct : +242 06 613 01 18
        </a>
    </div>
</div>
"""

TOUR_GRID_MARKDOWN = """\
### 🛡️ Architecture de la Tour de Sécurité à 5 Niveaux

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
    <div class="tour-card tour-level-1">
        <h4 style="color: #0066FF; margin-top: 0;">Niveau 1 — Étage Officiel (IAM & TPM)</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Production sécurisée avec attestation TPM 2.0 et authentification SSH Zero-Trust. Vos collaborateurs travaillent en toute sérénité.</p>
    </div>
    <div class="tour-card tour-level-2">
        <h4 style="color: #FF3366; margin-top: 0;">Niveau 2 — Étage Quarantaine (eBPF & Leurres)</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Piégeage et routage noyau eBPF Falco / Cilium vers conteneur leurre avec Canary Tokens et registre Merkle.</p>
    </div>
    <div class="tour-card tour-level-3">
        <h4 style="color: #00F0FF; margin-top: 0;">Niveau 3 — Centre IA STIX 2.1 (LLM Offline)</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Décomposition comportementale 100% hors-ligne en 4 Cybercards structurées au format international OASIS STIX 2.1.</p>
    </div>
    <div class="tour-card tour-level-4">
        <h4 style="color: #a855f7; margin-top: 0;">Niveau 4 — Laboratoire R&D (Qdrant Vector)</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Base vectorielle Qdrant analysant les motifs par embeddings vectoriels pour façonner le vaccin sur mesure.</p>
    </div>
    <div class="tour-card tour-level-5">
        <h4 style="color: #00FF88; margin-top: 0;">Niveau 5 — Banc d'Essai (Qualification Formelle)</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Validation formelle par analyse AST Python et scanner de vulnérabilités Bandit avant tout déploiement.</p>
    </div>
    <div class="tour-card tour-vps-lab">
        <h4 style="color: #D4AF37; margin-top: 0;">VPS LAB — Orchestration ZKP & Immunité</h4>
        <p style="font-size: 0.9rem; color: #CBD5E1;">Distribution souveraine des vaccins anonymisés via preuves à connaissance nulle (ZKP) en moins de 30s sur Systalink Cloud.</p>
    </div>
</div>
"""

PRICING_MARKDOWN = """\
### 📊 Modèle Économique & Offres SaaS B2B

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
    <div class="pricing-card">
        <h3 style="color: #F8FAFC; margin-top:0;">Offre PME</h3>
        <p style="color: #94A3B8; font-size: 0.85rem;">Petites et moyennes entreprises</p>
        <div class="pricing-price">180 000 FCFA <span style="font-size: 0.9rem; color: #94A3B8;">/ mois</span></div>
        <p style="font-size: 0.85rem; color: #CBD5E1;">Protection 5 Niveaux · Support Standard · Cloud Souverain Systalink</p>
    </div>
    <div class="pricing-card featured">
        <span style="background: #D4AF37; color: #0B0F19; font-weight:700; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.75rem;">RECOMMANDÉ ETI</span>
        <h3 style="color: #F8FAFC; margin-top:0.5rem;">Offre ETI</h3>
        <p style="color: #94A3B8; font-size: 0.85rem;">Entreprises de taille intermédiaire</p>
        <div class="pricing-price">800 000 FCFA <span style="font-size: 0.9rem; color: #94A3B8;">/ mois</span></div>
        <p style="font-size: 0.85rem; color: #CBD5E1;">Protection Haute Disponibilité · Vaccine Engine ZKP · SLA 99.9%</p>
    </div>
    <div class="pricing-card">
        <h3 style="color: #F8FAFC; margin-top:0;">Grands Comptes</h3>
        <p style="color: #94A3B8; font-size: 0.85rem;">Banques, Télécoms, Organismes d'État</p>
        <div class="pricing-price">2 500 000 FCFA <span style="font-size: 0.9rem; color: #94A3B8;">/ mois</span></div>
        <p style="font-size: 0.85rem; color: #CBD5E1;">Infrastructure Dédiée · SOC Souverain 24/7 · Audit Sur-Mesure</p>
    </div>
</div>
<p style="text-align: center; font-size: 0.9rem; color: #94A3B8; margin-top: 1.5rem;">
    📈 <strong>Métriques Financières Key</strong> : Marge brute &gt; 75% · Seuil de rentabilité au 19e mois · ARR 1.8M$ Année 3.
</p>
"""

FAQ_MARKDOWN = """\
### ❓ FAQ — Questions du Jury (CADev 2026)

#### Q1. Comment garantissez-vous qu'un attaquant piégé au Niveau 2 ne puisse pas s'évader vers le Niveau 1 ?
**Réponse :** L'étanchéité repose sur la micro-segmentation eBPF au niveau du noyau Linux. L'accès SSH officiel bascule l'attaquant de manière transparente vers le conteneur leurre (Niveau 2), surveillé en continu par eBPF Falco avec vérification par arbre de Merkle. Aucun privilège ni lien réseau descendant ne pointe vers les conteneurs de production.

#### Q2. Comment l'IA du Niveau 3 produit-elle une analyse sans exfiltrer de données ?
**Réponse :** L'IA repose sur un moteur LLM local 100% hors-ligne (en lecture seule), garantissant la souveraineté totale des données. La télémétrie est convertie en 4 Cybercards structurées selon la norme internationale OASIS STIX 2.1.

#### Q3. Qu'est-ce qu'un vaccin informatique et comment évite-t-on les faux positifs ?
**Réponse :** Le vaccin est un jeu de règles de neutralisation eBPF/Cilium et signatures comportementales. Au Niveau 5 (Banc d'Essai), il subit une qualification formelle (analyse syntaxique AST Python, scan de vulnérabilités Bandit, test d'innocuité). Rien n'est déployé sans qualification 100% positive.

#### Q4. Comment partagez-vous les vaccins sans révéler la topologie de la victime initiale ?
**Réponse :** Le VPS LAB central anonymise tous les vaccins à l'aide de preuves à connaissance nulle (ZKP - Zero-Knowledge Proofs). L'immunité est distribuée sans jamais exposer la provenance ni les IP d'origine.
"""

FOOTER_MARKDOWN = """\
<div style="border-top: 1px solid rgba(51, 65, 85, 0.8); padding-top: 1.5rem; margin-top: 2.5rem; text-align: center; color: #64748B; font-size: 0.85rem;">
    <p>CYBERSOCLE © 2026 — Dossier CADEV 2026 · Powered by Systalink Cloud</p>
    <p>Mentions légales conformes aux référentiels OHADA, ACN et ARTCI. Alignment ISO 27001 et PCI-DSS.</p>
    <p>WhatsApp Support : <a href="https://wa.me/242066130118" style="color: #00F0FF;">+242 06 613 01 18</a> | Email : support@cybersocle.studio</p>
</div>
"""


with gr.Blocks(title="CYBERSOCLE — Vitrine CADEV 2026") as demo:
    gr.HTML(HERO_MARKDOWN)

    with gr.Tabs():
        with gr.TabItem("🧪 Démonstration Interactive (Simulation Attaque)"):
            gr.Markdown("### ⚡ Simulation d'Attaque SSH & Quarantine eBPF en Direct")
            gr.Markdown("Testez le parcours de l'immunité collective : déclenchez une attaque SSH simulée pour observer le piégeage eBPF Niveau 2 et la génération du vaccin STIX 2.1 / ZKP.")

            with gr.Row():
                attacker_ip_input = gr.Textbox(value="192.168.45.102", label="IP de l'Attaquant Simulée")
                target_port_input = gr.Number(value=22, label="Port SSH")

            sim_button = gr.Button("🚀 Lancer la simulation d'attaque SSH", elem_classes=["btn-primary-gradient"])

            banner_output = gr.Markdown()

            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 🔴 ÉTAGE QUARANTAINE (Niveau 2 eBPF)")
                    quarantine_box = gr.Code(label="Logs Falco & Cage eBPF (Leurre PRISON)", language="json", elem_classes=["code-logs"])
                with gr.Column():
                    gr.Markdown("#### 🟢 ÉTAGE PRODUCTION (Niveau 1 Officiel)")
                    prod_box = gr.Code(label="Statut du Serveur de Production", language="json", elem_classes=["code-logs"])

            vaccine_box = gr.Code(label="Synthèse du Vaccin Informatique (Niveaux 3, 4, 5 & VPS LAB)", language="markdown", elem_classes=["code-logs"])

            sim_button.click(
                fn=run_ssh_attack_simulation,
                inputs=[attacker_ip_input, target_port_input],
                outputs=[quarantine_box, prod_box, vaccine_box, banner_output]
            )

        with gr.TabItem("🏰 La Tour à 5 Niveaux"):
            gr.HTML(TOUR_GRID_MARKDOWN)

        with gr.TabItem("💼 Modèle Économique & Tarifs"):
            gr.HTML(PRICING_MARKDOWN)

        with gr.TabItem("📖 FAQ & Jury CADEV 2026"):
            gr.HTML(FAQ_MARKDOWN)

    gr.HTML(FOOTER_MARKDOWN)

if __name__ == "__main__":
    demo.queue().launch(share=False)
