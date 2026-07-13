# 🤖 AI Engineer Journey

A daily learning log documenting my path to becoming an AI Engineer — building real, working projects using Python, the Groq API (qwen/qwen3-27b), REST APIs, Streamlit, embeddings, RAG, AI Agents, and FastAPI.

## 🌐 Live Demos
| App | URL |
|-----|-----|
| 📄 Chat With Your Notes (RAG) | [Try it →](https://ai-engineer-journey-my-mini-rag.streamlit.app/) |
| 🤖 AI Agent (Multi-tool) | [Try it →](https://ai-engineer-journey-aiagent.streamlit.app/) |

## 🛠️ Tech Stack

- **Python 3.12**
- **Groq API** (qwen/qwen3-27b)
- **FastAPI** — production AI backend
- **LangChain** — LLM application framework
- **Streamlit** — web UI + deployment
- **sentence-transformers** — local embeddings
- **ddgs** — DuckDuckGo web search
- **python-dotenv** — environment management
- **requests / httpx** — REST API calls

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
- `study_app.py` (upgraded) — Chat history saved to `chat_history.json` and reloaded automatically on restart
- `quiz_app.py` — Full interactive quiz web app with AI-generated MCQs, clickable radio options, instant feedback, score tracking, and persistent results log

**Concepts:** JSON file persistence, `os.path.exists()` safety checks, multi-variable `session_state` state machines, conditional UI flow

---

### Day 8: Prompt Chaining — Notes Processing Pipeline
- `notes_pipeline.py` — Takes raw messy notes through a 4-step AI pipeline: clean grammar → summarize → extract key points (JSON) → generate exam questions (JSON)

**Concepts:** Prompt chaining, reusable `ask()` helper function, multi-step pipelines

---

### Day 9: Embeddings + Semantic Search
- `embedd_compare.py` — Compares meaning similarity using cosine similarity
- `semantic_search.py` — Natural-language search over study notes by MEANING, not keywords

**Concepts:** Sentence embeddings (`sentence-transformers`), vectors as meaning, cosine similarity, semantic vs keyword search

---

### Day 10: Mini RAG — Chat With Your Notes (Terminal)
- `mini_rag.py` — Complete RAG pipeline from scratch: chunk → embed → retrieve → answer grounded in context only, with similarity threshold to prevent hallucination

**Concepts:** Document chunking, batch embedding, semantic retrieval, context-grounded generation, hallucination prevention

---

### Day 11: RAG Web App — Chat With Your Notes (Streamlit)
- `RAG_WEB.py` — Full Streamlit web app: upload any .txt file, process into chunks and embeddings, chat with full conversation interface, retrieved chunks shown in expander, conversation-aware follow-up questions

**Concepts:** `st.file_uploader()`, `@st.cache_resource`, `st.expander()`, query expansion using chat history

---

### Day 12: Deployment — RAG App Live on Streamlit Cloud
- `RAG_WEB.py` deployed to Streamlit Community Cloud — publicly accessible, free, no setup needed

**Live URL:** [Chat With Your Notes →](https://ai-engineer-journey-my-mini-rag.streamlit.app/)
<img width="1853" height="894" alt="image" src="https://github.com/user-attachments/assets/7e360b0c-01d0-4951-b4dd-f69e426a004a" />

**Concepts:** Streamlit Cloud deployment, `requirements.txt`, secrets management, GitHub push protection, rotating exposed API keys

---

### Day 13: AI Agents — First Agent with Tool Use
- `simple_agent.py` — Working AI agent with 3 tools: calculator, word counter, file reader. Agent autonomously decides which tool to call using the ReAct pattern

**Concepts:** AI agents, tool registry, ReAct loop (Reason → Act → Observe), tool calling, JSON-based tool call parsing, max iteration safety limit

---

### Day 14: Expanded Agent — 6 Tools Including REST API + Semantic Search
- `AGENT.py` (expanded) — Agent with 6 tools: calculator, word counter, file reader, joke fetcher (REST API), AI summarizer, semantic notes search. Successfully chains multiple tools in sequence

**Concepts:** REST API as agent tool, prompt chaining inside tools, embeddings inside tools, multi-tool chaining

---

### Day 15: Agent Memory — Short-term + Long-term Persistence
- `AGENT.py` (with memory) — Agent with two memory systems: short-term (shared conversation history) and long-term (JSON file persistence across restarts — agent recalls name and preferences without being told again)

**Concepts:** Short-term vs long-term agent memory, JSON-based persistent memory, `save_memory`/`recall_memory` tools, multi-tool JSON response parsing

---

### Day 16: Web Search Tool — Agent Goes Online
- `AGENT.py` (with web search) — Agent gains live internet access via DuckDuckGo. Can fetch current AI news, search documentation, answer real-time questions. Total: 9 tools

**Concepts:** DuckDuckGo search (`ddgs`), rate limiting with `time.sleep()`, safe result parsing with `.get()`

---

### Day 17: AI Agent Web UI (Streamlit)
- `agent_app.py` — Full Streamlit web interface: chat bubbles, "Tools used" expander, sidebar memory panel updating in real time, clear memory button, all 9 tools from browser

**Concepts:** Terminal→Streamlit conversion framework (print→st.write, input→st.chat_input, globals→session_state), `@st.cache_resource`, tool name consistency

---

### Day 18: Agent App Deployed + Product of Array Except Self
- `agent_app.py` deployed to Streamlit Community Cloud — second live AI product

**Live URL:** [AI Agent →](https://ai-engineer-journey-aiagent.streamlit.app/)
<img width="1855" height="882" alt="image" src="https://github.com/user-attachments/assets/0df70034-b36f-4c00-8d23-799207d051c9" />

**Concepts:** Multi-app deployment, separate `requirements.txt` per app, per-folder `.streamlit/secrets.toml`, prefix/suffix product pattern (DSA)

---

### Day 19: Valid Palindrome — Two Pointers Pattern (DSA)
- First Two Pointers problem — a brand new pattern after 6 days of hash maps
- Two pointer approach: left pointer from start, right pointer from end, skip non-alphanumeric, compare case-insensitively until pointers meet

**Concepts:** Two Pointers pattern, `.isalnum()`, `.lower()`, O(n) time O(1) space solution, inner while loops for skipping

---

### Day 20: Two Sum II + Three Sum — Two Pointers (DSA)
- **Two Sum II** — sorted array, two pointers from both ends, move based on sum comparison vs target. O(n) time, O(1) space
- **Three Sum** — sort array, fix one element with outer loop, use two pointers on the remainder to find pairs that sum to zero. Skip duplicates to avoid repeated triplets

**Concepts:** Two pointers on sorted arrays, duplicate skipping, reducing 3Sum to 2Sum, O(n²) time complexity, combining sort + two pointers

---

### Day 21: FastAPI Intro — AI Engineer API
- `main.py` — First FastAPI app serving AI via HTTP endpoints: `/chat` POST endpoint accepting JSON, Pydantic request validation, Groq integration, auto-generated Swagger docs at `/docs`

**Concepts:** FastAPI basics, `@app.post()` / `@app.get()` decorators, Pydantic `BaseModel` for request validation, type annotations, `uvicorn` server, automatic OpenAPI docs, HTTP status codes, `HTTPException`

---

### Day 22: Async FastAPI + Streaming Responses
- `main.py` — Production-grade AI API with two endpoint types: async regular chat and real-time streaming
- `test_client.py` — Async test client using `httpx` to verify both endpoints

**Endpoints:**
- `POST /chat` — full async response, returns complete JSON when Groq finishes
- `POST /chat/stream` — streams tokens to client in real-time as Groq generates them
- `GET /health` — health check endpoint

**Concepts:** `async/await` in FastAPI, `AsyncGroq` client, `StreamingResponse`, async generator functions (`yield`), `stream=True` in Groq API, `httpx.AsyncClient`, `aiter_text()` for reading streams, `asyncio.run()`, `flush=True` for real-time terminal output, difference between blocking vs non-blocking AI calls

---

### Day 23: FastAPI + Frontend Streaming Chat UI
- Built ChatGPT-style streaming chat UI served directly from FastAPI
- FastAPI `StaticFiles` serves the HTML/CSS/JS frontend
- Tokens stream in real-time via `fetch` + `ReadableStream` + `TextDecoder` loop on the frontend

**Concepts:** `StaticFiles` mounting in FastAPI, `FileResponse` for serving HTML, browser `ReadableStream`, `TextDecoder`, streaming fetch pattern, frontend-backend integration without a separate framework

---

### Day 24: Multi-turn Conversation Memory
- `main.py` (upgraded) — Chat app now remembers the full conversation across turns
- Backend maintains a `conversation_history` list that grows with every user + assistant turn
- Full history sent to Groq on every request so responses are context-aware

**Endpoints added:**
- `POST /reset` — clears conversation history (New Chat)
- `GET /history` — returns full conversation history as JSON for debugging

**DSA — Sliding Window begins:**
- **Best Time to Buy and Sell Stock** (Easy) — first Sliding Window problem
- Two pointer approach: `left` = buy day, `right` = sell day, move `left` when cheaper price found, track `max_profit` throughout
- Key insight: global `min`/`max` don't respect order — buy must happen before sell

**Concepts:** Global state in FastAPI, `finally` block to save streamed response after completion, accumulating streamed tokens server-side, variable-size sliding window pattern, O(n) single-pass stock profit

---

### Day 25: AI Personality Switcher + Longest Substring Without Repeating Characters
- `index.html` (upgraded) — Added personality dropdown to the chat UI with 5 selectable AI modes
- `main.py` (upgraded) — Added `PERSONALITIES` dict and `GET /personalities` endpoint
- Switching personality auto-resets conversation history so context doesn't bleed across modes

**Personalities added:**
- 🤖 Helpful Assistant — general purpose
- 🐍 Python Tutor — explains with code examples, highlights beginner mistakes
- 🔍 Code Reviewer — direct, finds bugs, suggests improvements
- 👶 ELI5 — simple words, analogies, fun examples
- 🏛️ Socratic Tutor — never gives answers, asks guiding questions instead

**DSA — Sliding Window #2:**
- **Longest Substring Without Repeating Characters** (Medium) — LeetCode 3
- Variable-size sliding window: `right` moves forward in `for` loop, `left` moves forward in inner `while` loop when duplicate found
- `seen` set tracks characters in current window, remove `s[left]` when shrinking
- Key insight: move `left` in a `while` loop, not just once — one step may not be enough to remove the duplicate

**Concepts:** `PERSONALITIES` dict as config, frontend dropdown → system prompt mapping in JS, auto-reset on personality switch, variable-size sliding window with `while` inner loop, O(n) time O(k) space where k = character set size

---

### Day 26: Skills Audit + Sliding Window Problems
- Conducted a full audit of Days 1–25 to identify gaps and plan next phases
- **DSA — Sliding Window #3 & #4:**
  - **Longest Repeating Character Replacement** (Medium) — LeetCode 424
  - **Permutation in String** (Medium) — LeetCode 567

**Gaps identified:** evals/testing, Docker deployment, advanced RAG, structured outputs (Pydantic), agent frameworks (LangGraph, CrewAI), LLM observability

**Concepts:** Sliding window with character frequency maps, `max()` on dict values, fixed-size window validation, anagram detection via window comparison, O(26n) ≈ O(n) frequency comparison

---

### Day 27: Job Post Analyzer — Structured Outputs with Pydantic + FastAPI
- `models.py` — Pydantic schema defining the full structured output: job title, company, experience level, skills, responsibilities, red flags, and summary
- `analyzer.py` — Groq integration with robust `clean_response()` to strip Qwen3 `<think>` blocks and extract pure JSON
- `main.py` — FastAPI backend serving both the `/analyze` POST endpoint and the frontend via `StaticFiles`
- `static/index.html` — Dark-themed single-page frontend: paste a job description, get fully parsed structured output rendered with skill tags, badges, and red flag highlights

**Key features:**
- `Optional` fields handle real-world messy job posts gracefully (missing salary, unnamed companies)
- `red_flags` field detects issues like unpaid trials, unrealistic experience demands, and vague compensation
- `clean_response()` handles Qwen3's `<think>` blocks with `re.DOTALL` regex + JSON boundary extraction (`find('{')` / `rfind('}')`)
- Full UI rendered from FastAPI itself — no separate frontend server needed

**DSA — Arrays & Hashing #7:**
- **Longest Consecutive Sequence** (Medium) — LeetCode 128
- Convert array to a `set` for O(1) lookups, only start counting from sequence starts (`num - 1` not in set)
- Each number visited at most twice — once in outer loop, once inside while — making it truly O(n)
- Key insight: a number is a sequence start only if its predecessor doesn't exist in the set

**Concepts:** Pydantic `BaseModel` for structured LLM output, `Optional[str] = None` vs required fields, `list[str]` typed fields, `json.loads()` → Pydantic validation pipeline, `re.sub()` with `re.DOTALL` for multi-line regex, JSON boundary extraction, `StaticFiles` + `FileResponse` in FastAPI, hash set sequence detection, O(n) amortized traversal

---

### Day 28: LangChain Fundamentals + Encode and Decode Strings
- `day28_langchain_basics.py` — Progressive LangChain exploration: basic LLM call → prompt templates → pipe chain → output parser → conversation memory

**LangChain components covered:**
- `ChatGroq` — wraps Groq API as a LangChain-compatible LLM object
- `ChatPromptTemplate` — reusable prompt with `{variable}` slots filled at runtime
- `prompt | llm | parser` — the canonical LangChain pipe chain pattern
- `StrOutputParser` — extracts plain string from `AIMessage` object automatically
- `MessagesPlaceholder` — slot in prompt template that accepts full chat history list
- `HumanMessage` / `AIMessage` — typed message objects replacing raw `{"role": "user", ...}` dicts
- Manual `chat_history` list — grows each turn, passed into chain via `invoke({...})`

**Key insight:** LangChain replaces what you built manually — `client.chat.completions.create()` becomes `ChatGroq`, message history dicts become typed objects, and multi-step pipelines become `prompt | llm | parser`

**DSA — Arrays & Hashing #8:**
- **Encode and Decode Strings** (Medium) — LeetCode 271
- Length-prefix encoding: store `len(word)#word` for each string, making delimiter unambiguous regardless of string contents
- Decode uses index `i` + `str.index('#', i)` to find length, then slices exactly that many chars after `#`
- Key insight: can't use simple delimiters like `","` since they may appear inside strings — length prefix is always unambiguous

**Concepts:** `ChatGroq`, `ChatPromptTemplate.from_messages()`, `MessagesPlaceholder`, pipe operator `|` for chaining, `StrOutputParser`, `HumanMessage`/`AIMessage` typed messages, length-prefix string encoding, `str.index(char, start)` for positional search, index-based while loop decoding, O(n) encode and decode

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
| 12 | RAG App Deployed | ✅ |
| 13 | AI Agent with Tool Use | ✅ |
| 14 | Expanded Agent (6 tools) | ✅ |
| 15 | Agent Memory (short + long term) | ✅ |
| 16 | Web Search Tool (9 tools total) | ✅ |
| 17 | Agent Web UI (Streamlit) | ✅ |
| 18 | Agent App Deployed (2nd live app) | ✅ |
| 19 | Valid Palindrome — Two Pointers | ✅ |
| 20 | Two Sum II + Three Sum — Two Pointers | ✅ |
| 21 | FastAPI Intro — AI Engineer API | ✅ |
| 22 | Async FastAPI + Streaming Responses | ✅ |
| 23 | FastAPI + Frontend Streaming Chat UI | ✅ |
| 24 | Multi-turn Memory + Sliding Window begins | ✅ |
| 25 | Personality Switcher + Longest Substring | ✅ |
| 26 | Skills Audit + Sliding Window #3 & #4 | ✅ |
| 27 | Job Post Analyzer — Structured Outputs + Pydantic + FastAPI | ✅ |
| 28 | LangChain Fundamentals + Encode and Decode Strings | ✅ |

## 🧩 DSA Track (NeetCode 150)

| Day | Problem | Pattern | Difficulty | Status |
|-----|---------|---------|------------|--------|
| 13 | Contains Duplicate | Hash Set | Easy | ✅ |
| 14 | Valid Anagram | Hash Map | Easy | ✅ |
| 15 | Two Sum | Hash Map | Easy | ✅ |
| 16 | Group Anagrams | Hash Map + defaultdict | Medium | ✅ |
| 17 | Top K Frequent Elements | Hash Map + Bucket Sort | Medium | ✅ |
| 18 | Product of Array Except Self | Prefix + Suffix | Medium | ✅ |
| 19 | Valid Palindrome | Two Pointers | Easy | ✅ |
| 20 | Two Sum II | Two Pointers | Medium | ✅ |
| 20 | Three Sum | Two Pointers | Medium | ✅ |
| 22 | Container With Most Water | Two Pointers | Medium | ✅ |
| 23 | Trapping Rain Water | Two Pointers | Hard | ✅ |
| 24 | Best Time to Buy and Sell Stock | Sliding Window | Easy | ✅ |
| 25 | Longest Substring Without Repeating Characters | Sliding Window | Medium | ✅ |
| 26 | Longest Repeating Character Replacement | Sliding Window | Medium | ✅ |
| 26 | Permutation in String | Sliding Window | Medium | ✅ |
| 27 | Longest Consecutive Sequence | Arrays & Hashing | Medium | ✅ |
| 28 | Encode and Decode Strings | Arrays & Hashing | Medium | ✅ |

## 🎯 Roadmap

- [x] Two Pointers problems (Two Sum II, 3Sum, Container with Most Water, Trapping Rain Water)
- [x] FastAPI — build AI backend
- [x] Async + Streaming FastAPI endpoints
- [x] Frontend streaming chat UI
- [x] Multi-turn conversation memory
- [x] AI Personality Switcher
- [x] Sliding Window — 4/6 done
- [x] Structured Outputs with Pydantic
- [x] LangChain fundamentals — prompt templates, chains, memory
- [ ] Arrays & Hashing — 1 problem remaining (Valid Sudoku)
- [ ] Sliding Window — remaining 2 problems
- [ ] LangChain RAG pipeline
- [ ] LangGraph intro
- [ ] FastAPI Authentication (API keys)
- [ ] Docker — containerize AI API
- [ ] ChromaDB vector database for scaling RAG
- [ ] PDF support for RAG
- [ ] Fine-tuning basics
- [ ] Portfolio polish

## 🚀 Setup

```bash
git clone https://github.com/Adityapanchal09/ai-engineer-journey.git
cd ai-engineer-journey
pip install -r APPS_WITH_UI/requirements.txt
echo "GROQ_API_KEY=your-key-here" > .env
```

Run any script with `python <filename>.py` or Streamlit apps with `streamlit run <filename>.py`

For the FastAPI apps:
```bash
cd day27-job-analyzer
pip install fastapi uvicorn groq pydantic python-dotenv aiofiles
uvicorn main:app --reload
```

For LangChain:
```bash
cd day28-langchain
pip install langchain langchain-groq python-dotenv
python day28_langchain_basics.py
```

## 👤 Author

**Aditya Panchal**
B.Tech CSE/AI Student | Building toward AI Engineering
[GitHub](https://github.com/Adityapanchal09/ai-engineer-journey)

---

*This repo is updated daily as part of a structured 5-phase AI Engineering roadmap.*