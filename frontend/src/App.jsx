import React, { useEffect, useState } from "react";
import axios from "axios";
import mermaid from "mermaid";

const API = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "strict" });

function Diagram({ source }) {
  const [svg, setSvg] = useState("");
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    setSvg("");
    setError(false);
    if (!source) return;
    const id = "system-diagram-" + Math.random().toString(36).slice(2);
    mermaid.render(id, source)
      .then(result => { if (active) setSvg(result.svg); })
      .catch(() => { if (active) setError(true); });
    return () => { active = false; };
  }, [source]);

  if (!source) return null;
  return <section className="panel">
    <h2>System diagram</h2>
    {error ? <><p className="muted">Diagram could not be rendered. Mermaid source:</p><pre>{source}</pre></>
      : svg ? <div className="diagram" dangerouslySetInnerHTML={{ __html: svg }} />
      : <p className="muted">Rendering diagram…</p>}
  </section>;
}

function List({ title, items }) {
  if (!Array.isArray(items) || !items.length) return null;
  return <div><h3>{title}</h3><ul>{items.map((item, i) => <li key={i}>{String(item)}</li>)}</ul></div>;
}

export default function App() {
  const [prompt, setPrompt] = useState("Design Netflix");
  const [design, setDesign] = useState(null);
  const [review, setReview] = useState(null);
  const [interview, setInterview] = useState(null);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");

  async function call(endpoint, text) {
    const response = await axios.post(API + "/" + endpoint, { prompt: text });
    if (response.data?.error) throw new Error(response.data.details || response.data.error);
    return response.data;
  }

  async function run(endpoint, text, setter) {
    setBusy(endpoint);
    setError("");
    try { setter(await call(endpoint, text)); }
    catch (e) { setError(String(e.response?.data?.detail || e.message || "The request failed.")); }
    finally { setBusy(""); }
  }

  function generate(event) {
    event.preventDefault();
    if (!prompt.trim() || busy) return;
    setDesign(null);
    setReview(null);
    setInterview(null);
    run("generate", prompt.trim(), setDesign);
  }

  const designText = design ? JSON.stringify(design, null, 2) : "";
  const scores = review?.final_score;
  return <main className="container">
    <header>
      <span className="eyebrow">AI-POWERED INTERVIEW PRACTICE</span>
      <h1>System Design Interview Simulator</h1>
      <p className="muted">Explore distributed architectures, identify bottlenecks, and practice technical follow-up questions.</p>
    </header>

    <section className="panel">
      <h2>System design prompt</h2>
      <p className="muted">Try “Design Instagram backend”, “Design Uber”, or “Design a URL shortener”.</p>
      <form onSubmit={generate}>
        <label htmlFor="prompt">Your design challenge</label>
        <textarea id="prompt" rows="3" value={prompt} onChange={e => setPrompt(e.target.value)} />
        <button disabled={Boolean(busy) || !prompt.trim()} type="submit">{busy === "generate" ? "Generating…" : "Generate architecture"}</button>
      </form>
    </section>

    {error && <div className="error" role="alert">{error}</div>}

    {design && <>
      <section className="panel">
        <h2>Architecture summary</h2>
        <p>{design.summary}</p>
        <div className="columns">
          <List title="Services" items={design.services} />
          <List title="Databases" items={design.databases} />
          <List title="Caching" items={design.cache} />
          <List title="Load balancing" items={design.load_balancing} />
          <List title="APIs" items={design.apis} />
        </div>
        {design.scaling_strategy && <><h3>Scaling strategy</h3><p>{design.scaling_strategy}</p></>}
      </section>
      <Diagram source={design.diagram} />
      <section className="panel">
        <h2>Engineering notes</h2>
        <List title="Design considerations" items={design.notes} />
        <div className="actions">
          <button type="button" disabled={Boolean(busy)} onClick={() => run("review", designText, setReview)}>
            {busy === "review" ? "Evaluating…" : "Evaluate design"}
          </button>
          <button type="button" className="secondary" disabled={Boolean(busy)} onClick={() => run("interview", designText, setInterview)}>
            {busy === "interview" ? "Preparing…" : "Practice follow-ups"}
          </button>
        </div>
      </section>
    </>}

    {review && <section className="panel">
      <h2>Interview-style review</h2>
      {scores && <div className="score-card">
        <span className="score">{scores.overall ?? "—"}/10</span>
        <div>{Object.entries(scores.breakdown || {}).map(([name, value]) =>
          <div key={name}><strong>{name.replace(/_/g, " ")}</strong>: {String(value)}/10</div>)}</div>
      </div>}
      {review.summary && <p>{review.summary}</p>}
      <div className="columns">
        <List title="Strengths" items={review.strengths} />
        <List title="Weaknesses" items={review.weaknesses} />
        <List title="Bottlenecks" items={review.bottlenecks} />
        <List title="Auto-detected issues" items={review.detected_issues} />
        <List title="Feedback" items={scores?.feedback} />
      </div>
      <p className="muted">AI-generated feedback is practice guidance, not an official hiring assessment. Keyword checks can be inaccurate.</p>
    </section>}

    {interview && <section className="panel">
      <h2>Interviewer follow-ups</h2>
      <div className="columns">
        <List title="Design follow-ups" items={interview.followups} />
        <List title="Scaling questions" items={interview.scaling_questions} />
        <List title="Trade-off questions" items={interview.tradeoff_questions} />
      </div>
      {interview.debugging_question && <><h3>Debugging challenge</h3><p>{interview.debugging_question}</p></>}
    </section>}
    <footer>React · FastAPI · OpenAI API · Mermaid.js</footer>
  </main>;
}
