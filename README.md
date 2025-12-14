<img width="1920" height="1024" alt="App page main" src="https://github.com/user-attachments/assets/dec82e9c-79ed-46be-849f-c8b7aa6285d4" />

**App Live Demo:** :--

https://github.com/user-attachments/assets/ef5f35fc-e42a-40b1-8f05-c3fb26a35afd


# 🔬 AI Researcher Agent / AI Research Saathi Agent 🤖

> **Discover cutting‑edge research papers from arXiv with the power of AI**

🚀 **Live App:** [https://ai-research-saathi-agent.streamlit.app/](https://ai-research-saathi-agent.streamlit.app/)

---

## 📌 Project Announcement

🎉 **Today I built a new end‑to‑end AI project – *AI Researcher Agent (AI Research Saathi Agent)***.

This project is an **AI‑powered research assistant** designed for students, researchers, and AI enthusiasts. It helps users **search, analyze, summarize, and interact with research papers from arXiv** using both **offline AI logic** and **multiple LLM providers**.

The app follows a **production‑grade architecture** with a FastAPI backend and a Streamlit frontend, deployed independently and connected via secure APIs.

---

## 🎯 Purpose & Vision

Research papers are powerful but time‑consuming to read. This app aims to:

* 🔍 Quickly **search relevant arXiv papers** by topic
* 🧠 Provide **AI‑generated summaries & key insights**
* 💬 Enable **chat‑based Q&A** on individual papers
* 👶 Support **ELI5 (Explain Like I’m 5)** explanations
* 🔌 Work **offline** or with **multiple LLM providers**
* 📚 Help users **build reading lists & alerts**

The goal is to act as a **personal AI research companion**.

---

## 🧱 High‑Level Architecture

```
[ Streamlit Frontend ]  →  [ FastAPI Backend ]  →  [ arXiv API ]
           |                     |
           |                     └─ AI Services (Offline / OpenAI / Groq / Anthropic / Gemini)
           |
           └─ UI, Filters, Chat, Summaries, Reading List
```

### 🔹 Frontend

* **Streamlit (streamlit_app.py)**
* Deployed on **Streamlit Cloud**

### 🔹 Backend

* **FastAPI (server.py)**
* Deployed on **Render**

---

## ⚙️ Core Components Explained

### 1️⃣ FastAPI Backend (`server.py`)

The backend exposes clean REST APIs consumed by the Streamlit frontend.

#### 🔗 Available Endpoints

* **`GET /health`**
  Health check endpoint to verify backend availability.

* **`GET /search`**
  Searches arXiv using a topic query and returns parsed paper entries.

* **`POST /summarize`**
  Generates AI summaries of papers.

  * Modes: `default`, `eli5`
  * Providers: `offline`, `openai`, `groq`, `anthropic`, `gemini`

* **`POST /chat`**
  Chat with a research paper using its abstract/context.

  * Maintains conversation history (client‑side)

The backend uses **LangChain tool wrappers** for structured integration.

---

### 2️⃣ arXiv Integration (`arxiv_tool.py`)

This module handles all arXiv interactions.

#### 🔍 Search Flow

* Normalizes keywords (`AND`, `OR`, `NOT`)
* Builds arXiv Atom API query
* Fetches XML response
* Parses and extracts:

  * Title
  * Abstract
  * Authors
  * Categories
  * PDF link
  * Published & updated dates

#### 🧰 LangChain Tool

```python
@tool
def arxiv_search(topic):
    return {"entries": [...]}
```

This allows future agent‑based extensions.

---

### 3️⃣ AI Services Layer (`ai_services.py`)

This is the **brain of the application**.

#### 📴 Offline AI (No API Key Required)

* **Summarization**

  * Sentence splitting
  * Token frequency scoring
  * Top‑sentence extraction
  * Key insight heuristics

* **ELI5 Mode**

  * Simplifies vocabulary
  * Shortens long sentences

* **Offline Chat**

  * Finds sentences with highest keyword overlap
  * Context‑aware responses

#### 🌐 Online LLM Providers (Optional)

If API keys are available, the app seamlessly switches to:

* OpenAI
* Groq
* Anthropic
* Google Gemini

All LLM responses are **normalized** into:

```json
{
  "summary": "...",
  "key_insights": ["..."],
  "bullets": ["..."]
}
```

Fallback logic ensures the app **always works**, even offline.

---

### 4️⃣ Streamlit Frontend (`streamlit_app.py`)

The frontend provides a **polished, interactive research UI**.

#### 🧭 Sidebar Features

* Backend health check
* Provider selection (offline / LLMs)
* ELI5 toggle
* Temperature slider (UI‑only)
* Runtime API key input
* Max results selector
* Popular topic buttons
* Alerts & Reading List (persisted in `alerts_store.json`)
* Advanced filters:

  * Date range
  * Author keyword
  * Categories
  * Sorting

#### 🖥️ Main Interface

* Search input → calls `/search`
* Results rendered as **paper cards**
* Client‑side filtering & sorting

Each paper supports:

* 🧠 **AI Summary** → `/summarize`
* 💬 **Chat with Paper** → `/chat`
* 📥 **Save to Reading List**
* 📄 **PDF Link**

#### ✨ Extra Features

* Streaming word‑by‑word chat rendering
* JSON & TXT export of results
* Personalized recommendations (keyword overlap)
* Side‑by‑side paper comparison
* Welcome cards & feature highlights
* Footer with developer credit

---

### 5️⃣ CLI Tool (`ai_researcher.py`)

A lightweight command‑line interface to search arXiv directly.

```bash
python ai_researcher.py "transformer models" --max-results 5
```

Outputs clean, formatted JSON in the terminal.

---

### 6️⃣ Testing (`test_api.py`)

Simple automated checks using `requests`:

* `/health`
* `/search` with sample topics

Ensures backend reliability.

---

## 🗂️ Data Models

### 📄 Paper Entry

```json
{
  "title": "...",
  "summary": "...",
  "authors": ["..."],
  "categories": ["..."],
  "pdf": "...",
  "published": "...",
  "updated": "..."
}
```

### 🧠 Summarization Response

```json
{
  "summary": "...",
  "key_insights": ["..."],
  "bullets": ["..."]
}
```

### 💬 Chat Response

```json
{
  "answer": "..."
}
```

---

## ▶️ Running Locally

### Backend

```bash
python -m uvicorn server:app --reload --host 127.0.0.1 --port 8001
```

### Frontend

```bash
streamlit run streamlit_app.py
```

### Test APIs

```bash
python test_api.py
```

---

## 📦 Tech Stack

* Python
* FastAPI
* Streamlit
* Uvicorn
* Requests
* LangChain (tool abstraction)
* arXiv API
* Optional LLM SDKs (OpenAI, Groq, Anthropic, Gemini)

---

## 🌟 Why This Project Matters

This project demonstrates:

* ✅ Real‑world **frontend–backend separation**
* ✅ API‑driven AI architecture
* ✅ Graceful offline → online AI fallback
* ✅ Clean modular design
* ✅ Production deployment (Render + Streamlit Cloud)

It’s not just a demo — it’s a **scalable AI research platform**.

---

## 👨‍💻 Developer

**Abhishek Kumar (Abhi Yadav)**
AI & Data Science Aspirant | Building practical AI products

---

⭐ If you like this project, don’t forget to **star the repo** and share feedback!
