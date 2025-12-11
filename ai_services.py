import os
import re
from typing import Dict, Any, List, Optional


def _split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    # Simple split on punctuation; keep it robust without external libs
    sentences = re.split(r"(?<=[.!?])\s+", text)
    # Filter short fragments
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    return sentences


_STOPWORDS = set(
    "a an the and or but if while with without within on in at for of to from by into over under about as is are was were be been being this that these those it its it's their there here such using use used than then when where which who whom whose what why how can may might should would could our we you your they them do does did done not no yes also more most much many few several each per via among between across against above below before after during until unless until because therefore however moreover nonetheless otherwise instead".split()
)


def _tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z\-']+", text.lower())
    return [t for t in tokens if t not in _STOPWORDS]


def _score_sentences(sentences: List[str]) -> List[float]:
    # Frequency-based extractive scoring
    all_tokens: List[str] = []
    for s in sentences:
        all_tokens.extend(_tokenize(s))
    freq: Dict[str, int] = {}
    for t in all_tokens:
        freq[t] = freq.get(t, 0) + 1
    if not freq:
        return [0.0] * len(sentences)
    max_f = max(freq.values())
    scores: List[float] = []
    for s in sentences:
        tokens = _tokenize(s)
        if not tokens:
            scores.append(0.0)
            continue
        score = sum(freq.get(t, 0) for t in tokens) / (len(tokens) * max_f)
        scores.append(score)
    return scores


def _simplify_eli5(text: str) -> str:
    replacements = {
        "utilize": "use",
        "approximately": "about",
        "methodology": "method",
        "optimization": "improving",
        "architecture": "design",
        "parameters": "settings",
        "algorithm": "set of steps",
        "demonstrate": "show",
        "significant": "big",
        "objective": "goal",
        "hypothesis": "idea",
        "complex": "hard",
        "simplify": "make easier",
        "evaluation": "testing",
        "robust": "reliable",
    }
    out = text
    for k, v in replacements.items():
        out = re.sub(rf"\b{k}\b", v, out, flags=re.IGNORECASE)
    # Shorten long sentences
    sentences = _split_sentences(out)
    clipped = []
    for s in sentences:
        if len(s) > 220:
            s = s[:200].rstrip() + "..."
        clipped.append(s)
    return " ".join(clipped)


def offline_summarize(text: str, max_sentences: int = 5, eli5: bool = False) -> Dict[str, Any]:
    sentences = _split_sentences(text)
    if not sentences:
        return {"summary": text.strip(), "key_insights": [], "bullets": []}
    scores = _score_sentences(sentences)
    # Pick top sentences while preserving order
    idx_sorted = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:max_sentences]
    idx_sorted = sorted(idx_sorted)
    chosen = [sentences[i] for i in idx_sorted]
    summary = " ".join(chosen)
    # Extract rough "insights" via keyword hints or top sentences
    insight_hints = ("we ", "our ", "propos", "introduc", "method", "result", "outperform", "improv")
    insights = [s for s in sentences if any(h in s.lower() for h in insight_hints)]
    if not insights:
        insights = chosen
    bullets = [s if len(s) <= 220 else s[:200].rstrip() + "..." for s in insights[:5]]
    if eli5:
        summary = _simplify_eli5(summary)
        bullets = [_simplify_eli5(b) for b in bullets]
    return {"summary": summary, "key_insights": bullets, "bullets": bullets}


