# ai_features.py
# Smart AI features:
#   - Sentiment analysis and urgency detection
#   - Smart reply suggestions for counselors
#   - Conversation summarization
#   - AI chatbot using RAG context

import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from config import PRIMARY_MODEL, FAST_MODEL, ALERT_KEYWORDS, SMART_REPLIES


def _llm(fast: bool = True) -> ChatGroq:
    return ChatGroq(
        model=FAST_MODEL if fast else PRIMARY_MODEL,
        temperature=0.2,
        groq_api_key=os.environ.get("GROQ_API_KEY", ""),
        max_tokens=512
    )


# ── Sentiment Analysis ─────────────────────────────────────────────────────────
def analyze_sentiment(message: str) -> dict:
    """
    Analyze sentiment and urgency of a parent message.
    Returns: sentiment, urgency level, category, brief reason.
    """
    prompt = f"""Analyze this school parent message. Return ONLY valid JSON.

Message: "{message}"

Return exactly:
{{"sentiment": "positive/neutral/concerned/urgent",
  "urgency": "low/medium/high",
  "category": "academic/attendance/behavioral/fee/health/general",
  "reason": "one short sentence explaining the sentiment"}}"""

    try:
        r     = _llm(fast=True).invoke([HumanMessage(content=prompt)])
        clean = r.content.strip().lstrip("```json").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return {"sentiment": "neutral", "urgency": "low",
                "category": "general", "reason": "Unable to analyze"}


# ── Alert Detection ────────────────────────────────────────────────────────────
def is_alert_message(message: str) -> bool:
    """Return True if message contains sensitive/urgent keywords."""
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in ALERT_KEYWORDS)


# ── Smart Reply Suggestions ───────────────────────────────────────────────────
def get_smart_replies(message: str, category: str = "general") -> list:
    """
    Generate 3 smart reply suggestions for the counselor.
    Falls back to templates if LLM fails.
    """
    prompt = f"""Generate exactly 3 short, professional reply suggestions for a school counselor
responding to this parent message about: {category}

Parent message: "{message}"

Return ONLY a JSON array:
["suggestion 1", "suggestion 2", "suggestion 3"]"""

    try:
        r     = _llm(fast=True).invoke([HumanMessage(content=prompt)])
        clean = r.content.strip().lstrip("```json").rstrip("```").strip()
        result = json.loads(clean)
        if isinstance(result, list) and len(result) >= 3:
            return result[:3]
    except Exception:
        pass

    return SMART_REPLIES.get(category, SMART_REPLIES["general"])


# ── Conversation Summary ──────────────────────────────────────────────────────
def summarize_conversation(messages: list) -> str:
    """
    Summarize the full conversation in 2-3 sentences.
    messages: list of dicts with 'role' and 'text'/'english' keys
    """
    if not messages:
        return "No conversation yet."

    convo = "\n".join(
        f"{m['role'].title()}: {m.get('english', m['text'])}"
        for m in messages
    )
    r = _llm(fast=False).invoke([HumanMessage(
        content=f"""Summarize this school counselor-parent conversation in 2-3 sentences.
Cover: the main concern raised, what was discussed, and any action items.

Conversation:
{convo}

Summary:"""
    )])
    return r.content.strip()


# ── AI Chatbot with RAG ───────────────────────────────────────────────────────
def answer_question(question: str, rag_context: str) -> str:
    """
    Answer a parent's school-related question using the RAG context
    retrieved from Vignan University's knowledge base.
    """
    prompt = f"""You are a helpful AI assistant for Vignan's University, Guntur.
Answer the parent's question clearly and politely using the information below.
If the answer is not available, say: "Please contact the university office for this information."
Keep the answer brief and friendly.

University Information:
{rag_context}

Parent's Question: {question}

Answer:"""

    r = _llm(fast=False).invoke([HumanMessage(content=prompt)])
    return r.content.strip()
