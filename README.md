# 🧠 FAANG System Design Simulator

An AI-powered distributed systems interview simulator that generates scalable architectures, evaluates them like a real FAANG interviewer, detects bottlenecks, visualizes system flows, and asks follow-up interview questions dynamically.

Built for practicing real-world system design interviews at scale.

---

## 🚀 Features

### 🏗 AI Architecture Generation
Generate production-style system designs for prompts like:

- Design Instagram
- Design Uber
- Design YouTube
- Design a URL Shortener
- Design WhatsApp

The simulator generates:

- Microservices
- Databases
- APIs
- Caching layers
- Scaling strategies
- Load balancing
- Distributed architecture diagrams

---

### 📊 FAANG-Style Interview Scoring

Every generated design is reviewed using a structured engineering rubric.

Scores include:

- Scalability
- Clarity
- Completeness
- System tradeoffs

Includes:

- strengths
- weaknesses
- bottlenecks
- hiring recommendation
- engineering feedback

---

### ⚠ Automatic Bottleneck Detection

The simulator automatically detects architectural weaknesses such as:

- Missing cache layer
- No CDN
- Database scaling issues
- Single points of failure
- Missing replication
- Poor load balancing

---

### 📈 System Diagram Visualization

Architectures are visualized using Mermaid.js diagrams.

Example:

```mermaid
graph TD;
User-->API_Gateway;
API_Gateway-->Services;
Services-->Database;

🎤 FAANG Interviewer Mode

Simulates real senior engineer follow-up questioning.

Generates:

Follow-up architecture questions
Scalability pressure scenarios
Tradeoff discussions
Debugging situations

Designed to mimic Google / Meta / Amazon interview pressure.

🖥 Tech Stack
Frontend
React
Axios
Mermaid.js
Backend
FastAPI
OpenAI API
Python
AI / Infrastructure Concepts
Distributed Systems
Scalability Engineering
System Design Interview Evaluation
Microservices Architecture
📸 Example Workflow
Input
Design Instagram backend
Output
Microservices architecture
Feed generation system
CDN layer
Redis caching
Load balancing
Database sharding
Mermaid architecture diagram
FAANG interview evaluation
Bottleneck analysis
Follow-up interview questions
⚡ Running Locally
1. Clone Repository
git clone <your-repo-url>
cd system-design-simulator
2. Backend Setup
cd backend

pip install -r requirements.txt

uvicorn main:app --reload

Backend runs on:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
3. Frontend Setup
cd frontend

npm install

npm start

Frontend runs on:

http://localhost:3000
🔑 Environment Variables

Create a .env file inside /backend

OPENAI_API_KEY=your_api_key_here
🧠 Why This Project Stands Out

Most interview prep tools only generate answers.

This project:

evaluates architecture quality
simulates interviewer pressure
detects engineering flaws
visualizes distributed systems
mimics real FAANG interview flow

It combines:

AI
distributed systems
full-stack engineering
interview simulation
scalable architecture reasoning

into one platform.

🔥 Future Improvements
Timed interview rounds
Voice interviewer mode
Multi-user mock interviews
Architecture editing canvas
Real-time collaborative interviews
Persistent scoring history
Company-specific interviewer personas
Kubernetes deployment simulation
👨‍💻 Author

Built by Vihaan Kesharwani.

Focused on scalable systems, AI engineering, and distributed architecture.
