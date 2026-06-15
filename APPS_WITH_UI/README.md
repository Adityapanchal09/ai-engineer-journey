# 📚 AI Study Assistant

An interactive, web-based AI tutor built with Python, Streamlit, and Groq's LLaMA 3.3 70B model. Choose any subject and chat with a personalized AI tutor that explains concepts using simple analogies.

![AI Study Assistant Screenshot](![alt text](image.png))

## Features

- 💬 **ChatGPT-style chat interface** — clean message bubbles for user and AI
- 🎯 **Subject-aware tutoring** — set any subject (History, Operating Systems, DAA, etc.) and the AI adapts its persona
- 🧠 **Persistent conversation memory** — full chat history maintained across the session
- ⚡ **Fast responses** — powered by Groq's LLaMA 3.3 70B (low latency inference)
- 🔄 **New session reset** — switch subjects and start fresh anytime

## Tech Stack

- **Python 3.12**
- **Streamlit** — web UI framework
- **Groq API** — LLaMA 3.3 70B Versatile model
- **python-dotenv** — environment variable management

## How It Works

1. Enter a subject in the sidebar (e.g. "Operating Systems")
2. Click **Start new session**
3. Ask questions in the chat box
4. The AI responds as an expert tutor in that subject, using analogies to explain concepts simply
5. Conversation history is preserved as you ask follow-up questions

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Adityapanchal09/ai-engineer-journey.git
cd ai-engineer-journey

# Install dependencies
pip install streamlit groq python-dotenv

# Add your Groq API key
echo "GROQ_API_KEY=your-key-here" > .env

# Run the app
streamlit run study_app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

## Example Use Cases

- Exam prep — ask conceptual questions about any subject
- Quick explanations — get analogies for tricky topics
- Subject switching — set subject to your current course and study interactively

## Project Structure

```
ai-engineer-journey/
├── study_app.py       # Main Streamlit application
├── .env                # API key (not committed)
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Add quiz generation mode within the same app
- [ ] Add document upload for context-aware Q&A
- [ ] Deploy to Streamlit Community Cloud for a live demo link
- [ ] Add export chat history to PDF/text

## Author

Built by [Aditya Panchal](https://github.com/Adityapanchal09) as part of a structured AI Engineering learning journey.

---

*Part of the [AI Engineer Journey](https://github.com/Adityapanchal09/ai-engineer-journey) — a daily learning log building toward AI Engineering expertise.*