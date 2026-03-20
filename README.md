# 🎓 Vignan University — AI Communication System

> **Multilingual AI-powered messaging platform** that bridges the language barrier between school counselors and parents at Vignan's Foundation for Science, Technology and Research (VFSTR), Guntur, Andhra Pradesh.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Deploying to Streamlit Cloud](#deploying-to-streamlit-cloud)
- [Screenshots](#screenshots)
- [Use Case at VFSTR](#use-case-at-vfstr)
- [License](#license)

---

## Overview

Vignan AI Communication System solves a real problem: **counselors speak English, but many parents speak only Telugu, Hindi, or Tamil**. This platform enables seamless, real-time, bidirectional communication between them — with full automatic translation, sentiment detection, and an AI chatbot that answers parent queries using Vignan's own knowledge base.

---

## Features

| Feature | Description |
|---|---|
| 🌐 **Multilingual Messaging** | Parents type in Telugu, Hindi, Tamil, or Romanized scripts — messages are auto-translated for the counselor |
| 🔄 **Bidirectional Translation** | Counselor replies in English; parents receive responses in their native script |
| 🤖 **LangGraph Pipeline** | 5-node AI pipeline: detect language → convert script → translate → analyse sentiment → generate smart replies |
| 📊 **Sentiment Analysis** | Every parent message is classified as Positive / Neutral / Concerned / Urgent with urgency level |
| 🚨 **Alert System** | Auto-detects sensitive keywords (ragging, bullying, mental health) and flags them for immediate attention |
| 💡 **Smart Reply Suggestions** | AI generates 3 context-aware reply suggestions for the counselor after each parent message |
| 🔍 **RAG Chatbot** | Parents can ask questions about fees, attendance, exams, hostel, placements — answered using Vignan's knowledge base via ChromaDB |
| 📚 **Knowledge Base** | Vignan University information loaded, chunked, embedded, and stored in ChromaDB for semantic search |
| 📈 **Analytics Dashboard** | Message logs, language detection stats, sentiment history, and conversation summarization |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit |
| **LLM** | Groq — LLaMA 3.3 70B (translation, RAG) + LLaMA 3.1 8B Instant (sentiment, quick tasks) |
| **AI Pipeline** | LangGraph (5-node StateGraph) |
| **RAG / Vector DB** | ChromaDB + LangChain |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (free, runs locally) |
| **LLM Framework** | LangChain + LangChain-Groq |
| **Language** | Python 3.10+ |

---

## Project Structure

```
vignan-ai-communicator/
│
├── app.py                          # Main Streamlit app (4 tabs: Messages, AI Assistant, Analytics, Knowledge Base)
├── pipeline.py                     # LangGraph 5-node pipeline for parent message processing
├── ai_features.py                  # Sentiment analysis, smart replies, conversation summarization, RAG Q&A
├── translator.py                   # Language detection, Romanized → native script, translation functions
├── rag.py                          # ChromaDB RAG engine — builds vector store from knowledge file
├── config.py                       # Models, supported languages, alert keywords, fallback replies
├── vignan_university_knowledge.txt # Vignan University knowledge base (fees, timings, hostel, placements, etc.)
├── requirements.txt                # Python dependencies
├── .env                            # ← YOU CREATE THIS (never commit to git)
└── .gitignore                      # Excludes .env, __pycache__, chroma_db/
```

---

## How It Works

### 5-Node LangGraph Pipeline

Every parent message travels through this pipeline automatically:

```
Parent types message
       │
       ▼
  Node 1 — Detect Language
  (Telugu? Hindi? Romanized Telugu? English?)
       │
       ▼
  Node 2 — Convert Script
  (Romanized "na pillavadu" → native "నా పిల్లవాడు")
       │
       ▼
  Node 3 — Translate to English
  (for counselor to read — uses RAG context for tone)
       │
       ▼
  Node 4 — Analyse Sentiment
  (positive / neutral / concerned / urgent + alert check)
       │
       ▼
  Node 5 — Generate Smart Replies
  (3 AI suggestions for the counselor)
       │
       ▼
  Counselor reads English + sees AI suggestions
  Counselor replies in English
       │
       ▼
  Auto-translated back to parent's native script
```

### RAG Chatbot Flow

```
Parent asks question
       │
       ▼
  ChromaDB semantic search
  (top 4 relevant chunks from vignan_university_knowledge.txt)
       │
       ▼
  Groq LLaMA 70B answers using retrieved context
       │
       ▼
  Answer shown in parent's language (native script + English)
```

---

## Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A free Groq API key — get one at [console.groq.com](https://console.groq.com)

### Step 1 — Clone the repository

```bash
git clone https://github.com/balasaikonka/vignan-ai-communicator.git
cd vignan-ai-communicator
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first run downloads the `all-MiniLM-L6-v2` sentence transformer model (~90MB). This happens once and is cached locally.

### Step 3 — Set up environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ **Never commit `.env` to git.** It is listed in `.gitignore`.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key from [console.groq.com](https://console.groq.com) |

---

## Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Deploying to Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is **not** committed)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repository → set `app.py` as the main file
4. Go to **Advanced settings → Secrets** and add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

5. Click **Deploy** — your live URL will be:
   `https://vignan-ai-communicator.streamlit.app`

---

## Screenshots

### 💬 Messages Tab
- Parent types in Telugu/Hindi/Tamil or Romanized script
- Message is auto-translated and shown to counselor in English
- Sentiment badge and urgency level displayed
- AI smart reply suggestions shown

### 🤖 AI Assistant Tab
- Parent asks questions in their language
- RAG chatbot searches Vignan's knowledge base
- Answer shown in native script + English

### 📊 Analytics Tab
- Message count, language breakdown
- Sentiment analysis testing tool
- Full conversation summary

### 📚 Knowledge Base Tab
- Preview of loaded university knowledge
- Test ChromaDB semantic search
- Add new documents to the knowledge base

---

## Use Case at VFSTR

| Department | Application |
|---|---|
| **Student Welfare Office** | Alert detection for ragging, bullying, mental health crises |
| **Academic Counselors** | Communicate attendance, marks, remedial classes with parents in their language |
| **Accounts / Fee Office** | Parents can query fee deadlines, scholarships, receipts in Telugu/Hindi |
| **Hostel Administration** | Hostel-related parent queries answered instantly via the AI chatbot |
| **Administrative Office** | Reduces call volume by 60–70% for common queries (timings, PTM dates, exam schedules) |
| **Placement Cell** | Parents can ask about placement companies, eligibility, packages |

---

## Supported Languages

Telugu · Hindi · Tamil · English · Spanish · French · Arabic · Bengali · Urdu · Chinese · Portuguese · German · Japanese · Korean · Vietnamese

Romanized input is supported for Telugu, Hindi, and Tamil (parents can type in English letters and the system converts to native script automatically).

---

## Alert Keywords

The system automatically flags messages containing:

`bully · ragging · hit · hurt · scared · fight · abuse · suicide · harm · danger · emergency · hospital · accident · threat · drugs · depression · mental · missing · suspended · expelled · harassment`

Flagged messages show a red **🚨 URGENT ALERT** banner for the counselor.

---

## License

This project was developed as part of an academic submission at **Vignan's Foundation for Science, Technology and Research (VFSTR)**, Vadlamudi, Guntur, Andhra Pradesh.

---

## Author

**Bala Sai Konka**
Vignan's University, Guntur, AP
GitHub: [@balasaikonka](https://github.com/balasaikonka)

---

> Built with ❤️ using Groq · LangGraph · ChromaDB · Streamlit
