import os
from collections.abc import Iterator
from threading import Thread
from unittest.mock import MagicMock

try:
    import gradio as gr
except ImportError:
    gr = MagicMock()

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
except ImportError:
    torch = MagicMock()
    AutoModelForCausalLM = MagicMock()
    AutoTokenizer = MagicMock()
    TextIteratorStreamer = MagicMock()

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

MAX_MAX_NEW_TOKENS = 2048
DEFAULT_MAX_NEW_TOKENS = 1024
MAX_INPUT_TOKEN_LENGTH = int(os.getenv("MAX_INPUT_TOKEN_LENGTH", "4096"))

TRANSLATIONS = {
    "fr": {
        "title": "CYBERSOCLE - Démo Interactive & Assistant Cyber-Cartographie",
        "subtitle": "### Architecture Microsegmentée, Fausse Boîte (Deception) et LLM Offline",
        "description": "Bienvenue sur l'interface démonstrative CYBERSOCLE. Sélectionnez votre langue et vos préférences vocales pour explorer le système.",
        "lang_label": "🌐 Choisir la langue / Choose language",
        "voice_label": "🎙️ Option Vocale (Synthetiseur Vocale)",
        "voice_options": ["Français - Voix Studio Sécurisée (Féminin)", "Français - Voix Tactique Ops (Masculin)", "Désactivé"],
        "system_prompt_label": "System Prompt (Consignes Agent/LLM)",
        "system_prompt_value": "Tu es un assistant expert en cybersécurité et microsegmentation CYBERSOCLE. Réponds en français avec précision technique.",
        "max_tokens_label": "Nombre max de nouveaux tokens",
        "top_p_label": "Top-p (échantillonnage noyau)",
        "top_k_label": "Top-k",
        "rep_penalty_label": "Pénalité de répétition",
        "submit_btn": "🚀 Envoyer le message",
        "clear_btn": "🗑️ Effacer l'historique",
        "undo_btn": "↩️ Annuler le dernier",
        "retry_btn": "🔄 Réessayer",
        "duplicate_btn": "📋 Dupliquer l'Espace",
        "security_tour_title": "🛡️ Parcours de Sécurité (5 Niveaux)",
        "security_tour_text": """\
1. **Bateau OFFICIEL** : Microsegmentation VLAN & Conteneurs immuables en lecture seule.
2. **Authentification Deception** : Mike-Vrai dirigé vers la production, Mike-Faux isolé dans le Bateau PRISON avec fausse base de données.
3. **Logging Sidecar eBPF** : Espion Falco non-intrusif & Registre Merkle à tuyau unidirectionnel.
4. **LLM Offline STIX 2.1** : Génération de Cybercards signées SHA256 sans connexion internet.
5. **Bateau SCIENCE & TEST** : Moteur de vaccins et validation humaine par l'Admin Sécurité.
""",
        "pricing_title": "💰 Grille Tarifaire FCFA & Offres Enterprise",
        "pricing_text": """\
- **Starter VPS** : 250 000 FCFA / mois (Jusqu'à 5 conteneurs durcis + Sidecar Falco)
- **Business Shield** : 750 000 FCFA / mois (15 conteneurs + Honeypot Deception + Offline LLM)
- **Enterprise Sovereign** : 2 000 000 FCFA / mois (Support LAB VPS illimité + Vaccins inter-entreprises)
""",
        "faq_title": "⚖️ CADEV 2026 Jury FAQ & Conformité",
        "faq_text": """\
- **Q : Comment est garantie l'isolation contre les virus ?**
  *R : Via Namespaces, Cgroups (limite 2GB RAM), Firecracker et montage filesystem read-only.*
- **Q : Comment fonctionne la bascule Mike-Vrai vs Mike-Faux ?**
  *R : La vérification de clé RSA/TPM redirige les attaquants vers Bateau PRISON sans alerte suspecte.*
""",
        "examples": [
            "Explique comment CYBERSOCLE isole une cellule infectée vers le Bateau PRISON.",
            "Génère une règle eBPF Cilium pour bloquer un reverse shell.",
            "Quelles sont les différences de clés entre Mike-Vrai et Mike-Faux ?"
        ]
    },
    "en": {
        "title": "CYBERSOCLE - Interactive Demo & Cyber-Cartography Assistant",
        "subtitle": "### Microsegmented Architecture, Honeypot Deception & Offline LLM",
        "description": "Welcome to the CYBERSOCLE showcase interface. Select your language and voice preferences to explore the system.",
        "lang_label": "🌐 Choose language / Choisir la langue",
        "voice_label": "🎙️ Voice Option (Voice Synthesizer)",
        "voice_options": ["English - Secure Studio Voice (Female)", "English - Tactical Ops Voice (Male)", "Disabled"],
        "system_prompt_label": "System Prompt (Agent/LLM Instructions)",
        "system_prompt_value": "You are an expert cybersecurity and microsegmentation assistant for CYBERSOCLE. Answer in English with technical accuracy.",
        "max_tokens_label": "Max new tokens",
        "top_p_label": "Top-p (nucleus sampling)",
        "top_k_label": "Top-k",
        "rep_penalty_label": "Repetition penalty",
        "submit_btn": "🚀 Send message",
        "clear_btn": "🗑️ Clear history",
        "undo_btn": "↩️ Undo last",
        "retry_btn": "🔄 Retry",
        "duplicate_btn": "📋 Duplicate Space",
        "security_tour_title": "🛡️ Security Tour (5 Levels)",
        "security_tour_text": """\
1. **OFFICIAL Boat**: VLAN microsegmentation & read-only immutable containers.
2. **Deception Auth**: Real-Mike routed to production, Fake-Mike isolated in PRISON Boat with fake DB.
3. **eBPF Sidecar Logging**: Non-intrusive Falco spy & Merkle ledger with one-way pipe.
4. **Offline LLM STIX 2.1**: SHA256-signed Cybercard generation without internet access.
5. **SCIENCE & TEST Boats**: Vaccine engine & Human-in-the-loop validation by Security Admin.
""",
        "pricing_title": "💰 Pricing Tiers (FCFA) & Enterprise Plans",
        "pricing_text": """\
- **Starter VPS**: 250,000 FCFA / month (Up to 5 hardened containers + Falco Sidecar)
- **Business Shield**: 750,000 FCFA / month (15 containers + Deception Honeypot + Offline LLM)
- **Enterprise Sovereign**: 2,000,000 FCFA / month (Unlimited LAB VPS support + Inter-enterprise vaccines)
""",
        "faq_title": "⚖️ CADEV 2026 Jury FAQ & Compliance",
        "faq_text": """\
- **Q: How is virus isolation guaranteed?**
  *A: Via Namespaces, Cgroups (2GB RAM limit), Firecracker, and read-only filesystem mounts.*
- **Q: How does Real-Mike vs Fake-Mike switching work?**
  *A: RSA/TPM key validation redirects attackers to the PRISON Boat without triggering suspicion.*
""",
        "examples": [
            "Explain how CYBERSOCLE isolates an infected cell to the PRISON Boat.",
            "Generate a Cilium eBPF rule to block a reverse shell.",
            "What are the key differences between Real-Mike and Fake-Mike?"
        ]
    }
}

