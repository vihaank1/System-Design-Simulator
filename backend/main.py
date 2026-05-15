from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

def clean_json_response(raw_text):
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    return json.loads(cleaned)

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# FASTAPI SETUP
# =========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================

class Request(BaseModel):
    prompt: str

# =========================
# SYSTEM DESIGN GENERATION
# =========================

@app.post("/generate")
def generate_system(req: Request):

    architecture_prompt = f"""
You are a senior distributed systems engineer.

Design a scalable production-grade architecture for:

{req.prompt}

Return ONLY valid JSON.

Required format:

{{
  "summary": "...",
  "services": [
    "...",
    "..."
  ],
  "databases": [
    "...",
    "..."
  ],
  "cache": [
    "..."
  ],
  "load_balancing": [
    "..."
  ],
  "scaling_strategy": "...",
  "apis": [
    "..."
  ],
  "diagram": "graph TD; User-->API; API-->DB;",
  "notes": [
    "...",
    "..."
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert system design interviewer."
            },
            {
                "role": "user",
                "content": architecture_prompt
            }
        ],
        temperature=0.7
    )

    raw = response.choices[0].message.content

    try:
        parsed = clean_json_response(raw)
        return parsed

    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "raw_response": raw,
            "details": str(e)
        }

# =========================
# REVIEW / SCORING
# =========================

@app.post("/review")
def review_system(req: Request):
    system_design = req.prompt

    review_prompt = f"""
    You are a FAANG senior systems design interviewer.

    Review this system design:

    {system_design}

    Return ONLY valid JSON:

    {{
      "summary": "...",
      "strengths": ["...", "..."],
      "weaknesses": ["...", "..."],
      "bottlenecks": ["...", "..."],
      "hire_recommendation": "Hire / No Hire",
      "final_score": {{
          "overall": 8,
          "breakdown": {{
              "scalability": 8,
              "clarity": 7,
              "completeness": 9
          }},
          "feedback": [
              "...",
              "..."
          ]
      }}
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": review_prompt}
        ]
    )

    import json

    raw_review = response.choices[0].message.content

    try:
        parsed_review = clean_json_response(raw_review)
    except Exception as e:
        parsed_review = {
            "raw": raw_review,
            "error": str(e)
        }

    issues = detect_bottlenecks(system_design)

    parsed_review["detected_issues"] = issues

    return parsed_review

# =========================
# BOTTLENECK DETECTOR
# =========================

def detect_bottlenecks(text):

    text = text.lower()

    issues = []

    if "cache" not in text:
        issues.append(
            "No caching layer detected → high latency risk"
        )

    if (
        "load balancer" not in text
        and "load balancing" not in text
    ):
        issues.append(
            "No load balancer detected → single point of failure"
        )

    if (
        "replica" not in text
        and "replication" not in text
        and "multi-region" not in text
        and "read replica" not in text
    ):
        issues.append(
            "No database replication detected → scaling bottleneck"
        )

    if "cdn" not in text:
        issues.append(
            "No CDN detected → poor global media delivery"
        )

    if (
        "queue" not in text
        and "kafka" not in text
        and "rabbitmq" not in text
    ):
        issues.append(
            "No async queue detected → traffic spike risk"
        )

    return issues

@app.post("/interview")
def interview_mode(req: Request):

    interview_prompt = f"""
    You are a senior FAANG system design interviewer.

    The candidate designed:

    {req.prompt}

    Ask:
    - 3 follow-up system design questions
    - 2 scalability pressure questions
    - 2 tradeoff questions
    - 1 bottleneck debugging question

    Return ONLY valid JSON:

    {{
      "followups": [],
      "scaling_questions": [],
      "tradeoff_questions": [],
      "debugging_question": ""
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": interview_prompt
            }
        ]
    )

    raw = response.choices[0].message.content

    try:
        parsed = clean_json_response(raw)
        return parsed
    except:
        return {"raw": raw}