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

    review_prompt = f"""
    You are a FAANG reviewer

    Evaluate this system:
    {system_design}

   
    Return ONLY JSON:

    {
      "scoring": {
      "scalability": 0-10,
      "reliability": 0-10,
      "efficiency": 0-10,
      "clarity": 0-10
    },
    "total_score": 0-40,
    "bottlenecks": [],
    "improvements": []
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
