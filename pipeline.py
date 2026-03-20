# pipeline.py
# LangGraph pipeline for the full parent message processing workflow.
#
# Every parent message travels through 5 nodes in order:
#
#   START
#     │
#     ▼
#   Node 1: detect_language   — detect language & whether it is Romanized
#     │
#     ▼
#   Node 2: convert_script    — Romanized → native script (skipped if already native)
#     │
#     ▼
#   Node 3: translate_english — translate native script → English for counselor
#     │
#     ▼
#   Node 4: analyse_sentiment — sentiment, urgency, category from English text
#     │
#     ▼
#   Node 5: generate_replies  — 3 smart reply suggestions for counselor
#     │
#     ▼
#   END  →  returns the completed State dict

import os
import json
from typing import TypedDict, Optional, List

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from config import PRIMARY_MODEL, FAST_MODEL, ALERT_KEYWORDS, SMART_REPLIES


# ── LLM helpers ───────────────────────────────────────────────────────────────
def _llm(fast: bool = False) -> ChatGroq:
    """Return a Groq ChatGroq instance. fast=True picks the smaller 8B model."""
    return ChatGroq(
        model=FAST_MODEL if fast else PRIMARY_MODEL,
        temperature=0.2,
        groq_api_key=os.environ.get("GROQ_API_KEY", ""),
        max_tokens=1024,
    )


# ── State ─────────────────────────────────────────────────────────────────────
# This TypedDict is the single object that flows through every node.
# Each node reads what it needs and adds its output to the same dict.

class ParentMessageState(TypedDict):
    # ── Input (set before graph runs) ──────────────────────────────────────────
    original_text:   str           # raw text the parent typed
    rag_context:     str           # relevant guidelines from ChromaDB (optional)

    # ── Node 1 output ──────────────────────────────────────────────────────────
    detected_lang:   str           # e.g. "Telugu", "Romanized Telugu", "Hindi"
    base_language:   str           # e.g. "Telugu" (without the "Romanized " prefix)
    was_romanized:   bool          # True if parent typed in Roman script

    # ── Node 2 output ──────────────────────────────────────────────────────────
    native_script:   str           # text in native Telugu/Hindi/Tamil script

    # ── Node 3 output ──────────────────────────────────────────────────────────
    english_text:    str           # English translation for counselor

    # ── Node 4 output ──────────────────────────────────────────────────────────
    sentiment:       str           # positive / neutral / concerned / urgent
    urgency:         str           # low / medium / high
    category:        str           # academic / behavioral / attendance / fee / general
    sentiment_reason:str           # one-sentence explanation
    is_alert:        bool          # True if dangerous keywords found

    # ── Node 5 output ──────────────────────────────────────────────────────────
    smart_replies:   List[str]     # 3 reply suggestions for counselor

    # ── Pipeline log ───────────────────────────────────────────────────────────
    steps:           List[str]     # human-readable log of completed steps


