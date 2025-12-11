# AI Researcher Agent Pro 🔬 🤖

An intelligent, **AI-powered** research assistant that searches, analyzes, and summarizes academic papers from arXiv with cutting-edge AI capabilities.

## 🌟 Features

### 🤖 AI-Powered Features (NEW!)
- **AI Paper Summarization** - Generate comprehensive summaries in seconds
- **Interactive Chat with Papers** - Ask questions and get intelligent answers
- **Key Insights Extraction** - Get structured insights automatically
- **Multi-Provider AI Support** - Choose from Groq (FREE!), OpenAI, Gemini, or Claude

### 🎨 Core Features
- **Beautiful Streamlit Web Interface** - Modern, interactive web UI with gradient themes
- **FastAPI REST API** - Modern, fast web API with automatic documentation
- **arXiv Integration** - Search and retrieve academic papers from arXiv
- **CLI Tool** - Command-line interface for quick searches
- **Auto-generated Documentation** - Interactive Swagger UI at `/docs`
- **LangChain Integration** - Built using LangChain tools framework
- **📊 Search Statistics** - Track your searches, papers, and AI summaries
- **📥 Export Options** - Download results, summaries as JSON, TXT, or Markdown

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip or uv package manager

### Installation

1. Clone or navigate to the repository:
```bash
cd "AI Researcher Agent"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or if using uv:
```bash
uv sync
```

### Running the Application

#### Option 1: Streamlit Web Interface (Recommended) 🎨

The easiest way to use the AI Researcher Agent is through the beautiful Streamlit web interface.

**Step 1:** Start the FastAPI backend server (required):
```bash
python -m uvicorn server:app --reload --host 127.0.0.1 --port 8001
```

**Step 2:** In a new terminal, start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

The Streamlit app will open automatically in your browser at:
- **Streamlit UI**: http://localhost:8501

**Features:**
- 🎨 Beautiful gradient-themed interface
- 🔍 Interactive search with real-time results
- 📊 Search statistics tracking
- 🔥 Popular topics quick access
- 📥 Export results as JSON or TXT
- 📱 Responsive design

#### Option 2: FastAPI Web Server (API Only)

Start the server:
```bash
python -m uvicorn server:app --reload --host 127.0.0.1 --port 8001
```

The API will be available at:
- **API Base**: http://127.0.0.1:8001
- **Interactive Docs**: http://127.0.0.1:8001/docs
- **Alternative Docs**: http://127.0.0.1:8001/redoc

#### Option 2: Command Line Interface

Search directly from the command line:
```bash
python ai_researcher.py "machine learning" --max-results 5
```

## 📚 API Endpoints

### GET /health
Health check endpoint to verify the server is running.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /search
Search for academic papers on arXiv.

**Parameters:**
- `topic` (required): The research topic to search for
- `max_results` (optional): Maximum number of results to return (default: 5, max: 50)

**Example Request:**
```bash
curl "http://127.0.0.1:8001/search?topic=quantum+computing&max_results=3"
```

**Example Response:**
```json
{
  "entries": [
    {
      "title": "Quantum Computing: A Gentle Introduction",
      "summary": "This paper provides an introduction to quantum computing...",
      "authors": ["John Doe", "Jane Smith"],
      "categories": ["quant-ph", "cs.ET"],
      "pdf": "https://arxiv.org/pdf/2301.12345v1"
    }
  ]
}
```

## 🧪 Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

This will test:
- Health endpoint
- Search endpoint with multiple topics

## 📁 Project Structure

```
AI Researcher Agent/
├── server.py           # FastAPI application
├── ai_researcher.py    # CLI tool
├── arxiv_tool.py       # arXiv search functionality
├── test_api.py         # API testing script
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

## 🛠️ Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **LangChain** - Framework for developing LLM applications
- **Requests** - HTTP library for API calls
- **Uvicorn** - ASGI server for running FastAPI
- **arXiv API** - Academic paper database

## 🔧 Development

The server runs in development mode with auto-reload enabled. Any changes to the code will automatically restart the server.

### Key Components

1. **arxiv_tool.py**: Core functionality for searching arXiv
   - `search_arxiv_papers()`: Queries the arXiv API
   - `parse_arxiv_xml()`: Parses XML responses
   - `arxiv_search`: LangChain tool wrapper

2. **server.py**: FastAPI application
   - Health check endpoint
   - Search endpoint with validation

3. **ai_researcher.py**: CLI interface
   - Argument parsing
   - Pretty-printed JSON output

## 📝 Example Usage

### Python Script
```python
import requests

response = requests.get(
    "http://127.0.0.1:8001/search",
    params={"topic": "neural networks", "max_results": 3}
)

papers = response.json()["entries"]
for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"PDF: {paper['pdf']}\n")
```

### Command Line
```bash
# Search for papers about deep learning
python ai_researcher.py "deep learning" --max-results 10

# Search for papers about reinforcement learning
python ai_researcher.py "reinforcement learning"
```

## 🐛 Bug Fixes

- ✅ Fixed space character handling in search queries
- ✅ Proper URL encoding for arXiv API requests
- ✅ Validation error handling

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using FastAPI and LangChain**
