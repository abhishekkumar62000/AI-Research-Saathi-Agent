"""
AI Researcher Agent - Enhanced with AI Chat & Summarization
A powerful web interface for searching and analyzing academic papers with AI
"""

import streamlit as st
import requests
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="AI Researcher Agent Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling (enhanced with chat UI)
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Paper card styling */
    .paper-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #6366f1;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .paper-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(99, 102, 241, 0.2);
    }
    
    .paper-title {
        color: #1e293b;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .paper-authors {
        color: #6366f1;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .paper-summary {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    .paper-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    
    .category-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .pdf-button {
        background: #10b981;
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        transition: background 0.2s;
    }
    
    .pdf-button:hover {
        background: #059669;
    }
    
    /* AI Chat styling */
    .chat-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: white;
        border: 1px solid #e2e8f0;
        margin-right: 2rem;
    }
    
    .ai-summary-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .insight-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Stats styling */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Loading animation */
    .loading-text {
        text-align: center;
        font-size: 1.2rem;
        color: #6366f1;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .sidebar-info {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #6366f1;
        margin: 1rem 0;
    }
    
    /* Search box enhancement */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* AI Badge */
    .ai-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8001"

# AI Configuration - Support multiple providers
AI_PROVIDERS = {
    "OpenAI (GPT-4)": "openai",
    "Google Gemini": "gemini",
    "Anthropic Claude": "anthropic",
    "Groq (Fast & Free)": "groq"
}

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

def generate_ai_summary(paper, api_key, provider="groq"):
    """Generate AI summary of a paper using various providers"""
    
    if not api_key:
        return None, "Please provide an API key in the sidebar"
    
    try:
        if provider == "groq":
            # Groq - Fast and Free!
            from groq import Groq
            client = Groq(api_key=api_key)
            
            prompt = f"""Analyze this research paper and provide a comprehensive summary:

Title: {paper['title']}
Authors: {', '.join(paper['authors'][:5])}
Abstract: {paper['summary']}

Please provide:
1. **Main Contribution**: What is the key innovation or finding?
2. **Methodology**: How did they approach the problem?
3. **Key Results**: What are the main findings?
4. **Significance**: Why does this matter?
5. **Limitations**: What are the constraints or future work needed?

Format your response in clear sections with bullet points."""

            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content, None
            
        elif provider == "openai":
            # OpenAI GPT-4
            import openai
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{
                    "role": "user",
                    "content": f"Summarize this research paper:\n\nTitle: {paper['title']}\n\nAbstract: {paper['summary']}\n\nProvide: Main contribution, methodology, key results, and significance."
                }],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content, None
            
        elif provider == "gemini":
            # Google Gemini
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"Summarize this research paper:\n\nTitle: {paper['title']}\n\nAbstract: {paper['summary']}"
            response = model.generate_content(prompt)
            return response.text, None
            
        elif provider == "anthropic":
            # Anthropic Claude
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"Summarize this research paper:\n\nTitle: {paper['title']}\n\nAbstract: {paper['summary']}"
                }]
            )
            return message.content[0].text, None
            
    except Exception as e:
        return None, f"Error: {str(e)}"

