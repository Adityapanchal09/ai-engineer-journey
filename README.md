# 🤖 AI Engineer Journey

A daily learning log documenting my path to becoming an AI Engineer — building real, working projects using Python, the Groq API (LLaMA 3.3 70B), REST APIs, Streamlit, embeddings, and RAG.

## 🌐 Live Demo
**Chat With Your Notes (RAG App):** [Try it here →](your-streamlit-url-here)

## 🛠️ Tech Stack

- **Python 3.12**
- **Groq API** (LLaMA 3.3 70B Versatile)
- **Streamlit** — web UI + deployment
- **sentence-transformers** — local embeddings
- **python-dotenv** — environment management
- **requests** — REST API calls

## 📂 Projects

### Day 1-2: Hello AI + Conversational Chatbot
- `hello_ai.py` — First AI API call, basic request/response
- `chatbot.py` — Terminal chatbot with conversation memory using message history

**Concepts:** API calls, .env config, system prompts, conversation history, Git basics

---

### Day 3: REST APIs + AI Study Assistant
- `rest_practice.py` — GET requests, query parameters, combining REST APIs with AI
- `study_assistant.py` — Terminal-based subject tutor with custom system prompts

**Concepts:** HTTP methods, status codes, JSON, headers, prompt engineering

---

### Day 4: Structured Output + Quiz Generator
- `quiz_generator.py` — Generates MCQ quizzes on any topic, returns structured JSON, runs an interactive scored quiz

**Concepts:** Forcing JSON output from LLMs, `json.loads()`, functions, `enumerate()`, input validation

---

### Day 5: File Handling + Smart Document Reader
- `doc_reader.py` — Reads `.txt` notes and provides: summary, key points extraction, auto-generated quiz, and interactive document chat

**Concepts:** File I/O (`open`, `read`, `with`), injecting documents into prompts, multi-function architecture

---

### Day 6: Web App — AI Study Assistant (Streamlit)
- `study_app.py` — ChatGPT-style web interface for the study assistant with subject switching, persistent chat history, and live responses

**Concepts:** Streamlit UI components, `session_state`, the rerun model, `st.chat_message`, sidebars

---

### Day 7: Persistence + Quiz Generator Web App
- `study_app.py` (upgraded) — Chat history now saved to `chat_history.json` and reloaded automatically on app restart
- `quiz_app.py` — Full interactive quiz web app with AI-generated MCQs, clickable radio options, instant feedback, score tracking, and persistent results log

**Concepts:** JSON file persistence, `os.path.exists()` safety checks, multi-variable `session_state` state machines, conditional UI flow, debugging Streamlit rerun bugs

---

### Day 8: Prompt Chaining — Notes Processing Pipeline
- `notes_pipeline.py` — Takes raw messy notes through a 4-step AI pipeline: clean grammar → summarize → extract key points (JSON) → generate exam questions (JSON)

**Concepts:** Prompt chaining, reusable `ask()` helper function, multi-step pipelines, choosing the right upstream input for each step

---

### Day 9: Embeddings + Semantic Search
- `embedd_compare.py` — Compares meaning similarity using cosine similarity
- `semantic_search.py` — Natural-language search over study notes by MEANING, not keywords

**Concepts:** Sentence embeddings (`sentence-transformers`), vectors as meaning, cosine similarity, `.item()` tensor unwrapping, semantic vs keyword search

---

### Day 10: Mini RAG — Chat With Your Notes (Terminal)
- `mini_rag.py` — Complete RAG pipeline from scratch: load document → chunk → embed → retrieve relevant chunks → answer grounded in context only, with similarity threshold to prevent hallucination

**Concepts:** Document chunking, batch embedding, semantic retrieval, context-grounded generation, list comprehensions, similarity thresholds, hallucination prevention

---

### Day 11: RAG Web App — Chat With Your Notes (Streamlit)
- `RAG_WEB.py` — Full Streamlit web app wrapping the Day 10 RAG pipeline: upload any .txt file via browser, process it into chunks and embeddings, chat with it via a full conversation interface with retrieved chunks shown in an expander, conversation-aware follow-up questions using query expansion

**Concepts:** `st.file_uploader()`, `@st.cache_resource` for model caching, `st.expander()`, query expansion using chat history for context-aware retrieval, debugging multi-turn RAG conversations

---

### Day 12: Deployment — Live on Streamlit Cloud
- `RAG_WEB.py` deployed to Streamlit Community Cloud — **publicly accessible, free, no setup needed for users**
- Added `requirements.txt` for dependency management
- Configured Streamlit secrets for secure API key handling (no .env file in production)

**Live URL:** [Chat With Your Notes →](your-streamlit-url-here)

**Concepts:** Streamlit Community Cloud deployment, `requirements.txt` best practices, secrets management in production (vs .env locally), GitHub push protection for secret scanning, rotating exposed API keys

---

## 📈 Progress Tracker

| Day | Project | Status |
|-----|---------|--------|
| 1-2 | Hello AI + Chatbot | ✅ |
| 3 | REST APIs + Study Assistant | ✅ |
| 4 | Quiz Generator (structured output) | ✅ |
| 5 | Document Reader (file handling) | ✅ |
| 6 | Streamlit Web App | ✅ |
| 7 | Persistence + Quiz Web App | ✅ |
| 8 | Prompt Chaining Pipeline | ✅ |
| 9 | Embeddings + Semantic Search | ✅ |
| 10 | Mini RAG (terminal) | ✅ |
| 11 | RAG Web App (Streamlit) | ✅ |
| 12 | Deployed to Streamlit Cloud | ✅ |
| 13+ | AI Agents with tool use | 🔄 In progress |

## 🎯 Roadmap

- [ ] AI agents with tool use
- [ ] ChromaDB vector database for scaling RAG
- [ ] PDF support for RAG
- [ ] Fine-tuning basics
- [ ] Portfolio polish + more live demos

## 🚀 Setup

```bash
git clone https://github.com/Adityapanchal09/ai-engineer-journey.git
cd ai-engineer-journey
pip install -r APPS_WITH_UI/requirements.txt
echo "GROQ_API_KEY=your-key-here" > .env
```

Run any script with `python <filename>.py` or Streamlit apps with `streamlit run <filename>.py`

## 👤 Author

**Aditya Panchal**
B.Tech CSE/AI Student | Building toward AI Engineering
[GitHub](https://github.com/Adityapanchal09)

---

*This repo is updated daily as part of a structured 5-phase AI Engineering roadmap.*