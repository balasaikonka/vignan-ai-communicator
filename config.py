# config.py
# Central settings for Vignan University AI Communication System

import os

# ── API Keys ───────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# ── Groq LLM Models ────────────────────────────────────────────────────────────
PRIMARY_MODEL = "llama-3.3-70b-versatile"   # translation, responses, RAG
FAST_MODEL    = "llama-3.1-8b-instant"      # sentiment, quick tasks

# ── Supported Languages ────────────────────────────────────────────────────────
LANGUAGES = {
    "English":    "en",
    "Telugu":     "te",
    "Hindi":      "hi",
    "Tamil":      "ta",
    "Spanish":    "es",
    "French":     "fr",
    "Arabic":     "ar",
    "Bengali":    "bn",
    "Urdu":       "ur",
    "Chinese":    "zh",
    "Portuguese": "pt",
    "German":     "de",
    "Japanese":   "ja",
    "Korean":     "ko",
    "Vietnamese": "vi",
}

# ── Alert Keywords (trigger urgent highlight) ─────────────────────────────────
ALERT_KEYWORDS = [
    "bully", "bullying", "ragging", "hit", "hurt", "scared", "afraid",
    "fight", "abuse", "suicide", "harm", "danger", "emergency",
    "sick", "hospital", "accident", "threat", "drugs", "crying",
    "depression", "mental", "help", "urgent", "not eating", "missing",
    "suspended", "expelled", "harassment",
]

# ── Smart Reply Templates (fallback) ─────────────────────────────────────────
SMART_REPLIES = {
    "academic": [
        "We will arrange extra coaching sessions for your child.",
        "Please visit us for a detailed academic progress discussion.",
        "Your child has shown improvement. Keep encouraging at home.",
    ],
    "attendance": [
        "Please ensure your child attends classes regularly.",
        "Attendance below 75% will result in exam debarment.",
        "We noticed some absences. Please let us know if there are issues.",
    ],
    "behavioral": [
        "We are working with your child to resolve this matter.",
        "A counselor session has been scheduled for your child.",
        "Let us meet to discuss a plan to support your child.",
    ],
    "fee": [
        "The fee payment deadline is approaching. Please pay on time.",
        "Scholarship application forms are available at the accounts office.",
        "Online fee payment is available via the university portal.",
    ],
    "general": [
        "Thank you for reaching out. We will respond shortly.",
        "Please visit the administrative office for more information.",
        "Your concern has been noted and will be addressed promptly.",
    ],
}
