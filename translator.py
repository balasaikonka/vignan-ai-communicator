# translator.py
# Full translation pipeline:
#   1. Detect language (including Romanized)
#   2. Convert Romanized → native script
#   3. Translate to English for counselor
#   4. Translate counselor reply → parent's language in Romanized format

import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import PRIMARY_MODEL, FAST_MODEL


def _llm(fast: bool = False) -> ChatGroq:
    """Return a Groq LLM instance."""
    return ChatGroq(
        model=FAST_MODEL if fast else PRIMARY_MODEL,
        temperature=0.2,
        groq_api_key=os.environ.get("GROQ_API_KEY", ""),
        max_tokens=1024
    )


# ── Step 1: Detect Language ────────────────────────────────────────────────────
def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns a description like "Telugu", "Hindi", "Romanized Telugu", etc.
    """
    response = _llm(fast=True).invoke([HumanMessage(
        content=f"""Detect the language of this text.
If it is written in Roman/Latin script but represents a non-English language
(like Telugu, Hindi, Tamil), say "Romanized <Language>" — e.g. "Romanized Telugu".

Text: "{text}"

Reply with ONLY the language name. Examples:
English, Telugu, Hindi, Romanized Telugu, Romanized Hindi, Spanish, Tamil"""
    )])
    return response.content.strip()


# ── Step 2: Romanized → Native Script ─────────────────────────────────────────
def romanized_to_native(text: str, language: str) -> str:
    """
    Convert Romanized text into native script.
    Example: "na pillavadu" → "నా పిల్లవాడు"
    """
    response = _llm(fast=False).invoke([HumanMessage(
        content=f"""Convert this Romanized {language} text into proper {language} native script.
Return ONLY the native script. No explanation, no extra text.

Romanized text: "{text}"
{language} script:"""
    )])
    return response.content.strip()


# ── Step 3: Translate to English ──────────────────────────────────────────────
def translate_to_english(text: str, source_language: str) -> str:
    """Translate any language text to English."""
    if "english" in source_language.lower():
        return text
    response = _llm(fast=False).invoke([
        SystemMessage(content="""You are a professional translator for school communications.
Translate the message to English accurately.
Preserve the meaning, emotion and context.
Return ONLY the English translation."""),
        HumanMessage(content=f"Translate this {source_language} text to English:\n\n{text}")
    ])
    return response.content.strip()


# ── Step 4: Translate Counselor Reply → Parent Language ───────────────────────
def translate_to_romanized(text: str, target_language: str) -> str:
    """
    Translate English counselor reply to the parent's language
    and output it in Romanized (Latin script) format so the parent
    can read it even without native script fonts.

    Example: "Your child needs more practice" →
             "mee pillavadu inka practice cheyyali" (Romanized Telugu)
    """
    if target_language.lower() == "english":
        return text

    response = _llm(fast=False).invoke([
        SystemMessage(content=f"""You are a professional translator for school communications.
Translate the English message into {target_language} but write it using
Roman/Latin script (Romanized {target_language}).
This is important: do NOT use the native script — use only English/Latin letters.
Keep the tone warm and professional.
Return ONLY the Romanized {target_language} translation."""),
        HumanMessage(content=f"Translate to Romanized {target_language}:\n\n{text}")
    ])
    return response.content.strip()


# ── Full Parent Message Pipeline ──────────────────────────────────────────────
def process_parent_message(raw_text: str) -> dict:
    """
    Run the full pipeline on a parent's message:
      1. Detect language
      2. Convert Romanized → native script (if needed)
      3. Translate to English for counselor

    Returns a dict with all steps and results.
    """
    # Step 1
    detected = detect_language(raw_text)

    # Step 2
    native_text = raw_text
    base_language = detected
    if detected.lower().startswith("romanized"):
        base_language = detected.replace("Romanized", "").strip()
        native_text   = romanized_to_native(raw_text, base_language)

    # Step 3
    english_text = translate_to_english(native_text, base_language)

    return {
        "original":      raw_text,
        "detected_lang": base_language,
        "native_script": native_text,
        "english":       english_text,
        "was_romanized": detected.lower().startswith("romanized")
    }

# ── Translate to Native Script ─────────────────────────────────────────────────
def translate_to_language(text: str, target_language: str) -> str:
    """
    Translate English text into the target language using native script.
    Used for displaying answers and counselor replies in native Telugu/Hindi/Tamil etc.
    Example: "Your child needs more practice" → "మీ పిల్లవాడికి మరింత ప్రాక్టీస్ అవసరం"
    """
    if target_language.lower() == "english":
        return text

    response = _llm(fast=False).invoke([
        SystemMessage(content=f"""You are a professional translator for school communications.
Translate the English message into {target_language} using the native script of {target_language}.
Use proper {target_language} characters (not Roman/Latin letters).
Keep the tone warm and professional.
Return ONLY the translated text in {target_language} native script."""),
        HumanMessage(content=f"Translate to {target_language}:\n\n{text}")
    ])
    return response.content.strip()
