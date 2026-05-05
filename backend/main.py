from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Request(BaseModel):
    prompt: str

@app.post("/generate")
def generate_system(req: Request):
    user_input = req.prompt

    architecture_prompt = f"""
    Design a scalable system for: {user_input}

    Return ONLY valid JSON:

    {{
     "services": ["..."],
     "databases": ["..."],
     "diagram": "Return a Mermaid.js diagram of the system",
     "cache": ["..."],
     "load_balancing": ["..."],
     "scaling_strategy": "...",
    "notes": "..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": architecture_prompt}]
    )

    import json

    raw = response.choices[0].message.content

    try:
        parsed = json.loads(raw)
    except:
        parsed = {"raw": raw}

    return parsed

@app.post("/review")
def review_system(req: Request):
    system_design = req.prompt

    SYSTEM_PROMPT = """
    You are a FAANG senior interviewer.

    Return ONLY valid JSON in this format:

    return {
    "summary": summary,
    "components": components,
    "database_design": db_design,
    "apis": apis,
    "scalability_notes": scalability_notes,
    "bottlenecks": bottlenecks,
    "final_score": {
        "overall": 7.5,
        "breakdown": {
            "scalability": 8,
            "clarity": 7,
            "completeness": 7
        },
        "feedback": [
            "Good separation of services",
            "Missing caching layer (Redis)"
        ]
    }
}
"""

    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": review_prompt}]
    )

    issues=detect_bottlenecks(system_design)

    return {
        "review": response.choices[0].message.content,
        "detected_issues": issues
        }


def detect_bottlenecks(text):
    issues = []

    if "cache" not in text.lower():
        issues.append("No caching layer → high latency risk")

    if "load balancer" not in text.lower():
        issues.append("No load balancer → single point of failure")

    if "database" in text.lower() and "replica" not in text.lower():
        issues.append("No DB replication → scaling bottleneck")

    return issues