def chat_with_paper(paper, question, chat_history, api_key, provider="groq"):
    """Chat with a paper using AI"""
    
    if not api_key:
        return "Please provide an API key in the sidebar", None
    
    try:
        if provider == "groq":
            from groq import Groq
            client = Groq(api_key=api_key)
            
            # Build context from paper
            context = f"""You are an AI research assistant. You're helping a researcher understand this paper:

Title: {paper['title']}
Authors: {', '.join(paper['authors'])}
Abstract: {paper['summary']}
Categories: {', '.join(paper['categories'])}

Answer the researcher's questions about this paper in a clear, helpful way."""

            # Build messages with history
            messages = [{"role": "system", "content": context}]
            
            # Add chat history
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add current question
            messages.append({"role": "user", "content": question})
            
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content, None
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔬 AI Researcher Agent <span class="ai-badge">AI-POWERED</span></h1>
        <p>Discover and analyze cutting-edge research papers with AI assistance</p>
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
            st.info("Start the server:\n```bash\npython -m uvicorn server:app --reload --host 127.0.0.1 --port 8001\n```")
        
        st.markdown("---")
        
        # AI Configuration
        st.markdown("### 🤖 AI Configuration")
        
        # Provider selection
        provider_name = st.selectbox(
            "AI Provider",
            list(AI_PROVIDERS.keys()),
            help="Choose your AI provider"
        )
        provider = AI_PROVIDERS[provider_name]
        st.session_state['ai_provider'] = provider
        
        # API Key input
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Enter your API key for AI features",
            placeholder="sk-..."
        )
        st.session_state['ai_api_key'] = api_key
        
        if provider == "groq":
            st.info("🚀 **Groq is FREE!** Get your API key at [console.groq.com](https://console.groq.com)")
        elif provider == "openai":
            st.info("Get your API key at [platform.openai.com](https://platform.openai.com)")
        elif provider == "gemini":
            st.info("Get your API key at [makersuite.google.com](https://makersuite.google.com)")
        elif provider == "anthropic":
            st.info("Get your API key at [console.anthropic.com](https://console.anthropic.com)")
        
        st.markdown("---")
        
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
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.session_state.search_topic = topic
        
        st.markdown("---")
        
        # About
        st.markdown("""
        <div class="sidebar-info">
            <h4>ℹ️ About</h4>
            <p>AI-powered research assistant with paper summarization and interactive chat features.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        if 'total_searches' not in st.session_state:
            st.session_state.total_searches = 0
        if 'total_papers' not in st.session_state:
            st.session_state.total_papers = 0
        if 'ai_summaries' not in st.session_state:
            st.session_state.ai_summaries = 0
        
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
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.ai_summaries}</div>
            <div class="stat-label">AI Summaries</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
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
    if search_button and search_topic:
        if not api_status:
            st.error("⚠️ API is not running. Please start the server first.")
        else:
            with st.spinner("🔎 Searching arXiv for papers..."):
                results = search_papers(search_topic, max_results)
                
                if results and 'entries' in results:
                    papers = results['entries']
                    
                    # Update stats
                    st.session_state.total_searches += 1
                    st.session_state.total_papers += len(papers)
                    
                    # Display results
                    st.markdown(f"### 📚 Found {len(papers)} papers on '{search_topic}'")
                    
                    # AI Features Notice
                    if st.session_state.get('ai_api_key'):
                        st.success("✨ AI features enabled! Click 'AI Summary' or 'Chat with Paper' on any result.")
                    else:
                        st.info("💡 **Tip:** Add your API key in the sidebar to unlock AI summaries and chat features!")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display each paper with AI features
                    for idx, paper in enumerate(papers, 1):
                        display_paper_with_ai(paper, idx)
                    
                    # Export option
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        # Download as JSON
                        json_data = json.dumps(papers, indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"papers_{search_topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col2:
                        # Download as text
                        text_data = "\n\n".join([
                            f"Title: {p['title']}\nAuthors: {', '.join(p['authors'])}\nSummary: {p['summary']}\nPDF: {p['pdf']}\n"
                            for p in papers
                        ])
                        st.download_button(
                            label="📥 Download TXT",
                            data=text_data,
                            file_name=f"papers_{search_topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                else:
                    st.warning("No papers found. Try a different search term.")
    
    elif search_button and not search_topic:
        st.warning("⚠️ Please enter a search topic")
    
    # Welcome message if no search yet
    if not search_button or not search_topic:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin-top: 2rem;">
            <h2 style="color: #1e293b; margin-bottom: 1rem;">👋 Welcome to AI Researcher Agent Pro!</h2>
            <p style="color: #475569; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                Search for cutting-edge research papers and analyze them with AI. Get instant summaries, chat with papers, and extract key insights!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: #1e293b;">Fast Search</h3>
                <p style="color: #64748b;">Get instant results from millions of papers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="color: #1e293b;">AI Summaries</h3>
                <p style="color: #64748b;">Instant paper summaries with AI</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <h3 style="color: #1e293b;">Chat with Papers</h3>
                <p style="color: #64748b;">Ask questions and get answers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📥</div>
                <h3 style="color: #1e293b;">Easy Export</h3>
                <p style="color: #64748b;">Download results and summaries</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()