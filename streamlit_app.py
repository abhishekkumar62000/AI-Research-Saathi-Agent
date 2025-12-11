"""
AI Researcher Agent - Streamlit Web Interface
A beautiful web interface for searching academic papers from arXiv
"""

import streamlit as st
import requests
import os
from datetime import datetime
import json
import pathlib
import base64

# Page configuration
st.set_page_config(
    page_title="AI Researcher Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Dark Neon Theme */
    :root {
        --bg-0: #0b1220; /* deep navy */
        --bg-1: #0f172a; /* slate */
        --txt-0: #e5e7eb; /* light text */
        --neon-1: #22d3ee; /* cyan */
        --neon-2: #a78bfa; /* purple */
        --neon-3: #34d399; /* green */
        --neon-4: #f472b6; /* pink */
        --grad-1: linear-gradient(135deg, #0ea5e9 0%, #a78bfa 50%, #34d399 100%);
    }

    body, .block-container { background: var(--bg-0); color: var(--txt-0); }
    .stApp { background: radial-gradient(circle at 10% 10%, #0b1220, #0f172a 50%, #0b1220 100%); }

    /* Global inputs and sidebar styling */
    section[data-testid="stSidebar"] > div { background: rgba(2,6,23,0.6); border-left: 2px solid rgba(34,211,238,0.3); }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label { color: #cbd5e1 !important; }
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] div,
    .stMultiSelect div[data-baseweb="select"] div,
    .stSlider,
    .stNumberInput input {
        background: rgba(15,23,42,0.65) !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        border-radius: 10px !important;
    }
    .stSelectbox [data-testid="stMarkdownContainer"] { color: #e5e7eb; }
    div[data-baseweb="select"] > div { background: rgba(2,6,23,0.7); }
    div[data-baseweb="select"] svg { fill: #a78bfa; }
    .stSlider [data-testid="stTickBar"] div { background: linear-gradient(90deg, #22d3ee, #a78bfa); height: 4px; }
    .stSlider [data-testid="stThumbValue"] { background: #0ea5e9; color: #0b1220; border-radius: 8px; }

    /* Streamlit buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--neon-1), var(--neon-2));
        color: #0b1220; border: none; border-radius: 12px; padding: 0.6rem 1.1rem; font-weight: 800;
        box-shadow: 0 8px 20px rgba(167,139,250,0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover { transform: translateY(-1px) scale(1.02); box-shadow: 0 12px 28px rgba(34,211,238,0.35); }
    .stDownloadButton > button { background: linear-gradient(135deg, var(--neon-3), var(--neon-1)); color: #0b1220; border-radius: 12px; font-weight: 800; }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] { border: 1px solid rgba(167,139,250,0.25); background: rgba(16,24,40,0.6); border-radius: 14px; }
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color: #e5e7eb; }

    /* Header styling */
    .main-header {
        background: var(--grad-1);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(167, 139, 250, 0.25);
        position: relative;
        overflow: hidden;
    }
    .main-header::after {
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: 22px;
        background: conic-gradient(from 90deg at 50% 50%, rgba(34,211,238,0.2), rgba(167,139,250,0.15), rgba(52,211,153,0.2));
        filter: blur(30px);
        z-index: 0;
    }
    .main-header h1 { position: relative; z-index: 1; font-size: 3rem; font-weight: 800; margin: 0; }
    .main-header p { position: relative; z-index: 1; font-size: 1.1rem; opacity: 0.95; }

    /* Paper card */
    .paper-card {
        background: linear-gradient(180deg, rgba(16,24,40,0.85), rgba(16,24,40,0.65));
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(2, 6, 23, 0.6);
        border: 1px solid rgba(167,139,250,0.25);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .paper-card:hover { transform: translateY(-2px); border-color: rgba(34,211,238,0.45); box-shadow: 0 12px 30px rgba(167,139,250,0.25); }
    .paper-title { color: #e2e8f0; font-size: 1.35rem; font-weight: 800; margin-bottom: 0.35rem; }
    .paper-authors { color: var(--neon-2); font-size: 0.95rem; margin-bottom: 0.5rem; font-weight: 600; }
    .paper-summary { color: #cbd5e1; font-size: 0.98rem; line-height: 1.7; margin: 1rem 0; }
    .paper-meta { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.6rem; }
    .category-badge { background: linear-gradient(135deg, var(--neon-1), var(--neon-2)); color: #0b1220; padding: 0.32rem 0.9rem; border-radius: 999px; font-size: 0.82rem; font-weight: 800; }

    /* Animated buttons */
    .pdf-button {
        background: linear-gradient(135deg, var(--neon-3), var(--neon-1));
        color: #0b1220; padding: 0.6rem 1.1rem; border-radius: 10px; text-decoration: none; font-weight: 800; display: inline-block;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 8px 20px rgba(34,211,238,0.25);
    }
    .pdf-button:hover { transform: translateY(-1px) scale(1.02); box-shadow: 0 12px 28px rgba(52,211,153,0.35); }

    /* Stats */
    .stat-card { background: linear-gradient(135deg, #0ea5e9 0%, #a78bfa 100%); color: white; padding: 1.1rem; border-radius: 14px; text-align: center; box-shadow: 0 6px 20px rgba(14,165,233,0.25); }
    .stat-number { font-size: 2.2rem; font-weight: 900; margin: 0; }
    .stat-label { font-size: 0.95rem; opacity: 0.95; margin-top: 0.35rem; }

    /* Sidebar info */
    .sidebar-info { background: rgba(2,6,23,0.6); padding: 1rem; border-radius: 12px; border: 1px solid rgba(34,211,238,0.3); margin: 1rem 0; color: #cbd5e1; }

    /* Highlight */
    mark { background: linear-gradient(135deg, rgba(34,211,238,0.6), rgba(167,139,250,0.6)); color: #0b1220; padding: 0 4px; border-radius: 4px; }
        /* Animations */
        @keyframes fadeInUp { from { opacity: 0; transform: translate3d(0, 10px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes subtlePulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
        @keyframes shimmer { 0% { background-position: -500px 0; } 100% { background-position: 500px 0; } }
        @keyframes iconBounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
        .welcome-card { animation: fadeInUp 0.6s ease both; background: linear-gradient(135deg, rgba(241,245,249,0.08), rgba(203,213,225,0.12)); border-radius: 16px; box-shadow: 0 10px 30px rgba(2,6,23,0.5); border: 1px solid rgba(167,139,250,0.25); }
        .welcome-title { background: linear-gradient(90deg, #22d3ee, #a78bfa); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .shimmer-line { background: linear-gradient(90deg, rgba(255,255,255,0.0), rgba(255,255,255,0.08), rgba(255,255,255,0.0)); background-size: 500px 100%; animation: shimmer 2.2s infinite; height: 2px; border-radius: 999px; }
        .feature-card { animation: fadeInUp 0.5s ease both; background: linear-gradient(180deg, rgba(16,24,40,0.85), rgba(16,24,40,0.65)); border-radius: 16px; box-shadow: 0 8px 26px rgba(2,6,23,0.6); border: 1px solid rgba(34,211,238,0.22); transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease; }
        .feature-card:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(167,139,250,0.28); border-color: rgba(167,139,250,0.4); }
        .feature-icon { font-size: 3rem; display: inline-block; animation: iconBounce 2.4s ease-in-out infinite; }
        /* Footer */
        .footer-fixed {
            position: fixed; left: 0; right: 0; bottom: 0;
            display: flex; align-items: center; justify-content: center;
            padding: 0.6rem 1rem; z-index: 9999;
            background: linear-gradient(90deg, rgba(34,211,238,0.15), rgba(167,139,250,0.15));
            border-top: 1px solid rgba(167,139,250,0.35);
            backdrop-filter: blur(10px);
            box-shadow: 0 -8px 20px rgba(2,6,23,0.35);
            animation: fadeInUp 0.5s ease both;
        }
        .footer-inner { display: inline-flex; align-items: center; gap: 0.6rem; }
        .footer-avatar { width: 28px; height: 28px; border-radius: 50%; border: 2px solid rgba(34,211,238,0.6); box-shadow: 0 4px 12px rgba(167,139,250,0.35); }
        .footer-badge {
            background: linear-gradient(135deg, var(--neon-1), var(--neon-2));
            color: #0b1220; font-weight: 900; letter-spacing: 0.3px;
            padding: 0.35rem 0.75rem; border-radius: 999px;
            box-shadow: 0 6px 18px rgba(167,139,250,0.35);
        }
        .footer-icon { margin-right: 0.5rem; animation: iconBounce 2.2s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# API Configuration
# Prefer Streamlit secrets, then environment, else local dev
API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://127.0.0.1:8001"))

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def search_papers(topic, max_results=5):
    """Search for papers using the API"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/search",
            params={"topic": topic, "max_results": max_results},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Please make sure the server is running on port 8001.")
        st.info("Run: `python -m uvicorn server:app --reload --host 127.0.0.1 --port 8001`")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def display_paper(paper, index):
    """Display a single paper"""
    # Keyword highlighting based on current search keywords
    kw = st.session_state.get('filters', {}).get('keywords', '')
    def _highlight(text: str) -> str:
        try:
            words = [w for w in kw.split() if len(w) > 2]
            for w in words:
                text = text.replace(w, f"<mark>{w}</mark>")
                text = text.replace(w.capitalize(), f"<mark>{w.capitalize()}</mark>")
            return text
        except Exception:
            return text
    title_html = _highlight(paper['title'])
    summary_snip = paper['summary'][:400]
    summary_html = _highlight(summary_snip) + ('...' if len(paper['summary']) > 400 else '')
    st.markdown(f"""
    <div class="paper-card">
        <div class="paper-title">📄 {title_html}</div>
        <div class="paper-authors">👥 {', '.join(paper['authors'][:5])}{'...' if len(paper['authors']) > 5 else ''}</div>
        <div class="paper-summary">{summary_html}</div>
        <div class="paper-meta">
            {''.join([f'<span class="category-badge">{cat}</span>' for cat in paper['categories'][:4]])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # PDF download button
    if paper.get('pdf'):
        st.markdown(f"""
        <a href="{paper['pdf']}" target="_blank" class="pdf-button">
            📥 Download PDF
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔬 AI Researcher Agent</h1>
        <p>Discover cutting-edge research papers from arXiv</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Offline")
            if st.secrets.get("API_BASE_URL") or os.getenv("API_BASE_URL"):
                st.info("API Base URL is set. If offline, check the backend deployment status.")
            else:
                st.info("Set `API_BASE_URL` in Streamlit Secrets to your deployed backend URL (e.g., https://your-api.onrender.com). For local dev use:\n```bash\npython -m uvicorn server:app --reload --host 127.0.0.1 --port 8001\n```")
        
        st.markdown("---")

        st.markdown("### 🤖 AI Settings")
        provider = st.selectbox(
            "AI Provider",
            options=["Offline (no key)", "OpenAI", "Groq", "Anthropic", "Gemini"],
            index=0,
            help="Choose a provider for summaries and chat. Offline works without API keys."
        )
        eli5 = st.toggle("Explain like I'm 5 (ELI5)", value=False)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1,
                                help="Higher is more creative; lower is more focused.")

        # Optional: allow setting keys at runtime (session-only)
        with st.expander("Set API Keys (optional)"):
            openai_key = st.text_input("OPENAI_API_KEY", type="password")
            groq_key = st.text_input("GROQ_API_KEY", type="password")
            anthropic_key = st.text_input("ANTHROPIC_API_KEY", type="password")
            google_key = st.text_input("GOOGLE_API_KEY / GOOGLE_GENERATIVE_AI_API_KEY", type="password")
            if st.button("Apply Keys"):
                if openai_key:
                    os.environ["OPENAI_API_KEY"] = openai_key
                if groq_key:
                    os.environ["GROQ_API_KEY"] = groq_key
                if anthropic_key:
                    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
                if google_key:
                    os.environ["GOOGLE_API_KEY"] = google_key
                    os.environ["GOOGLE_GENERATIVE_AI_API_KEY"] = google_key
                st.success("Keys applied in session.")
        
        # Search settings
        max_results = st.slider(
            "📊 Maximum Results",
            min_value=1,
            max_value=20,
            value=5,
            help="Number of papers to retrieve"
        )
        
        st.markdown("---")
        
        # Popular topics
        st.markdown("### 🔥 Popular Topics")
        popular_topics = [
            "Machine Learning",
            "Deep Learning",
            "Neural Networks",
            "Quantum Computing",
            "Natural Language Processing",
            "Computer Vision",
            "Reinforcement Learning",
            "Transformers"
        ]
        
        for topic in popular_topics:
            if st.button(f"✨ {topic}", key=f"topic_{topic}", use_container_width=True):
                st.session_state.search_topic = topic
        
        st.markdown("---")
        
        # About
        st.markdown("""
        <div class="sidebar-info">
            <h4>ℹ️ About</h4>
            <p>Search and discover academic papers from arXiv.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        if 'total_searches' not in st.session_state:
            st.session_state.total_searches = 0
        if 'total_papers' not in st.session_state:
            st.session_state.total_papers = 0
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_searches}</div>
            <div class="stat-label">Total Searches</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_papers}</div>
            <div class="stat-label">Papers Found</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔔 Alerts & Recommendations")
        # Simple local JSON store for alerts and reading list
        store_path = pathlib.Path("alerts_store.json")
        if 'alerts' not in st.session_state:
            if store_path.exists():
                try:
                    st.session_state.alerts = json.loads(store_path.read_text(encoding="utf-8"))
                except Exception:
                    st.session_state.alerts = {"topics": [], "authors": [], "reading_list": []}
            else:
                st.session_state.alerts = {"topics": [], "authors": [], "reading_list": []}

        alert_topic = st.text_input("Set Topic Alert", placeholder="e.g., diffusion models")
        if st.button("🔔 Set Alert") and alert_topic:
            if alert_topic not in st.session_state.alerts["topics"]:
                st.session_state.alerts["topics"].append(alert_topic)
                store_path.write_text(json.dumps(st.session_state.alerts, indent=2), encoding="utf-8")
            st.success(f"Alert set for topic: {alert_topic}")

        alert_author = st.text_input("Follow Author", placeholder="e.g., Yann LeCun")
        if st.button("👤 Follow Author") and alert_author:
            if alert_author not in st.session_state.alerts["authors"]:
                st.session_state.alerts["authors"].append(alert_author)
                store_path.write_text(json.dumps(st.session_state.alerts, indent=2), encoding="utf-8")
            st.success(f"Following author: {alert_author}")

        st.caption("Daily Digest & email can be enabled later via SMTP/API.")

        st.markdown("---")
        st.markdown("### 🔍 Advanced Filters")
        date_range = st.selectbox(
            "Date Range",
            options=["All time", "Last 7 days", "Last 30 days", "Last 365 days"],
            index=0,
            help="Filter by publication date"
        )
        author_filter = st.text_input("Author contains", help="Filter results by author name")
        common_cats = [
            "cs.AI", "cs.LG", "cs.CV", "cs.CL", "stat.ML", "quant-ph", "cs.RO", "cs.DS",
            "math.OC", "econ.EM", "physics.comp-ph"
        ]
        category_filter = st.multiselect("Categories", options=common_cats, help="Match any of the selected categories")
        sort_option = st.selectbox(
            "Sort By",
            options=["Relevance (default)", "Newest first", "Oldest first"],
            index=0,
        )
        st.caption("Tip: Use AND/OR/NOT in your search query for Boolean search.")
    
    # Main content
    # Session state initialization
    if 'papers' not in st.session_state:
        st.session_state.papers = []
    if 'summaries' not in st.session_state:
        st.session_state.summaries = {}
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'chat_histories' not in st.session_state:
        st.session_state.chat_histories = {}  # idx -> List[{role, content}]
    if 'selected_indices' not in st.session_state:
        st.session_state.selected_indices = []
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    if 'reading_list' not in st.session_state:
        st.session_state.reading_list = st.session_state.alerts.get("reading_list", [])

    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search input
        search_topic = st.text_input(
            "🔍 Search for research papers",
            value=st.session_state.get('search_topic', ''),
            placeholder="e.g., machine learning, quantum computing, neural networks...",
            key="search_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🚀 Search", type="primary", use_container_width=True)
    
    # Search functionality
    # Handle search action and persist results in session
    if search_button and search_topic:
        if not api_status:
            st.error("⚠️ API is not running. Please start the server first.")
        else:
            with st.spinner("🔎 Searching arXiv for papers..."):
                results = search_papers(search_topic, max_results)
                if results and 'entries' in results:
                    st.session_state.papers = results['entries']
                    st.session_state.search_topic = search_topic
                    st.session_state.total_searches += 1
                    st.session_state.total_papers += len(st.session_state.papers)
                    st.session_state.filters = {
                        "date_range": date_range,
                        "author": author_filter.strip(),
                        "categories": category_filter,
                        "sort": sort_option,
                        "keywords": search_topic,
                    }
                else:
                    st.session_state.papers = []
                    st.warning("No papers found. Try a different search term.")
    elif search_button and not search_topic:
        st.warning("⚠️ Please enter a search topic")
    
    # Welcome message if no search yet
    # Render results from session state (so buttons don't clear the page)
    if st.session_state.papers:
        papers = st.session_state.papers
        topic = st.session_state.get('search_topic', search_topic)
        # Apply client-side filters
        import datetime as _dt
        def _parse_date(s):
            try:
                return _dt.datetime.fromisoformat(s.replace("Z", "+00:00")).date()
            except Exception:
                return None
        today = _dt.date.today()
        def _date_ok(p):
            if st.session_state.filters.get("date_range") == "All time":
                return True
            pub = _parse_date(p.get("published") or p.get("updated") or "")
            if not pub:
                return True
            rng = st.session_state.filters.get("date_range")
            days = 0
            if rng == "Last 7 days":
                days = 7
            elif rng == "Last 30 days":
                days = 30
            elif rng == "Last 365 days":
                days = 365
            return (today - pub).days <= days if days else True
        def _author_ok(p):
            a = st.session_state.filters.get("author", "").lower()
            if not a:
                return True
            return any(a in x.lower() for x in p.get("authors", []))
        def _category_ok(p):
            cats = st.session_state.filters.get("categories", [])
            if not cats:
                return True
            pcats = set(p.get("categories", []))
            return any(c in pcats for c in cats)
        filtered = [p for p in papers if _date_ok(p) and _author_ok(p) and _category_ok(p)]
        if st.session_state.filters.get("sort") == "Newest first":
            filtered.sort(key=lambda p: p.get("published", ""), reverse=True)
        elif st.session_state.filters.get("sort") == "Oldest first":
            filtered.sort(key=lambda p: p.get("published", ""))
        st.markdown(f"### 📚 Found {len(papers)} papers on '{topic}'")
        st.markdown("<br>", unsafe_allow_html=True)

        # Comparison selection persisted
        st.session_state.selected_indices = st.multiselect(
            "Select papers to compare (optional)",
            options=list(range(1, len(papers) + 1)),
            default=st.session_state.selected_indices,
            help="Pick 2-3 papers to compare summaries and insights.",
            key="compare_select"
        )

        # Display each paper with AI actions (filtered list)
        for idx, paper in enumerate(filtered, 1):
            display_paper(paper, idx)

            c1, c2, c3 = st.columns([1, 1, 3])
            with c1:
                if st.button(f"🤖 AI Summary #{idx}", key=f"summarize_{idx}"):
                    with st.spinner("Generating AI summary..."):
                        prov = provider.split(" ")[0].lower()
                        if prov == "offline":
                            prov = "offline"
                        payload = {
                            "text": f"Title: {paper['title']}\nAuthors: {', '.join(paper['authors'])}\nAbstract: {paper['summary']}",
                            "mode": "eli5" if eli5 else "default",
                            "provider": prov,
                        }
                        try:
                            resp = requests.post(f"{API_BASE_URL}/summarize", json=payload, timeout=60)
                            if resp.status_code == 200:
                                st.session_state.summaries[idx] = resp.json()
                            else:
                                st.error(f"Summarization error: {resp.status_code} - {resp.text}")
                        except Exception as e:
                            st.error(f"Summarization failed: {e}")

            with c2:
                chat_key = f"chat_toggle_{idx}"
                if st.button(f"💬 Chat #{idx}", key=chat_key):
                    st.session_state.setdefault(chat_key, True)

            # Save to reading list
            c_read, _ = st.columns([1, 3])
            with c_read:
                if st.button(f"📚 Save to Reading List #{idx}", key=f"save_{idx}"):
                    entry = {
                        "title": paper['title'],
                        "authors": paper['authors'],
                        "pdf": paper.get('pdf'),
                        "categories": paper.get('categories', []),
                        "summary": paper.get('summary', ''),
                    }
                    st.session_state.reading_list.append(entry)
                    try:
                        store_path = pathlib.Path("alerts_store.json")
                        st.session_state.alerts["reading_list"] = st.session_state.reading_list
                        store_path.write_text(json.dumps(st.session_state.alerts, indent=2), encoding="utf-8")
                    except Exception:
                        pass
                    st.success("Saved to your Reading List.")

            # Show stored summary if available
            if idx in st.session_state.summaries:
                data = st.session_state.summaries[idx]
                st.subheader("AI Summary")
                st.write(data.get("summary", ""))
                insights = data.get("key_insights", [])
                if insights:
                    st.markdown("**Key Insights:**")
                    for b in insights:
                        st.markdown(f"- {b}")

            if st.session_state.get(f"chat_toggle_{idx}"):
                with st.expander(f"Chat with Paper #{idx}", expanded=True):
                    # Ensure chat history exists for this paper
                    history = st.session_state.chat_histories.setdefault(idx, [])

                    # Render chat transcript
                    for msg in history:
                        role = msg.get("role", "assistant")
                        content = msg.get("content", "")
                        with st.chat_message("user" if role == "user" else "assistant"):
                            st.markdown(content)

                    # Quick prompt suggestions
                    st.markdown("_Quick prompts:_")
                    cqa1, cqa2, cqa3, cqa4 = st.columns(4)
                    quick_map = {
                        "Contributions": "What are the core contributions?",
                        "Limitations": "What are the limitations or failure cases?",
                        "Compare": "How does this compare to prior work?",
                        "ELI5": "Explain this paper like I'm five.",
                    }
                    for label, default_q in zip(["Contributions", "Limitations", "Compare", "ELI5"], quick_map.values()):
                        pass
                    if cqa1.button("Contributions", key=f"quick_contrib_{idx}"):
                        st.session_state[f"q_{idx}"] = quick_map["Contributions"]
                    if cqa2.button("Limitations", key=f"quick_limits_{idx}"):
                        st.session_state[f"q_{idx}"] = quick_map["Limitations"]
                    if cqa3.button("Compare", key=f"quick_compare_{idx}"):
                        st.session_state[f"q_{idx}"] = quick_map["Compare"]
                    if cqa4.button("ELI5", key=f"quick_eli5_{idx}"):
                        st.session_state[f"q_{idx}"] = quick_map["ELI5"]

                    # Input + actions
                    with st.form(key=f"chat_form_{idx}", clear_on_submit=True):
                        user_q = st.text_input("Your message", value=st.session_state.get(f"q_{idx}", ""))
                        col_send, col_clear, col_export = st.columns([1, 1, 1])
                        send = col_send.form_submit_button("Send")
                        clear = col_clear.form_submit_button("Clear Chat")
                        export = col_export.form_submit_button("Export")

                    if clear:
                        st.session_state.chat_histories[idx] = []
                        st.session_state.answers.pop(idx, None)
                        st.experimental_rerun()

                    if export:
                        # Build markdown transcript for download
                        md_lines = [f"# Chat Transcript - Paper #{idx}", ""]
                        for m in history:
                            prefix = "User" if m.get("role") == "user" else "Assistant"
                            md_lines.append(f"**{prefix}:** {m.get('content','')}")
                        md = "\n\n".join(md_lines)
                        st.download_button(
                            label="Download Transcript",
                            data=md,
                            file_name=f"chat_paper_{idx}.md",
                            mime="text/markdown",
                            key=f"dl_chat_{idx}"
                        )

                    if send and user_q:
                        with st.spinner("Thinking..."):
                            prov = provider.split(" ")[0].lower()
                            if prov == "offline":
                                prov = "offline"
                            context = (
                                f"Title: {paper['title']}\n"
                                f"Authors: {', '.join(paper['authors'])}\n"
                                f"Abstract: {paper['summary']}\n"
                                f"Categories: {', '.join(paper['categories'])}"
                            )
                            # Add user to history before sending
                            history.append({"role": "user", "content": user_q})
                            payload = {
                                "context": context,
                                "question": user_q,
                                "mode": "eli5" if eli5 else "default",
                                "provider": prov,
                                "history": history,
                            }
                            try:
                                resp = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=60)
                                if resp.status_code == 200:
                                    answer = resp.json().get("answer", "")
                                    # Streaming render: progressively update assistant bubble
                                    with st.chat_message("assistant"):
                                        placeholder = st.empty()
                                        stream_text = ""
                                        import time as _t
                                        # Simple word-by-word stream for UX
                                        for word in answer.split():
                                            stream_text += (word + " ")
                                            placeholder.markdown(stream_text)
                                            _t.sleep(0.02)
                                    # Store full answer in history
                                    history.append({"role": "assistant", "content": answer})
                                    st.session_state.answers[idx] = answer
                                else:
                                    st.error(f"Chat error: {resp.status_code} - {resp.text}")
                            except Exception as e:
                                st.error(f"Chat failed: {e}")

        # Export option
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            json_data = json.dumps(papers, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"papers_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        with col2:
            text_data = "\n\n".join([
                f"Title: {p['title']}\nAuthors: {', '.join(p['authors'])}\nSummary: {p['summary']}\nPDF: {p['pdf']}\n"
                for p in filtered
            ])
            st.download_button(
                label="📥 Download TXT",
                data=text_data,
                file_name=f"papers_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        # Personalized recommendations section
        st.markdown("---")
        st.markdown("### 🌟 For You")
        # Recommend papers similar to alerts and reading list via keyword overlap
        def _score(p, keywords):
            text = (p['title'] + ' ' + p.get('summary','')).lower()
            return sum(1 for k in keywords if k.lower() in text)
        alert_keywords = st.session_state.alerts.get("topics", []) + st.session_state.alerts.get("authors", [])
        if alert_keywords:
            scored = sorted(papers, key=lambda p: _score(p, alert_keywords), reverse=True)
            recs = [p for p in scored if _score(p, alert_keywords) > 0][:5]
            if recs:
                for rp in recs:
                    st.markdown(f"- **{rp['title']}** — {', '.join(rp['authors'][:3])}")
            else:
                st.caption("No personalized recommendations yet. Add topic/author alerts.")
        else:
            st.caption("Set alerts or save papers to get personalized recommendations.")
    
    # If no results yet, show welcome
    if not st.session_state.papers:
        st.markdown("""
        <div class="welcome-card" style="text-align: center; padding: 2.5rem; margin-top: 1.5rem;">
            <h2 class="welcome-title" style="font-size: 2.1rem; font-weight: 900; margin: 0 0 0.6rem 0;">👋 Welcome to AI Researcher Agent!</h2>
            <div class="shimmer-line"></div>
            <p style="color: #cbd5e1; font-size: 1.05rem; margin-top: 0.9rem;">Search for academic papers from arXiv and discover cutting-edge research.</p>
            <p style="color: #94a3b8; margin-top: 0.5rem;">💡 Try searching for topics like "machine learning", "quantum computing", or "neural networks"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 2rem;">
                <div class="feature-icon">🔍</div>
                <h3 style="color: #e2e8f0; margin-top: 1rem;">Smart Search</h3>
                <p style="color: #94a3b8;">Search millions of papers from arXiv</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 2rem;">
                <div class="feature-icon">📊</div>
                <h3 style="color: #e2e8f0; margin-top: 1rem;">Track Stats</h3>
                <p style="color: #94a3b8;">Monitor your research activity</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 2rem;">
                <div class="feature-icon">📥</div>
                <h3 style="color: #e2e8f0; margin-top: 1rem;">Export Results</h3>
                <p style="color: #94a3b8;">Download papers as JSON or TXT</p>
            </div>
            """, unsafe_allow_html=True)

    # Alerts quick check: surface new papers for alert topics (manual trigger)
    if st.session_state.alerts.get("topics"):
        st.markdown("## 🔔 Alert Check")
        if st.button("Check Alerts Now"):
            with st.spinner("Checking alert topics..."):
                found = []
                for t in st.session_state.alerts["topics"]:
                    res = search_papers(t, max_results=5)
                    if res and 'entries' in res:
                        found.extend(res['entries'])
                if found:
                    st.success(f"Found {len(found)} recent papers for your alerts.")
                    for p in found[:10]:
                        st.markdown(f"- **{p['title']}** — {', '.join(p['authors'][:3])}")
                else:
                    st.info("No new alert matches right now.")

    # If user selected papers to compare, show side-by-side comparison
    if st.session_state.papers and st.session_state.selected_indices:
        st.markdown("## 🆚 Compare Selected Papers")
        cols = st.columns(len(st.session_state.selected_indices))
        for i, idx in enumerate(st.session_state.selected_indices):
            p = st.session_state.papers[idx - 1]
            with cols[i]:
                st.markdown(f"**{p['title']}**")
                payload = {
                    "text": f"Title: {p['title']}\nAuthors: {', '.join(p['authors'])}\nAbstract: {p['summary']}",
                    "mode": "eli5" if eli5 else "default",
                    "provider": (provider.split(" ")[0].lower() if provider else "offline") or "offline",
                }
                try:
                    resp = requests.post(f"{API_BASE_URL}/summarize", json=payload, timeout=60)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.write(data.get("summary", ""))
                        insights = data.get("key_insights", [])
                        if insights:
                            st.markdown("**Key Insights:**")
                            for b in insights[:5]:
                                st.markdown(f"- {b}")
                    else:
                        st.error("Compare summarize error")
                except Exception as e:
                    st.error(f"Compare failed: {e}")

    # Footer: Developer credit (fixed at bottom) with avatar
    # Load developer image and embed as base64 data URI for reliable rendering
    dev_img_path = os.path.join(os.getcwd(), "developer.jpg")
    data_uri = None
    try:
        with open(dev_img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{b64}"
    except Exception:
        data_uri = None

    footer_html = (
        f"""
        <div class=\"footer-fixed\"> 
            <div class=\"footer-inner\"> 
                <span class=\"footer-icon\">⚙️</span>
                {f'<img class=\"footer-avatar\" src=\"{data_uri}\" alt=\"Abhishek Kumar\" />' if data_uri else ''}
                <span class=\"footer-badge\">Developer: Abhishek Kumar</span>
            </div>
        </div>
        """
    )
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
