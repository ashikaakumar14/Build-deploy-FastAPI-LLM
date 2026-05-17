# FastAPI LLM API with Prompt Engineering

A production-style REST API that integrates OpenAI to summarize text and analyze sentiment. Deployed on Render with a live interactive docs page.

**Live API:** https://week1-fastapi-llm.onrender.com/docs

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service status and timestamp |
| POST | `/summarize` | Summarizes text within a given word limit |
| POST | `/analyze-sentiment` | Returns sentiment, confidence score, and explanation |

---

## Built With

`FastAPI` · `OpenAI API` · `Pydantic v2` · `Uvicorn` · `Render`

---

## Prompt Engineering

Each LLM endpoint was tested with 3 prompt variations — experimenting with role prompting, audience constraints, output formatting, and language specification. Key finding: small prompt changes (e.g. adding "Respond only in English") had a significant impact on output consistency and reliability.

---

## Running Locally

```bash
git clone https://github.com/ashikaakumar14/Build-deploy-FastAPI-LLM.git
cd Build-deploy-FastAPI-LLM
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OPENAI_API_KEY
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to explore the API locally.