def offline_chat(context: str, question: str, eli5: bool = False) -> str:
    # Very naive retrieval: pick sentences with highest keyword overlap
    sents = _split_sentences(context)
    q_tokens = set(_tokenize(question))
    if not sents:
        base = "I don't have enough information to answer."
        return _simplify_eli5(base) if eli5 else base
    scored = []
    for s in sents:
        s_tokens = set(_tokenize(s))
        overlap = len(q_tokens & s_tokens)
        scored.append((overlap, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for _, s in scored[:3] if _ > 0]
    if not top:
        answer = "Based on the abstract, I cannot find a direct answer. The paper discusses: " + " ".join(sents[:2])
    else:
        answer = "Here is what the paper says: " + " ".join(top)
    return _simplify_eli5(answer) if eli5 else answer


def _call_openai(messages: List[Dict[str, str]], model: str = "gpt-4o-mini") -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
        return resp.choices[0].message.content
    except Exception:
        return None


def _call_groq(messages: List[Dict[str, str]], model: str = "llama-3.1-70b-versatile") -> Optional[str]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
        return resp.choices[0].message.content
    except Exception:
        return None


def _call_anthropic(messages: List[Dict[str, str]], model: str = "claude-3-5-haiku-latest") -> Optional[str]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        # Convert OpenAI-like messages to Anthropic prompt
        sys = ""
        user_parts = []
        for m in messages:
            if m["role"] == "system":
                sys = m["content"]
            elif m["role"] == "user":
                user_parts.append(m["content"])
            elif m["role"] == "assistant":
                user_parts.append("Assistant: " + m["content"])  # context only
        content = "\n\n".join(user_parts)
        resp = client.messages.create(
            model=model,
            max_tokens=800,
            temperature=0.2,
            system=sys or "You are a helpful assistant.",
            messages=[{"role": "user", "content": content}],
        )
        # Anthropics returns content parts
        if resp.content and len(resp.content) > 0:
            return getattr(resp.content[0], "text", None) or str(resp.content[0])
        return None
    except Exception:
        return None


def _call_gemini(messages: List[Dict[str, str]], model: str = "gemini-1.5-flash") -> Optional[str]:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        sys = ""
        user_content = []
        for m in messages:
            if m["role"] == "system":
                sys = m["content"]
            elif m["role"] == "user":
                user_content.append(m["content"])
        prompt = (sys + "\n\n" + "\n\n".join(user_content)).strip()
        model_obj = genai.GenerativeModel(model)
        resp = model_obj.generate_content(prompt)
        return getattr(resp, "text", None)
    except Exception:
        return None


def llm_generate(provider: str, messages: List[Dict[str, str]]) -> Optional[str]:
    provider = (provider or "").lower()
    if provider == "openai":
        return _call_openai(messages)
    if provider == "groq":
        return _call_groq(messages)
    if provider == "anthropic":
        return _call_anthropic(messages)
    if provider == "gemini":
        return _call_gemini(messages)
    return None


def ai_summarize(text: str, mode: str = "default", provider: str = "offline") -> Dict[str, Any]:
    eli5 = mode.lower() == "eli5"
    # Try LLM first if provider given; otherwise offline
    sys = "You summarize scientific papers clearly and concisely. Also extract 3-5 key insights as bullets."
    if eli5:
        sys += " Explain like I'm five without losing the main ideas."
    user = f"Summarize the following scientific abstract or excerpt in 6-8 sentences. Then list 3-5 key insights as bullets.\n\nTEXT:\n{text}"
    llm_out = llm_generate(provider, [{"role": "system", "content": sys}, {"role": "user", "content": user}])
    if llm_out:
        # Heuristic split: summary first paragraph, bullets afterwards
        parts = llm_out.strip().split("\n\n")
        summary = parts[0].strip()
        bullets = []
        for line in llm_out.splitlines():
            if line.strip().startswith(('-', '*', '•')):
                bullets.append(line.strip('-*• ').strip())
        if not bullets:
            bullets = [p.strip() for p in parts[1:3] if p.strip()]
        return {"summary": summary, "key_insights": bullets[:5], "bullets": bullets[:5]}
    # Offline fallback
    return offline_summarize(text, max_sentences=5, eli5=eli5)


def ai_chat(context: str, question: str, mode: str = "default", provider: str = "offline", history: Optional[List[Dict[str, str]]] = None) -> str:
    eli5 = mode.lower() == "eli5"
    messages = [{"role": "system", "content": "Answer questions using the given paper context. If unsure, say so."}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"})
    llm_out = llm_generate(provider, messages)
    if llm_out:
        return llm_out
    return offline_chat(context, question, eli5=eli5)
