from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Body
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from arxiv_tool import arxiv_search
from ai_services import ai_summarize, ai_chat

app = FastAPI(title="AI Researcher Agent", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(topic: str = Query(..., min_length=1), max_results: int = Query(5, ge=1, le=50)):
    try:
        result = arxiv_search.invoke(topic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    entries = result.get("entries", [])
    if len(entries) > max_results:
        entries = entries[:max_results]
    return JSONResponse(content={"entries": entries})


class SummarizeRequest(BaseModel):
    text: str
    mode: Optional[str] = "default"  # "default" | "eli5"
    provider: Optional[str] = "offline"  # offline | openai | groq | anthropic | gemini


@app.post("/summarize")
def summarize(req: SummarizeRequest):
    if not req.text or len(req.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Missing 'text' to summarize")
    try:
        result = ai_summarize(req.text, mode=req.mode or "default", provider=req.provider or "offline")
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatRequest(BaseModel):
    context: str
    question: str
    mode: Optional[str] = "default"
    provider: Optional[str] = "offline"
    history: Optional[List[Dict[str, str]]] = None  # [{role, content}]


@app.post("/chat")
def chat(req: ChatRequest):
    if not req.context or not req.question:
        raise HTTPException(status_code=400, detail="Missing 'context' or 'question'")
    try:
        answer = ai_chat(
            context=req.context,
            question=req.question,
            mode=req.mode or "default",
            provider=req.provider or "offline",
            history=req.history or [],
        )
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