def get_device():
    if hasattr(torch, "cuda") and torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch, "backends") and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"

device = get_device()

model = None
tokenizer = None

def load_model_and_tokenizer():
    global model, tokenizer
    if model is not None and tokenizer is not None:
        return
    print(f"Loading model {MODEL_ID} on device {device}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    tokenizer.use_default_system_prompt = False

    torch_dtype = getattr(torch, "bfloat16", None) if device == "cuda" else getattr(torch, "float32", None)
    device_map = "auto" if device == "cuda" else None

    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch_dtype,
            device_map=device_map,
            trust_remote_code=True
        )
        if device_map is None and hasattr(model, "to"):
            model = model.to(device)
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@spaces.GPU
def generate(
    message: str,
    chat_history: list,
    system_prompt: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.6,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1.0,
) -> Iterator[str]:
    load_model_and_tokenizer()
    if model is None or tokenizer is None:
        yield "Model is not loaded. Please verify configuration and server memory."
        return

    conversation = []
    if system_prompt:
        conversation.append({"role": "system", "content": system_prompt})
    for user, assistant in chat_history:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    conversation.append({"role": "user", "content": message})

    try:
        input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt", add_generation_prompt=True)
        if input_ids.shape[1] > MAX_INPUT_TOKEN_LENGTH:
            input_ids = input_ids[:, -MAX_INPUT_TOKEN_LENGTH:]
            gr.Warning(f"Trimmed input from conversation as it was longer than {MAX_INPUT_TOKEN_LENGTH} tokens.")
        input_ids = input_ids.to(model.device)

        streamer = TextIteratorStreamer(tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)
        generate_kwargs = {
            "input_ids": input_ids,
            "streamer": streamer,
            "max_new_tokens": max_new_tokens,
            "do_sample": temperature > 0,
            "temperature": temperature if temperature > 0 else None,
            "top_p": top_p if temperature > 0 else None,
            "top_k": top_k if temperature > 0 else None,
            "num_beams": 1,
            "repetition_penalty": repetition_penalty,
            "eos_token_id": tokenizer.eos_token_id
        }
        generate_kwargs = {k: v for k, v in generate_kwargs.items() if v is not None}

        t = Thread(target=model.generate, kwargs=generate_kwargs)
        t.start()

        outputs = []
        for text in streamer:
            outputs.append(text)
            yield "".join(outputs).replace("<|EOT|>", "")

    except Exception as e:
        yield f"Generation error: {e!s}"


