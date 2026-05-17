import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv(override=True)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)
    max_length: int = Field(gt=0)


class SummarizeResponse(BaseModel):
    summary: str


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1)


class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    explanation: str


def _require_client() -> OpenAI:
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not set. Add it to your .env file.",
        )
    return client


def _json_from_model(prompt: str) -> dict:
    c = _require_client()
    result = c.responses.create(model=OPENAI_MODEL, input=prompt)
    try:
        return json.loads(result.output_text)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="Model did not return valid JSON.") from exc


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest):
    c = _require_client()
    prompt = (
    f"You are a professional editor writing for a general audience with no technical background. "
    f"Summarize the following text in exactly 1 sentence, using simple everyday language. "
    f"Do not use jargon or technical terms.\n\n"
    f"Text:\n{payload.text}"
)
    result = c.responses.create(model=OPENAI_MODEL, input=prompt)
    return {"summary": result.output_text.strip()}


@app.post("/analyze-sentiment", response_model=SentimentResponse)
def analyze_sentiment(payload: SentimentRequest):
    data = _json_from_model(
    "You are an expert linguist analyzing text for a business report. "
"Respond only in English. "
"Carefully analyze the emotional tone and context of the text below. "
"Be precise with your confidence score and provide a detailed explanation of your reasoning. "
"Return ONLY JSON with keys: sentiment (positive|neutral|negative), confidence (0 to 1), explanation.\n"
f"Text:\n{payload.text}"
    )
    return data
