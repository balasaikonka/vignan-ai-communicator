# app.py  —  Vignan University AI Communication System
# Run: streamlit run app.py

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Load GROQ_API_KEY from .env file (local dev).
# On Streamlit Cloud: set it in App Settings → Secrets.
# On Railway/Render: set it as an environment variable in the dashboard.
load_dotenv()

st.set_page_config(
    page_title="Vignan University — AI Communicator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #f5f7fb; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a237e 0%, #283593 100%) !important;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: #e8eaf6 !important; }
.header {
    background: linear-gradient(135deg, #1a237e 0%, #1565c0 50%, #0277bd 100%);
    border-radius: 16px; padding: 24px 32px; margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(26,35,126,0.25);
}
.header h1 { color: white; font-size: 1.75rem; font-weight: 700; margin: 0; }
.header p  { color: rgba(255,255,255,0.8); margin: 6px 0 0; font-size: 0.9rem; }
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 12px; padding: 4px; gap: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: #546e7a; font-weight: 500; font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a237e, #1565c0) !important;
    color: white !important;
}
.chat-window {
    background: white; border-radius: 14px; border: 1px solid #e3e8f0;
    padding: 20px; min-height: 400px; max-height: 480px; overflow-y: auto;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 16px;
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-thumb { background: #c5cae9; border-radius: 4px; }
.row-parent {
    display: flex; justify-content: flex-end; align-items: flex-end;
    gap: 8px; margin: 12px 0;
}
.bubble-parent {
    background: linear-gradient(135deg, #1565c0, #1e88e5);
    color: white; padding: 12px 16px; border-radius: 18px 18px 4px 18px;
    max-width: 68%; font-size: 0.9rem; line-height: 1.55;
    box-shadow: 0 2px 8px rgba(21,101,192,0.25);
}
.row-counselor {
    display: flex; justify-content: flex-start; align-items: flex-end;
    gap: 8px; margin: 12px 0;
}
.bubble-counselor {
    background: white; color: #263238; padding: 12px 16px;
    border-radius: 18px 18px 18px 4px; max-width: 68%;
    font-size: 0.9rem; line-height: 1.55;
    border: 1px solid #e3e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.av {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.av-parent    { background: #1565c0; }
.av-counselor { background: #2e7d32; }
.ts-right { font-size: 0.67rem; color: #90a4ae; text-align: right; margin-top: 3px; }
.ts-left  { font-size: 0.67rem; color: #90a4ae; text-align: left;  margin-top: 3px; }
.trans-note {
    font-size: 0.82rem; color: #1a237e;
    margin-top: 6px; padding: 6px 10px;
    background: #e8eaf6; border-radius: 6px; border-left: 3px solid #3f51b5;
    line-height: 1.5;
}
.alert-banner {
    background: linear-gradient(135deg, #b71c1c, #c62828);
    border-radius: 10px; padding: 12px 18px; color: #ffcdd2;
    font-size: 0.87rem; font-weight: 500; margin: 8px 0;
    border: 1px solid #ef9a9a;
}
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; margin: 2px 3px;
}
.s-urgent    { background:#ffebee; color:#c62828; border:1px solid #ef9a9a; }
.s-concerned { background:#fff8e1; color:#f57f17; border:1px solid #ffcc02; }
.s-neutral   { background:#e3f2fd; color:#1565c0; border:1px solid #90caf9; }
.s-positive  { background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; }
.card {
    background: white; border-radius: 12px; padding: 16px 18px;
    border: 1px solid #e3e8f0; margin: 8px 0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.card h4 { color: #1a237e; margin: 0 0 6px 0; font-size: 0.88rem; font-weight: 600; }
.card p  { color: #546e7a; margin: 0; font-size: 0.83rem; line-height: 1.5; }
.bot-answer {
    background: #e8eaf6; border-left: 4px solid #3f51b5;
    border-radius: 0 10px 10px 0; padding: 14px 16px;
    color: #1a237e; font-size: 0.9rem; line-height: 1.6; margin: 8px 0;
}
.bot-question {
    background: white; border: 1px solid #e3e8f0; border-radius: 10px;
    padding: 10px 14px; color: #546e7a; font-size: 0.88rem;
    margin: 8px 0; text-align: right;
}
.summary-box {
    background: #e8f5e9; border-left: 4px solid #2e7d32;
    border-radius: 0 10px 10px 0; padding: 14px 18px;
    color: #1b5e20; font-size: 0.9rem; line-height: 1.6;
}
.sec-label {
    font-size: 0.78rem; font-weight: 600; color: #90a4ae;
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;
}
footer, #MainMenu { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
DEFAULTS = {
    "messages":               [],
    "bot_history":            [],
    "smart_replies":          [],
    "smart_replies_native":   [],
    "sr_cache_key":           "",
    "last_sentiment":         None,
    "show_alert":             False,
    "parent_lang":            "Telugu",
    "role":                   "Parent",
    "parent_msg":             "",
    "counselor_msg":          "",
    "_clear_parent":          False,
    "_clear_counselor":       False,
    "_auto_send":             False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


@st.cache_resource(show_spinner="Loading Vignan University knowledge base...")
def load_rag():
    from rag import build_rag_engine
    return build_rag_engine("vignan_university_knowledge.txt")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Vignan AI")
    st.markdown("---")
    # API key is pre-configured — no manual entry needed
    st.markdown("---")
    st.markdown("### 👤 Your Role")
    role = st.radio("Login as:", ["Parent", "Counselor"], horizontal=True)
    st.session_state.role = role

    from config import LANGUAGES
    st.markdown("### 🌍 Parent Language")
    parent_lang = st.selectbox(
        "Language", list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index("Telugu")
    )
    st.session_state.parent_lang = parent_lang

    st.markdown("---")
    st.markdown("**🏫 Vignan's University**")
    st.caption("Vadlamudi, Guntur, AP · www.vignan.ac.in")
    st.markdown("---")
    st.markdown("**⚙️ Stack**")
    st.caption("• Groq LLaMA 3.3 70B\n• ChromaDB + LangChain\n• Sentence Transformers")
    st.markdown("---")
    if st.button("🗑️ Clear All", use_container_width=True):
        for k in list(DEFAULTS.keys()):
            st.session_state[k] = DEFAULTS[k]
        st.rerun()


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>🎓 Vignan University — AI Communication System</h1>
    <p>Multilingual counselor–parent messaging · AI chatbot · Smart alerts · Knowledge base</p>
</div>
""", unsafe_allow_html=True)

# Validate API key is present — stop early with a clear message if missing
if not os.environ.get("GROQ_API_KEY"):
    st.error(
        "⚠️ **GROQ_API_KEY not found.**\n\n"
        "**Local:** Create a `.env` file in the project folder with:\n"
        "`GROQ_API_KEY=your_key_here`\n\n"
        "**Streamlit Cloud:** Go to App Settings → Secrets and add:\n"
        "`GROQ_API_KEY = \"your_key_here\"`"
    )
    st.stop()

role        = st.session_state.role
parent_lang = st.session_state.parent_lang

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Messages", "🤖 AI Assistant", "📊 Analytics", "📚 Knowledge Base"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MESSAGING
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([3, 1], gap="medium")

    with left:
        st.markdown('<div class="sec-label">Conversation</div>', unsafe_allow_html=True)

        chat_html = '<div class="chat-window">'
        if not st.session_state.messages:
            chat_html += ('<p style="text-align:center;color:#b0bec5;'
                          'margin-top:120px;font-size:0.9rem;">No messages yet. Start below ↓</p>')

        for msg in st.session_state.messages:
            ts = msg.get("time", "")
            if msg["role"] == "parent":
                show    = msg.get("native_script", msg["text"])
                en_note = ""
                if msg.get("english") and msg["english"] != msg["text"]:
                    en_note = f'<div class="trans-note">🌐 English: {msg["english"]}</div>'
                # Show LangGraph pipeline steps if available
                steps_html = ""
                if msg.get("pipeline_steps"):
                    steps_joined = " → ".join(
                        s.split(" — ", 1)[1] if " — " in s else s
                        for s in msg["pipeline_steps"]
                    )
                    steps_html = (
                        f'<div style="font-size:0.68rem;color:#90a4ae;margin-top:4px;">' +
                        f'⚙ {steps_joined}</div>'
                    )
                chat_html += f"""
                <div class="row-parent">
                    <div>
                        <div class="bubble-parent">{show}</div>
                        {en_note}
                        {steps_html}
                        <div class="ts-right">{msg.get("detected_lang","")}&nbsp;·&nbsp;{ts}</div>
                    </div>
                    <div class="av av-parent">👨‍👩‍👧</div>
                </div>"""
            else:
                # Counselor reply — show English + native script translation
                native_reply = msg.get("translated", "")
                native_note  = ""
                if native_reply and parent_lang != "English":
                    native_note = f'<div class="trans-note">🌐 {parent_lang}: {native_reply}</div>'
                chat_html += f"""
                <div class="row-counselor">
                    <div class="av av-counselor">🎓</div>
                    <div>
                        <div class="bubble-counselor">{msg["text"]}</div>
                        {native_note}
                        <div class="ts-left">Counselor&nbsp;·&nbsp;{ts}</div>
                    </div>
                </div>"""

        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        if st.session_state.show_alert:
            st.markdown("""
            <div class="alert-banner">
                🚨 <strong>URGENT ALERT:</strong> This message contains sensitive content.
                Please respond immediately.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ══════════════════════════════════════════════════════════════════════
        # PARENT INPUT
        # ══════════════════════════════════════════════════════════════════════
        if role == "Parent":
            st.markdown(
                f'<div class="sec-label">Your Message — {parent_lang}</div>',
                unsafe_allow_html=True
            )

            # Suggestions: each item is (native_label, romanized_value)
            # Button shows native script (easy to read)
            # Clicking fills input box with Romanized (easy to type/edit) AND auto-sends
            PARENT_SUGGESTIONS = {
                "Telugu": [
                    ("📚 విద్య", [
                        ("నా పిల్లవాడు మాత్స్ లో వీక్ గా ఉన్నాడు",    "na pillavadu maths lo weak ga unnadu"),
                        ("నా పిల్లవాడు పరీక్షలో ఫెయిల్ అయ్యాడు",       "na pillavadu exams lo fail ayadu"),
                        ("హోమ్‌వర్క్ చేయడం లేదు, సహాయం కావాలి",        "homework cheyatledu, help kavali"),
                        ("నా పిల్లవాడి మార్కులు ఎలా ఉన్నాయి?",         "na pillavadu marks ela unnai?"),
                    ]),
                    ("📅 హాజరు", [
                        ("నా పిల్లవాడు స్కూల్ కి రావడం లేదు",           "na pillavadu school ki ravatledu"),
                        ("పిల్లవాడు అబ్సెంట్ గా ఉన్నాడు, కారణం చెప్పండి", "pillavadu absent ga unnadu, reason cheppandi"),
                        ("హాజరు ఎలా ఉంది చెప్పండి",                    "attendance ela undi cheppandi"),
                        ("లీవ్ అప్లై చేయాలి ఎలా?",                     "leave apply cheyyali ela?"),
                    ]),
                    ("💰 ఫీజు", [
                        ("ఫీజు కట్టడానికి చివరి తేదీ ఎంటి?",            "fee kattatam ki last date enti?"),
                        ("ఫీజు వివరాలు చెప్పండి",                       "fee details cheppandi"),
                        ("స్కాలర్‌షిప్ ఎలా అప్లై చేయాలి?",             "scholarship ela apply cheyali?"),
                        ("ఫీజు పే చేసాను, రసీదు రాలేదు",               "fee pay chesanu, receipt raledu"),
                    ]),
                    ("🏫 సాధారణం", [
                        ("టీచర్ తో మీటింగ్ పెట్టుకోవాలని ఉంది",        "teacher tho meeting pettukovalani undi"),
                        ("కాలేజీ టైమింగ్స్ చెప్పండి",                   "college timings cheppandi"),
                        ("తర్వాత PTM తేదీ ఎంటి?",                      "next PTM date enti?"),
                        ("హాస్టల్ లో సమస్య ఉంది",                       "hostel lo problem undi"),
                    ]),
                ],
                "Hindi": [
                    ("📚 पढ़ाई", [
                        ("मेरा बच्चा मैथ्स में कमज़ोर है",               "mera bachcha maths mein weak hai"),
                        ("मेरा बच्चा परीक्षा में फेल हो गया",            "mera bachcha exam mein fail ho gaya"),
                        ("होमवर्क नहीं कर रहा, मदद चाहिए",              "homework nahi kar raha, help chahiye"),
                        ("मार्क्स कैसे हैं बताइए",                       "marks kaise hain bataiye"),
                    ]),
                    ("📅 उपस्थिति", [
                        ("मेरा बच्चा स्कूल नहीं आ रहा",                  "mera bachcha school nahi aa raha"),
                        ("अनुपस्थित है, कारण बताओ",                      "absent hai, reason batao"),
                        ("उपस्थिति कितनी है?",                           "attendance kitni hai?"),
                        ("छुट्टी के लिए आवेदन कैसे करें?",              "leave apply kaise kare?"),
                    ]),
                    ("💰 फीस", [
                        ("फीस जमा करने की अंतिम तिथि क्या है?",         "fee jama karne ki last date kya hai?"),
                        ("फीस का विवरण बताएं",                           "fee details batao"),
                        ("छात्रवृत्ति के लिए कैसे आवेदन करें?",         "scholarship ke liye kaise apply kare?"),
                        ("फीस दे दी, रसीद नहीं आई",                     "fee de diya, receipt nahi aayi"),
                    ]),
                    ("🏫 सामान्य", [
                        ("शिक्षक से मिलना चाहता हूँ",                    "teacher se milna chahta hoon"),
                        ("कॉलेज का समय क्या है?",                        "college timing kya hai?"),
                        ("अगली PTM कब है?",                              "next PTM kab hai?"),
                        ("हॉस्टल में समस्या है",                          "hostel mein problem hai"),
                    ]),
                ],
                "Tamil": [
                    ("📚 கல்வி", [
                        ("என் பிள்ளை மாத்ஸ்ல வீக்கா இருக்கான்",         "en pillai maths la weak aa irukkan"),
                        ("என் பிள்ளை தேர்வில் தோல்வி அடைந்தான்",        "en pillai exam la fail aaitaan"),
                        ("ஹோம்வொர்க் செய்யல, உதவி வேண்டும்",            "homework seyyala, help vendum"),
                        ("மார்க்ஸ் எப்படி இருக்கு சொல்லுங்க",           "marks epdi irukku sollunga"),
                    ]),
                    ("📅 வருகை", [
                        ("என் பிள்ளை பள்ளிக்கு வரல",                    "en pillai school ku varala"),
                        ("வராமல் இருக்கான், காரணம் சொல்லுங்க",           "absent aa irukkaan, karanam sollunga"),
                        ("வருகை எப்படி இருக்கு?",                        "attendance epdi irukku?"),
                        ("விடுமுறை விண்ணப்பிக்க எப்படி?",               "leave apply pannuvathu epdi?"),
                    ]),
                    ("💰 கட்டணம்", [
                        ("கட்டணம் கட்ட கடைசி தேதி என்ன?",               "fee kattarathuku last date enna?"),
                        ("கட்டண விவரங்கள் சொல்லுங்க",                   "fee details sollunga"),
                        ("உதவித்தொகைக்கு விண்ணப்பிக்க எப்படி?",         "scholarship ku apply pannuvathu epdi?"),
                        ("கட்டணம் கட்டினேன், ரசீது வரல",                "fee kattinen, receipt varala"),
                    ]),
                    ("🏫 பொது", [
                        ("ஆசிரியரிடம் சந்திப்பு வேண்டும்",              "teacher kita meeting vaikanum"),
                        ("கல்லூரி நேரம் என்ன?",                         "college timing enna?"),
                        ("அடுத்த PTM எப்போது?",                          "next PTM eppo?"),
                        ("விடுதியில் சிக்கல் இருக்கு",                   "hostel la problem irukku"),
                    ]),
                ],
            }
            DEFAULT_PARENT = [
                ("📚 Academics", [
                    ("My child is weak in mathematics",     "My child is weak in mathematics"),
                    ("My child failed the exam",            "My child failed the exam"),
                    ("Not doing homework, need help",       "Not doing homework, need help"),
                    ("Please share the marks",              "Please share the marks"),
                ]),
                ("📅 Attendance", [
                    ("My child is not attending school",    "My child is not attending school"),
                    ("Child is absent, please advise",      "Child is absent, please advise"),
                    ("What is the current attendance?",     "What is the current attendance?"),
                    ("How to apply for leave?",             "How to apply for leave?"),
                ]),
                ("💰 Fees", [
                    ("What is the fee payment last date?",  "What is the fee payment last date?"),
                    ("Please share fee details",            "Please share fee details"),
                    ("How to apply for scholarship?",       "How to apply for scholarship?"),
                    ("Fee paid but receipt not received",   "Fee paid but receipt not received"),
                ]),
                ("🏫 General", [
                    ("I want to meet the teacher",          "I want to meet the teacher"),
                    ("What are the college timings?",       "What are the college timings?"),
                    ("When is the next PTM?",               "When is the next PTM?"),
                    ("There is a problem in the hostel",    "There is a problem in the hostel"),
                ]),
            ]

            suggestions = PARENT_SUGGESTIONS.get(parent_lang, DEFAULT_PARENT)

            with st.expander("💡 Tap a suggestion — it will send automatically", expanded=False):
                for cat_name, cat_msgs in suggestions:
                    st.caption(cat_name)
                    cols = st.columns(2)
                    for idx, item in enumerate(cat_msgs):
                        native_label, romanized_value = item
                        btn_key = f"p_sugg_{parent_lang}_{cat_name}_{idx}"
                        # Show native script on button (easy to read)
                        # Clicking fills box with Romanized AND auto-sends
                        if cols[idx % 2].button(native_label, key=btn_key, use_container_width=True):
                            st.session_state["parent_msg"] = romanized_value
                            st.session_state["_auto_send"] = True
                            st.rerun()

            # Apply clear flag BEFORE widget renders
            if st.session_state.get("_clear_parent"):
                st.session_state["parent_msg"]   = ""
                st.session_state["_clear_parent"] = False

            st.text_area(
                "Your message",
                height=90,
                placeholder=(
                    f"Type in {parent_lang} or Romanized {parent_lang}...\n"
                    f"Example: 'na pillavadu school ki ravatledu'"
                ),
                label_visibility="collapsed",
                key="parent_msg",
            )

            c1, _ = st.columns([1, 5])
            manual_send = c1.button("Send 📤", type="primary", use_container_width=True)

            if manual_send or st.session_state.get("_auto_send"):
                st.session_state["_auto_send"] = False
                msg_text = st.session_state["parent_msg"].strip()
                if msg_text:
                    with st.spinner("Processing message through LangGraph pipeline..."):
                        from pipeline import run_parent_pipeline
                        from rag import get_context
                        # Get RAG context first so Node 3 can use it
                        rag_engine  = load_rag()
                        rag_context = get_context(rag_engine, msg_text)
                        # Run the full 5-node LangGraph pipeline
                        result = run_parent_pipeline(msg_text, rag_context)

                    # Build sentiment dict in same shape as before for the UI
                    sentiment = {
                        "sentiment": result["sentiment"],
                        "urgency":   result["urgency"],
                        "category":  result["category"],
                        "reason":    result["sentiment_reason"],
                    }
                    st.session_state.messages.append({
                        "role":          "parent",
                        "text":          msg_text,
                        "native_script": result["native_script"],
                        "english":       result["english_text"],
                        "detected_lang": result["base_language"],
                        "was_romanized": result["was_romanized"],
                        "time":          datetime.now().strftime("%I:%M %p"),
                        "pipeline_steps": result["steps"],
                    })
                    st.session_state.last_sentiment       = sentiment
                    st.session_state.show_alert           = result["is_alert"]
                    st.session_state.smart_replies        = result["smart_replies"]
                    st.session_state.smart_replies_native = []
                    st.session_state.sr_cache_key         = ""
                    st.session_state["_clear_parent"]     = True
                    st.rerun()

        # ══════════════════════════════════════════════════════════════════════
        # COUNSELOR INPUT
        # ══════════════════════════════════════════════════════════════════════
        else:
            st.markdown(
                '<div class="sec-label">Your Reply — type in English</div>',
                unsafe_allow_html=True
            )

            COUNSELOR_SUGGESTIONS = {
                "📚 Academic": [
                    "Your child is performing well. Keep encouraging daily study at home.",
                    "We noticed difficulty in Mathematics. Extra coaching is every Tuesday.",
                    "Your child's grades improved this semester. Great progress!",
                    "Please enroll your child in remedial classes — Tuesday and Thursday.",
                    "Check the student portal for detailed marks and subject-wise performance.",
                    "Pending assignments must be submitted before end of this week.",
                ],
                "📅 Attendance": [
                    "We noticed your child has been absent. Please let us know if there is an issue.",
                    "Regular attendance is required. Below 75% means exam debarment.",
                    "Please submit a medical certificate for illness-related absence.",
                    "Attendance is at a concerning level. Please ensure daily presence.",
                    "Leave applications need 2 days advance notice. Contact the office.",
                    "Your child's attendance is excellent this month. Well done!",
                ],
                "💰 Fees": [
                    "The fee deadline is approaching. Please pay before the due date.",
                    "You can pay online at www.vignan.ac.in — it is quick and easy.",
                    "Scholarship forms are at the accounts office. Deadline: October 15.",
                    "Fee payment received. Receipt will be sent to your registered email.",
                    "Late fee penalty applies after the due date. Please pay soon.",
                    "Contact the accounts office for fee-related queries.",
                ],
                "⚠️ Behavioral": [
                    "We need to discuss your child's behavior. Can we meet this week?",
                    "Your child has excellent discipline. We appreciate your support.",
                    "A counseling session is arranged for your child. We will inform you.",
                    "We are working closely with your child. Please support at home too.",
                    "A minor incident happened. Your child has been counseled. All resolved.",
                    "Please remind your child about uniform and code of conduct.",
                ],
                "📆 Meetings": [
                    "Next PTM is first Saturday of next month, 9 AM to 1 PM.",
                    "You can visit any working day between 10 AM and 4 PM to meet me.",
                    "Thank you for reaching out. We will address your concern shortly.",
                    "Please visit the administrative office for further help.",
                    "We appreciate your involvement in your child's education.",
                    "Contact us anytime through the university portal or phone.",
                ],
                "🏥 Health": [
                    "Your child visited the medical centre. Please ensure rest at home.",
                    "Our counselor is available every Wednesday. I can arrange a session.",
                    "We noticed your child seems stressed. Let us support them together.",
                    "Please inform us of any medical condition so we can assist better.",
                    "Your child is doing well and settling in nicely.",
                    "For mental health concerns, please reach out to us anytime.",
                ],
            }

            with st.expander("💡 Tap a suggestion to fill your reply", expanded=False):
                for cat_name, cat_replies in COUNSELOR_SUGGESTIONS.items():
                    st.caption(cat_name)
                    cols = st.columns(2)
                    for idx, reply in enumerate(cat_replies):
                        label   = reply[:65] + "…" if len(reply) > 65 else reply
                        btn_key = f"c_sugg_{cat_name}_{idx}"
                        if cols[idx % 2].button(label, key=btn_key,
                                                use_container_width=True, help=reply):
                            st.session_state["counselor_msg"] = reply
                            st.rerun()

            # AI Smart Replies — show English + native script translation below
            if st.session_state.smart_replies:
                st.caption("🤖 AI Smart Replies — based on last parent message:")

                cache_key = str(st.session_state.smart_replies) + parent_lang
                if st.session_state.sr_cache_key != cache_key:
                    if parent_lang != "English":
                        from translator import translate_to_language
                        with st.spinner(f"Translating to {parent_lang}..."):
                            st.session_state.smart_replies_native = [
                                translate_to_language(r, parent_lang)
                                for r in st.session_state.smart_replies
                            ]
                    else:
                        st.session_state.smart_replies_native = list(st.session_state.smart_replies)
                    st.session_state.sr_cache_key = cache_key

                native_list = st.session_state.smart_replies_native
                for i, reply in enumerate(st.session_state.smart_replies):
                    native_text = native_list[i] if i < len(native_list) else ""
                    col_card, col_btn = st.columns([5, 1])
                    with col_card:
                        native_line = (
                            f'<div style="font-size:0.9rem;color:#1a237e;margin-top:6px;">'
                            f'🌐 {native_text}</div>'
                            if native_text and parent_lang != "English" else ""
                        )
                        st.markdown(
                            f'<div style="background:#e8eaf6;border-radius:10px;'
                            f'padding:10px 14px;border-left:4px solid #3f51b5;margin:4px 0;">'
                            f'<div style="font-size:0.82rem;color:#546e7a;">🇬🇧 {reply}</div>'
                            f'{native_line}</div>',
                            unsafe_allow_html=True,
                        )
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Use ✓", key=f"ai_sr_{i}", use_container_width=True):
                            st.session_state["counselor_msg"] = reply
                            st.rerun()

            # Apply clear flag BEFORE widget renders
            if st.session_state.get("_clear_counselor"):
                st.session_state["counselor_msg"]    = ""
                st.session_state["_clear_counselor"] = False

            st.text_area(
                "Your reply",
                height=90,
                placeholder="Type your reply in English...",
                label_visibility="collapsed",
                key="counselor_msg",
            )

            c1, _ = st.columns([1, 5])
            if c1.button("Send 📤", type="primary", use_container_width=True):
                msg_text = st.session_state["counselor_msg"].strip()
                if msg_text:
                    with st.spinner("Translating reply to parent's language..."):
                        from translator import translate_to_language
                        # Translate to native script (Telugu/Hindi/Tamil etc.)
                        translated = (
                            translate_to_language(msg_text, parent_lang)
                            if parent_lang != "English" else ""
                        )
                    st.session_state.messages.append({
                        "role":       "counselor",
                        "text":       msg_text,
                        "translated": translated,
                        "time":       datetime.now().strftime("%I:%M %p"),
                    })
                    st.session_state["_clear_counselor"]      = True
                    st.session_state.smart_replies            = []
                    st.session_state.smart_replies_native     = []
                    st.session_state.sr_cache_key             = ""
                    st.session_state.show_alert               = False
                    st.rerun()

    # ── Right panel ────────────────────────────────────────────────────────────
    with right:
        st.markdown('<div class="sec-label">AI Insights</div>', unsafe_allow_html=True)

        sentiment = st.session_state.last_sentiment
        if sentiment:
            s   = sentiment.get("sentiment", "neutral")
            cls = {
                "urgent":"s-urgent","concerned":"s-concerned",
                "neutral":"s-neutral","positive":"s-positive",
            }.get(s, "s-neutral")
            st.markdown(f"""
            <div class="card">
                <h4>📊 Message Analysis</h4>
                <p>
                    <span class="badge {cls}">{s.upper()}</span><br><br>
                    Urgency: <strong>{sentiment.get('urgency','').title()}</strong><br>
                    Category: <strong>{sentiment.get('category','').title()}</strong><br><br>
                    {sentiment.get('reason','')}
                </p>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h4>🔄 Translation Flow</h4>
            <p>
                Parent types Romanized<br>↓ Detect language<br>
                ↓ Convert to native script<br>↓ Translate → English<br>
                ↓ Counselor replies<br>↓ Translate back (Native script)
            </p>
        </div>""", unsafe_allow_html=True)

        if len(st.session_state.messages) >= 2:
            if st.button("📝 Summarize Chat", use_container_width=True):
                from ai_features import summarize_conversation
                with st.spinner("Summarizing..."):
                    summary = summarize_conversation(st.session_state.messages)
                st.markdown(f'<div class="summary-box">{summary}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI ASSISTANT CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    is_english = parent_lang == "English"

    st.markdown('<div class="sec-label">AI Assistant — Vignan University Q&A</div>',
                unsafe_allow_html=True)
    if not is_english:
        st.caption(
            f"Type in {parent_lang} or Romanized {parent_lang}. "
            f"Answers shown in {parent_lang} native script with English below."
        )
    else:
        st.caption("Ask anything about Vignan's University — timings, fees, exams, hostel, placements and more.")

    # Display conversation history
    for msg in st.session_state.bot_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="bot-question">🙋 {msg["text"]}</div>',
                        unsafe_allow_html=True)
        else:
            if not is_english and msg.get("native"):
                # Show native script prominently, English as small reference below
                st.markdown(f"""
                <div class="bot-answer">
                    🤖 <strong>{msg["native"]}</strong>
                    <div style="margin-top:10px;padding-top:10px;
                                border-top:1px solid #c5cae9;
                                font-size:0.78rem;color:#7986cb;">
                        🇬🇧 {msg["text"]}
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-answer">🤖 {msg["text"]}</div>',
                            unsafe_allow_html=True)

    st.markdown("---")

    # Quick question buttons — native script labels
    st.caption("📌 Quick questions — click to ask:")
    quick_en = [
        "What are the college timings?",    "When is the next PTM?",
        "What is the attendance rule?",     "What is the fee structure?",
        "What placement companies visit?",  "What are the hostel facilities?",
        "When are the mid exams?",          "What clubs are available?",
    ]
    quick_native = {
        "Telugu": [
            "కాలేజీ టైమింగ్స్ ఎంటి?",       "తర్వాత PTM ఎప్పుడు?",
            "హాజరు నియమం ఏమిటి?",           "ఫీజు స్ట్రక్చర్ ఎంటి?",
            "ప్లేస్‌మెంట్స్ ఎలా చేయాలి?",  "హాస్టల్ సదుపాయాలు ఎంటి?",
            "మిడ్ పరీక్షలు ఎప్పుడు?",       "క్లబ్‌లు ఏమి ఉన్నాయి?",
        ],
        "Hindi": [
            "कॉलेज का समय क्या है?",         "अगली PTM कब है?",
            "उपस्थिति नियम क्या है?",        "फीस संरचना क्या है?",
            "प्लेसमेंट कंपनियां कौन सी?",   "हॉस्टल की सुविधाएं क्या हैं?",
            "मिड परीक्षा कब है?",             "कौन से क्लब हैं?",
        ],
        "Tamil": [
            "கல்லூரி நேரம் என்ன?",          "அடுத்த PTM எப்போது?",
            "வருகை விதி என்ன?",              "கட்டண அமைப்பு என்ன?",
            "வேலைவாய்ப்பு நிறுவனங்கள்?",   "விடுதி வசதிகள் என்ன?",
            "மிட் தேர்வு எப்போது?",          "என்ன கிளப்கள் உள்ளன?",
        ],
    }
    btn_labels = quick_native.get(parent_lang, quick_en)
    q_cols  = st.columns(4)
    clicked = None
    for i, (label, en_q) in enumerate(zip(btn_labels, quick_en)):
        if q_cols[i % 4].button(label, key=f"qbot_{i}", use_container_width=True):
            clicked = en_q

    ph = (
        f"Type in {parent_lang} or Romanized e.g. 'fee last date enti?'"
        if not is_english else "e.g. What is the last date to pay fees?"
    )
    q_col, s_col = st.columns([5, 1])
    user_q  = q_col.text_input("question", placeholder=ph,
                                label_visibility="collapsed", key="bot_q")
    ask_btn = s_col.button("Ask 🔍", type="primary", use_container_width=True)

    typed  = user_q.strip() if ask_btn and user_q.strip() else None
    to_ask = clicked or typed

    if to_ask:
        with st.spinner("Searching knowledge base..."):
            from rag import get_context
            from ai_features import answer_question
            from translator import translate_to_english, translate_to_language

            rag  = load_rag()
            en_q = (
                translate_to_english(to_ask, parent_lang)
                if (typed and not clicked) else to_ask
            )
            context        = get_context(rag, en_q)
            english_answer = answer_question(en_q, context)
            # Translate answer to native script for display
            native_ans = (
                translate_to_language(english_answer, parent_lang)
                if not is_english else ""
            )

        st.session_state.bot_history.append({"role": "user", "text": to_ask})
        st.session_state.bot_history.append({
            "role": "bot", "text": english_answer, "native": native_ans
        })
        st.rerun()

    if st.session_state.bot_history:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.bot_history = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">Conversation Analytics</div>', unsafe_allow_html=True)

    msgs   = st.session_state.messages
    total  = len(msgs)
    p_cnt  = sum(1 for m in msgs if m["role"] == "parent")
    c_cnt  = sum(1 for m in msgs if m["role"] == "counselor")
    langs  = list(set(m.get("detected_lang","") for m in msgs if m.get("detected_lang")))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Messages",    total)
    c2.metric("Parent Messages",   p_cnt)
    c3.metric("Counselor Replies", c_cnt)
    c4.metric("Languages Seen",    len(langs))

    st.markdown("---")
    left_a, right_a = st.columns(2)

    with left_a:
        st.markdown('<div class="sec-label">Conversation Summary</div>', unsafe_allow_html=True)
        if len(msgs) >= 2:
            if st.button("Generate Summary", type="primary", use_container_width=True):
                from ai_features import summarize_conversation
                with st.spinner("Summarizing..."):
                    sm = summarize_conversation(msgs)
                st.markdown(f'<div class="summary-box">{sm}</div>', unsafe_allow_html=True)
        else:
            st.info("Have a conversation first.")

        st.markdown("---")
        st.markdown('<div class="sec-label">Message Log</div>', unsafe_allow_html=True)
        for i, msg in enumerate(msgs):
            icon = "👨‍👩‍👧" if msg["role"] == "parent" else "🎓"
            with st.expander(f"{icon} {msg['role'].title()} — {msg.get('time','')}"):
                st.write(f"**Original:** {msg['text']}")
                if msg.get("native_script") and msg["native_script"] != msg["text"]:
                    st.write(f"**Native Script:** {msg['native_script']}")
                if msg.get("english"):
                    st.write(f"**English:** {msg['english']}")
                if msg.get("translated"):
                    st.write(f"**Translated (Native):** {msg['translated']}")
                if msg.get("detected_lang"):
                    st.write(f"**Language:** {msg['detected_lang']}")

    with right_a:
        st.markdown('<div class="sec-label">Test Sentiment Analysis</div>', unsafe_allow_html=True)
        test_msg = st.text_area(
            "Enter any message to analyze:", height=90,
            placeholder="e.g. My child is being bullied at school.",
            key="analytics_msg"
        )
        if st.button("Analyze via LangGraph", type="primary", use_container_width=True):
            if test_msg.strip():
                with st.spinner("Running LangGraph pipeline..."):
                    from pipeline import run_parent_pipeline
                    res = run_parent_pipeline(test_msg, "")
                s   = res.get("sentiment","neutral")
                cls = {
                    "urgent":"s-urgent","concerned":"s-concerned",
                    "neutral":"s-neutral","positive":"s-positive",
                }.get(s,"s-neutral")
                alrt = res.get("is_alert", False)
                steps_text = "<br>".join(res.get("steps", []))
                st.markdown(f"""
                <div class="card">
                    <h4>Analysis Result</h4>
                    <p>
                        Sentiment: <span class="badge {cls}">{s.upper()}</span><br>
                        Urgency: <strong>{res.get("urgency","").upper()}</strong><br>
                        Category: <strong>{res.get("category","").title()}</strong><br>
                        Reason: {res.get("sentiment_reason","")}<br><br>
                        {'⚠️ <strong style="color:#c62828">ALERT: Sensitive content detected!</strong>'
                         if alrt else '✅ No sensitive keywords found.'}
                    </p>
                </div>""", unsafe_allow_html=True)
                st.markdown("**LangGraph Steps:**")
                for step in res.get("steps", []):
                    st.caption(step)
            else:
                st.warning("Please enter a message.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        '<div class="sec-label">Vignan University Knowledge Base — ChromaDB RAG</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "`vignan_university_knowledge.txt` is loaded, chunked, embedded and stored "
        "in ChromaDB. The AI assistant searches this to answer parent questions."
    )

    left_kb, right_kb = st.columns(2)

    with left_kb:
        st.markdown('<div class="sec-label">Knowledge File</div>', unsafe_allow_html=True)
        from rag import load_knowledge_file
        raw    = load_knowledge_file("vignan_university_knowledge.txt")
        topics = [
            ln.strip() for ln in raw.split("\n")
            if ln.strip().isupper() and len(ln.strip()) > 5
        ]
        st.info(f"📄 {len(raw):,} characters · {len(topics)} sections loaded")
        for t in topics[:20]:
            st.caption(f"📌 {t}")
        with st.expander("View file preview"):
            st.text(raw[:3000] + "\n\n... [truncated]")

    with right_kb:
        st.markdown('<div class="sec-label">Test RAG Search</div>', unsafe_allow_html=True)
        sq = st.text_input("Search query", placeholder="e.g. placement companies",
                           key="kb_search_q")
        if st.button("🔍 Search ChromaDB", use_container_width=True):
            if sq.strip():
                from rag import get_context
                rag    = load_rag()
                result = get_context(rag, sq)
                st.markdown(
                    f'<div class="bot-answer">{result or "No results found."}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("Enter a search query.")

        st.markdown("---")
        st.markdown('<div class="sec-label">Add Extra Document</div>', unsafe_allow_html=True)
        extra_topic = st.text_input("Topic", placeholder="e.g. New Exam Schedule",
                                   key="kb_topic")
        extra_text  = st.text_area("Content", height=100,
                                   placeholder="Paste university info here...",
                                   key="kb_content")
        if st.button("📥 Add to ChromaDB", type="primary", use_container_width=True):
            if extra_topic.strip() and extra_text.strip():
                rag = load_rag()
                rag.add_texts([extra_text], metadatas=[{"source": extra_topic}])
                st.success(f"✅ '{extra_topic}' added to ChromaDB!")
            else:
                st.warning("Please fill in both fields.")