def switch_language(
    lang_choice: str,
    curr_max_tokens: int = DEFAULT_MAX_NEW_TOKENS,
    curr_top_p: float = 0.9,
    curr_top_k: int = 50,
    curr_rep_penalty: float = 1.0
):
    lang_key = "fr" if "Français" in lang_choice else "en"
    t = TRANSLATIONS[lang_key]

    header_md = f"# {t['title']}\n{t['subtitle']}\n\n{t['description']}"

    update_fn = getattr(gr, "update", None)
    if update_fn is callable:
        return (
            header_md,
            update_fn(label=t["voice_label"], choices=t["voice_options"], value=t["voice_options"][0]),
            update_fn(label=t["system_prompt_label"], value=t["system_prompt_value"]),
            update_fn(label=t["max_tokens_label"], value=curr_max_tokens),
            update_fn(label=t["top_p_label"], value=curr_top_p),
            update_fn(label=t["top_k_label"], value=curr_top_k),
            update_fn(label=t["rep_penalty_label"], value=curr_rep_penalty),
            t["security_tour_title"] + "\n" + t["security_tour_text"],
            t["pricing_title"] + "\n" + t["pricing_text"],
            t["faq_title"] + "\n" + t["faq_text"],
            update_fn(value=t["submit_btn"]),
            update_fn(value=t["clear_btn"]),
            update_fn(value=t["undo_btn"]),
            update_fn(value=t["retry_btn"]),
        )

    return (
        header_md,
        gr.Radio(label=t["voice_label"], choices=t["voice_options"], value=t["voice_options"][0]),
        gr.Textbox(label=t["system_prompt_label"], value=t["system_prompt_value"]),
        gr.Slider(label=t["max_tokens_label"], minimum=1, maximum=MAX_MAX_NEW_TOKENS, step=1, value=curr_max_tokens),
        gr.Slider(label=t["top_p_label"], minimum=0.05, maximum=1.0, step=0.05, value=curr_top_p),
        gr.Slider(label=t["top_k_label"], minimum=1, maximum=1000, step=1, value=curr_top_k),
        gr.Slider(label=t["rep_penalty_label"], minimum=1.0, maximum=2.0, step=0.05, value=curr_rep_penalty),
        t["security_tour_title"] + "\n" + t["security_tour_text"],
        t["pricing_title"] + "\n" + t["pricing_text"],
        t["faq_title"] + "\n" + t["faq_text"],
        gr.Button(value=t["submit_btn"]),
        gr.Button(value=t["clear_btn"]),
        gr.Button(value=t["undo_btn"]),
        gr.Button(value=t["retry_btn"]),
    )


style_path = os.path.join(os.path.dirname(__file__), "style.css")
css_content = ""
if os.path.exists(style_path):
    with open(style_path, encoding="utf-8") as f:
        css_content = f.read()

