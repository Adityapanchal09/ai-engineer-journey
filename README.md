# 🤖 AI Engineer Journey

A daily learning log documenting my path to becoming an AI Engineer — building real, working projects using Python, the Groq API (LLaMA 3.3 70B), REST APIs, and Streamlit.

## 🛠️ Tech Stack

- **Python 3.12**
- **Groq API** (LLaMA 3.3 70B Versatile)
- **Streamlit** — web UI
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
- `quiz_app.py` — Full interactive quiz web app: AI-generated MCQs, clickable radio options, instant feedback with explanations, score tracking, and a persistent results log saved to `quiz_log.json`

**Concepts:** JSON file persistence (`json.dump`/`json.load`), `os.path.exists()` safety checks, multi-variable `session_state` state machines, `st.radio`, conditional UI flow (question → feedback → next), debugging real Streamlit rerun bugs

---

### Day 8: Prompt Chaining — Notes Processing Pipeline
- `notes_pipeline.py` — Takes raw, messy/unstructured notes and runs them through a 4-step AI pipeline: clean grammar → summarize → extract key points (JSON) → generate exam questions (JSON), saving the full result to `pipeline_output.json`

**Concepts:** Prompt chaining (output of one AI call feeding into the next), reusable `ask()` helper function, multi-step pipelines, choosing the right upstream input for each step, debugging `json.dump()` argument order

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
| 9+ | Embeddings, vector databases, RAG | 🔄 In progress |

## 🎯 Roadmap

- [ ] Embeddings & vector databases
- [ ] RAG — chat with PDFs
- [ ] AI agents with tool use
- [ ] Deploy apps to Streamlit Community Cloud
- [ ] Fine-tuning basics
- [ ] Portfolio polish + live demo links

## 🚀 Setup

```bash
git clone https://github.com/Adityapanchal09/ai-engineer-journey.git
cd ai-engineer-journey
pip install -r requirements.txt
echo "GROQ_API_KEY=your-key-here" > .env
```

Run any script with `python <filename>.py` or Streamlit apps with `streamlit run <filename>.py`

## 👤 Author

**Aditya Panchal**
B.Tech CSE/AI Student | Building toward AI Engineering
[GitHub](https://github.com/Adityapanchal09)

---

*This repo is updated daily as part of a structured 5-phase AI Engineering roadmap.*