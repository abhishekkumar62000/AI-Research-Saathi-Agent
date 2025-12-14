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

---

## 🧠 LangGraph Binary Tree – How the App Works (User Journey)

Below is a **LangGraph-style Binary Tree representation** explaining **how a new user starts and interacts with the AI Researcher Agent**. This shows decision points, flow control, and fallback logic clearly.

```
                          👤 New User Opens App
                                   │
                                   ▼
                       🖥️ Streamlit Frontend Loads
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          🔍 User Enters Search Topic        ❌ No Topic Entered
                    │                             │
                    ▼                             ▼
        ▶️ Call /search API (FastAPI)     🎴 Show Welcome + Tips
                    │
                    ▼
        🌐 arXiv API Fetch (Atom XML)
                    │
                    ▼
        📄 Parsed Research Papers Returned
                    │
                    ▼
          🧾 Display Paper Cards (UI)
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
🧠 User Clicks "AI Summary"   💬 User Clicks "Chat"
        │                       │
        ▼                       ▼
▶️ Call /summarize API     ▶️ Call /chat API
        │                       │
        ▼                       ▼
┌───────────────┐        ┌───────────────┐
│ LLM Provider? │        │ LLM Provider? │
└───────┬───────┘        └───────┬───────┘
        │YES                    │YES
        ▼                       ▼
 🤖 Online LLM Response     🤖 Online LLM Response
        │                       │
        └──────────┬────────────┘
                   ▼
          🔄 Normalize AI Output
                   │
                   ▼
        🧠 Summary / Answer Returned
                   │
                   ▼
          🖥️ Render in Streamlit UI
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
📥 Save to Reading List   📤 Export / Compare
        │                     │
        ▼                     ▼
🔔 Alerts & Recommender   🔚 User Session Ends
```

---

### 🧩 Binary Decision Logic Explained

* **Decision Node 1:** Did the user enter a search topic?

  * ❌ No → Show welcome cards and guidance
  * ✅ Yes → Proceed to arXiv search

* **Decision Node 2:** Does the user want a summary or chat?

  * Summary → `/summarize`
  * Chat → `/chat`

* **Decision Node 3:** Is an LLM provider configured?

  * ❌ No → Offline AI logic (heuristics)
  * ✅ Yes → OpenAI / Groq / Anthropic / Gemini

This structure ensures **fault tolerance**, **offline usability**, and **scalable agent-based reasoning**, which aligns perfectly with **LangGraph design philosophy**.

---

### 🧠 Why This Fits LangGraph Concepts

* 🔁 **Stateful Flow**: Session state + chat history
* 🌳 **Graph Nodes**: Search → Summarize / Chat
* 🔀 **Conditional Edges**: LLM vs Offline
* 🛑 **Safe Fallbacks**: App always responds
* 🧩 **Composable Tools**: arXiv search as a tool node

This binary-tree-like LangGraph flow makes the app **agent-ready** for future extensions like multi-agent research, critique agents, or paper comparison agents.

---

## ❤️ **Made with Passion by Abhishek Yadav & Open-Source Contributors!** 🚀✨


<h1 align="center">© LICENSE <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Symbols/Check%20Box%20With%20Check.webp" alt="Check Box With Check" width="25" height="25" /></h1>

<table align="center">
  <tr>
     <td>
       <p align="center"> <img src="https://github.com/malivinayak/malivinayak/blob/main/LICENSE-Logo/MIT.png?raw=true" width="80%"></img>
    </td>
    <td> 
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/> <br> 
This project is licensed under <a href="./LICENSE">MIT</a>. <img width=2300/>
    </td>
  </tr>
</table>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">



 
 <hr>

<div align="center">
<a href="#"><img src="assets/githubgif.gif" width="150"></a>
	
### **Thanks for checking out my GitHub Profile!**  

 ## 💌 Sponser

  [![BuyMeACoffee](https://img.buymeacoffee.com/button-api/?text=Buymeacoffee&emoji=&slug=codingstella&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/abhishekkumar62000)

## 👨‍💻 Developer Information  
**Created by:** **Abhishek Kumar**  
**📧 Email:** [abhiydv23096@gmail.com](mailto:abhiydv23096@gmail.com)  
**🔗 LinkedIn:** [Abhishek Kumar](https://www.linkedin.com/in/abhishek-kumar-70a69829a/)  
**🐙 GitHub Profile:** [@abhishekkumar62000](https://github.com/abhishekkumar62000)

<p align="center">
  <img src="https://github.com/user-attachments/assets/6283838c-8640-4f22-87d4-6d4bfcbbb093" width="120" style="border-radius: 50%;">
</p>
</div>  


`Don't forget to give A star to this repository ⭐`


`👍🏻 All Set! 💌`

</div>

---