# ══════════════════════════════════════════════════════════════════════════════
# NODE 1 — Detect language
# ══════════════════════════════════════════════════════════════════════════════
def node_detect_language(state: ParentMessageState) -> ParentMessageState:
    """
    Ask Groq: what language is this text?
    Sets detected_lang, base_language, was_romanized.
    Uses the fast 8B model — quick task, no complex reasoning needed.
    """
    response = _llm(fast=True).invoke([HumanMessage(
        content=f"""Detect the language of this text.
If it uses Roman/Latin letters to write a non-English language, say "Romanized <Language>".
Examples of valid answers: English, Telugu, Hindi, Tamil, Romanized Telugu, Romanized Hindi.

Text: "{state['original_text']}"

Reply with ONLY the language name:"""
    )])

    detected = response.content.strip()
    is_roman  = detected.lower().startswith("romanized")
    base      = detected.replace("Romanized", "").strip() if is_roman else detected

    return {
        **state,
        "detected_lang": detected,
        "base_language": base,
        "was_romanized": is_roman,
        "steps":         state["steps"] + [f"✅ Node 1 — Language detected: {detected}"],
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 2 — Convert Romanized → native script
# ══════════════════════════════════════════════════════════════════════════════
def node_convert_script(state: ParentMessageState) -> ParentMessageState:
    """
    If the parent typed in Roman letters (e.g. "na pillavadu..."),
    convert to proper native script (e.g. "నా పిల్లవాడు...").
    If already in native script or English, skip conversion.
    Uses the 70B model — script conversion needs higher accuracy.
    """
    if not state["was_romanized"]:
        # Already in native script or English — nothing to convert
        return {
            **state,
            "native_script": state["original_text"],
            "steps": state["steps"] + ["✅ Node 2 — No conversion needed (already native)"],
        }

    response = _llm(fast=False).invoke([HumanMessage(
        content=f"""Convert this Romanized {state['base_language']} text to native {state['base_language']} script.
Return ONLY the native script characters. No explanation, no Latin letters.

Romanized text: "{state['original_text']}"
{state['base_language']} script:"""
    )])

    return {
        **state,
        "native_script": response.content.strip(),
        "steps": state["steps"] + [f"✅ Node 2 — Converted to native {state['base_language']} script"],
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 3 — Translate to English
# ══════════════════════════════════════════════════════════════════════════════
def node_translate_english(state: ParentMessageState) -> ParentMessageState:
    """
    Translate the native script text to English so the counselor can read it.
    If already English, skip. Uses the 70B model for quality.
    RAG context (counseling guidelines) is injected here to ensure
    the translation preserves the right tone for school communication.
    """
    if state["base_language"].lower() == "english":
        return {
            **state,
            "english_text": state["original_text"],
            "steps": state["steps"] + ["✅ Node 3 — Already English, skipped translation"],
        }

    rag_note = ""
    if state.get("rag_context"):
        rag_note = f"\n\nCounseling context (use to preserve appropriate tone):\n{state['rag_context'][:400]}"

    response = _llm(fast=False).invoke([
        SystemMessage(content=f"""You are a professional translator for school counselor-parent communications.
Translate the message to English accurately.
Preserve the meaning, emotion, and context.
Return ONLY the English translation.{rag_note}"""),
        HumanMessage(content=f"Translate this {state['base_language']} text to English:\n\n{state['native_script']}")
    ])

    return {
        **state,
        "english_text": response.content.strip(),
        "steps": state["steps"] + [f"✅ Node 3 — Translated {state['base_language']} → English"],
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 4 — Analyse sentiment
# ══════════════════════════════════════════════════════════════════════════════
def node_analyse_sentiment(state: ParentMessageState) -> ParentMessageState:
    """
    Classify the English message into:
      - sentiment:  positive / neutral / concerned / urgent
      - urgency:    low / medium / high
      - category:   academic / behavioral / attendance / fee / health / general
      - reason:     one sentence
    Also checks for alert keywords (bullying, ragging, etc.)
    Uses fast 8B model — JSON classification, low complexity.
    """
    prompt = f"""Analyse this school parent message and return ONLY valid JSON.

Message: "{state['english_text']}"

{{"sentiment":"positive/neutral/concerned/urgent",
  "urgency":"low/medium/high",
  "category":"academic/behavioral/attendance/fee/health/general",
  "reason":"one sentence"}}"""

    try:
        r     = _llm(fast=True).invoke([HumanMessage(content=prompt)])
        clean = r.content.strip().lstrip("```json").rstrip("```").strip()
        data  = json.loads(clean)
        senti = data.get("sentiment", "neutral")
        urgency  = data.get("urgency",   "low")
        category = data.get("category",  "general")
        reason   = data.get("reason",    "")
    except Exception:
        senti, urgency, category, reason = "neutral", "low", "general", "Unable to analyze"

    # Check alert keywords (simple keyword scan — no LLM needed)
    msg_lower = state["english_text"].lower()
    alert     = any(kw in msg_lower for kw in ALERT_KEYWORDS)

    return {
        **state,
        "sentiment":       senti,
        "urgency":         urgency,
        "category":        category,
        "sentiment_reason":reason,
        "is_alert":        alert,
        "steps": state["steps"] + [
            f"✅ Node 4 — Sentiment: {senti} | Urgency: {urgency} | Alert: {alert}"
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 5 — Generate smart replies
# ══════════════════════════════════════════════════════════════════════════════
def node_generate_replies(state: ParentMessageState) -> ParentMessageState:
    """
    Generate 3 short, professional reply suggestions for the counselor.
    Uses the category from Node 4 to tailor the suggestions.
    Falls back to template replies from config.py if LLM fails.
    Uses fast 8B model.
    """
    prompt = f"""Generate exactly 3 short professional reply suggestions for a school counselor.
Context category: {state['category']}
Parent message: "{state['english_text']}"

Return ONLY a JSON array of 3 strings:
["reply 1", "reply 2", "reply 3"]"""

    try:
        r     = _llm(fast=True).invoke([HumanMessage(content=prompt)])
        clean = r.content.strip().lstrip("```json").rstrip("```").strip()
        replies = json.loads(clean)
        if isinstance(replies, list) and len(replies) >= 3:
            smart = replies[:3]
        else:
            raise ValueError("Not enough replies")
    except Exception:
        smart = SMART_REPLIES.get(state["category"], SMART_REPLIES["general"])

    return {
        **state,
        "smart_replies": smart,
        "steps": state["steps"] + ["✅ Node 5 — Smart replies generated"],
    }


# ══════════════════════════════════════════════════════════════════════════════
# BUILD THE GRAPH
# ══════════════════════════════════════════════════════════════════════════════
def build_parent_pipeline():
    """
    Connects the 5 nodes into a LangGraph StateGraph.
    Returns a compiled graph ready to invoke.

    Flow:
      START → detect_language → convert_script → translate_english
            → analyse_sentiment → generate_replies → END
    """
    graph = StateGraph(ParentMessageState)

    # Register nodes
    graph.add_node("detect_language",   node_detect_language)
    graph.add_node("convert_script",    node_convert_script)
    graph.add_node("translate_english", node_translate_english)
    graph.add_node("analyse_sentiment", node_analyse_sentiment)
    graph.add_node("generate_replies",  node_generate_replies)

    # Connect edges — each node flows directly into the next
    graph.add_edge(START,              "detect_language")
    graph.add_edge("detect_language",  "convert_script")
    graph.add_edge("convert_script",   "translate_english")
    graph.add_edge("translate_english","analyse_sentiment")
    graph.add_edge("analyse_sentiment","generate_replies")
    graph.add_edge("generate_replies",  END)

    return graph.compile()


# ── Public function called from app.py ────────────────────────────────────────
def run_parent_pipeline(raw_text: str, rag_context: str = "") -> dict:
    """
    Entry point for app.py.
    Runs the full 5-node LangGraph pipeline on a parent message.
    Returns the final State dict with all results filled in.
    """
    pipeline = build_parent_pipeline()

    initial_state: ParentMessageState = {
        "original_text":    raw_text,
        "rag_context":      rag_context,
        "detected_lang":    "",
        "base_language":    "",
        "was_romanized":    False,
        "native_script":    "",
        "english_text":     "",
        "sentiment":        "neutral",
        "urgency":          "low",
        "category":         "general",
        "sentiment_reason": "",
        "is_alert":         False,
        "smart_replies":    [],
        "steps":            [],
    }

    result = pipeline.invoke(initial_state)
    return result