with gr.Blocks(title="CYBERSOCLE", css=css_content) as demo:
    default_lang = "fr"
    t_def = TRANSLATIONS[default_lang]

    with gr.Row(elem_classes=["lang-voice-bar"]):
        lang_selector = gr.Radio(
            choices=["Français 🇫🇷", "English 🇬🇧"],
            value="Français 🇫🇷",
            label=t_def["lang_label"],
            interactive=True,
            elem_id="lang_selector"
        )
        voice_selector = gr.Radio(
            choices=t_def["voice_options"],
            value=t_def["voice_options"][0],
            label=t_def["voice_label"],
            interactive=True,
            elem_id="voice_selector"
        )

    header_markdown = gr.Markdown(
        f"# {t_def['title']}\n{t_def['subtitle']}\n\n{t_def['description']}",
        elem_id="header_markdown"
    )

    with gr.Row(elem_classes=["main-grid"]):
        with gr.Column(scale=3, elem_classes=["chat-column"]):
            chatbot = gr.Chatbot(height=450)
            msg_input = gr.Textbox(
                placeholder="Tapez votre message ici... / Type your message here...",
                show_label=False,
                container=False
            )
            with gr.Row(elem_classes=["btn-group"]):
                submit_btn = gr.Button(t_def["submit_btn"], variant="primary")
                clear_btn = gr.Button(t_def["clear_btn"])
                undo_btn = gr.Button(t_def["undo_btn"])
                retry_btn = gr.Button(t_def["retry_btn"])

        with gr.Column(scale=2, elem_classes=["params-column"]):
            sys_prompt_box = gr.Textbox(
                label=t_def["system_prompt_label"],
                value=t_def["system_prompt_value"],
                lines=4
            )
            max_tokens_slider = gr.Slider(
                label=t_def["max_tokens_label"],
                minimum=1,
                maximum=MAX_MAX_NEW_TOKENS,
                step=1,
                value=DEFAULT_MAX_NEW_TOKENS,
            )
            top_p_slider = gr.Slider(
                label=t_def["top_p_label"],
                minimum=0.05,
                maximum=1.0,
                step=0.05,
                value=0.9,
            )
            top_k_slider = gr.Slider(
                label=t_def["top_k_label"],
                minimum=1,
                maximum=1000,
                step=1,
                value=50,
            )
            rep_penalty_slider = gr.Slider(
                label=t_def["rep_penalty_label"],
                minimum=1.0,
                maximum=2.0,
                step=0.05,
                value=1.0,
            )

    with gr.Row(elem_classes=["info-cards-row"]):
        tour_box = gr.Markdown(
            t_def["security_tour_title"] + "\n" + t_def["security_tour_text"],
            elem_classes=["info-card"]
        )
        pricing_box = gr.Markdown(
            t_def["pricing_title"] + "\n" + t_def["pricing_text"],
            elem_classes=["info-card"]
        )
        faq_box = gr.Markdown(
            t_def["faq_title"] + "\n" + t_def["faq_text"],
            elem_classes=["info-card"]
        )

    # Chat interaction logic
    def user_chat_step(user_message, history):
        return "", history + [[user_message, None]]

    def bot_chat_step(history, sys_prompt, max_tokens, top_p, top_k, rep_penalty):
        if not history:
            yield history
            return
        user_message = history[-1][0]
        chat_hist = history[:-1]

        chat_hist_tuples = [(h[0], h[1]) for h in chat_hist if h[1] is not None]

        generator = generate(
            message=user_message,
            chat_history=chat_hist_tuples,
            system_prompt=sys_prompt,
            max_new_tokens=max_tokens,
            temperature=0.6,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=rep_penalty
        )
        for bot_response in generator:
            history[-1][1] = bot_response
            yield history

    def undo_last_chat(history):
        if history:
            history.pop()
        return history

    def retry_last_chat(history, sys_prompt, max_tokens, top_p, top_k, rep_penalty):
        if not history:
            yield history
            return
        history[-1][1] = None
        yield from bot_chat_step(history, sys_prompt, max_tokens, top_p, top_k, rep_penalty)

    msg_input.submit(
        user_chat_step, [msg_input, chatbot], [msg_input, chatbot], queue=False
    ).then(
        bot_chat_step,
        [chatbot, sys_prompt_box, max_tokens_slider, top_p_slider, top_k_slider, rep_penalty_slider],
        chatbot
    )

    submit_btn.click(
        user_chat_step, [msg_input, chatbot], [msg_input, chatbot], queue=False
    ).then(
        bot_chat_step,
        [chatbot, sys_prompt_box, max_tokens_slider, top_p_slider, top_k_slider, rep_penalty_slider],
        chatbot
    )

    clear_btn.click(list, None, chatbot, queue=False)
    undo_btn.click(undo_last_chat, chatbot, chatbot, queue=False)
    retry_btn.click(
        retry_last_chat,
        [chatbot, sys_prompt_box, max_tokens_slider, top_p_slider, top_k_slider, rep_penalty_slider],
        chatbot
    )

    lang_selector.change(
        fn=switch_language,
        inputs=[lang_selector, max_tokens_slider, top_p_slider, top_k_slider, rep_penalty_slider],
        outputs=[
            header_markdown,
            voice_selector,
            sys_prompt_box,
            max_tokens_slider,
            top_p_slider,
            top_k_slider,
            rep_penalty_slider,
            tour_box,
            pricing_box,
            faq_box,
            submit_btn,
            clear_btn,
            undo_btn,
            retry_btn
        ]
    )

if __name__ == "__main__":
    demo.queue().launch(share=False)
