import { useState } from "react";

interface ChatResponse {
  response: string;
  tier: string;
  model: string;
  complexity: string;
  estimated_cost_usd: number;
  input_tokens: number;
  output_tokens: number;
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL || ""}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setResult(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const complexityColor: Record<string, string> = {
    easy: "#22c55e",
    medium: "#f59e0b",
    hard: "#ef4444",
  };

  return (
    <div style={s.page}>
      {/* Header */}
      <div style={s.header}>
        <div style={s.logo}>⚡</div>
        <div>
          <h1 style={s.title}>LLM Cost Autopilot</h1>
          <p style={s.subtitle}>Smart routing · Cheap when possible · Strong when needed</p>
        </div>
      </div>

      {/* Stats Bar */}
      <div style={s.statsBar}>
        <div style={s.statItem}>
          <span style={s.statIcon}>💚</span>
          <span style={s.statText}>Cheap → Gemini Flash</span>
        </div>
        <div style={s.divider} />
        <div style={s.statItem}>
          <span style={s.statIcon}>🔥</span>
          <span style={s.statText}>Strong → Gemini Pro</span>
        </div>
        <div style={s.divider} />
        <div style={s.statItem}>
          <span style={s.statIcon}>🧠</span>
          <span style={s.statText}>85% Classifier Accuracy</span>
        </div>
      </div>

      {/* Input */}
      <div style={s.inputCard}>
        <div style={s.inputLabel}>Your Prompt</div>
        <textarea
          style={s.textarea}
          placeholder="Ask anything — the system will automatically route it to the right model..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={4}
          onKeyDown={(e) => e.key === "Enter" && e.metaKey && handleSubmit()}
        />
        <div style={s.inputFooter}>
          <span style={s.hint}>⌘ + Enter to send</span>
          <button style={loading ? s.buttonLoading : s.button} onClick={handleSubmit} disabled={loading}>
            {loading ? (
              <span>⏳ Routing...</span>
            ) : (
              <span>Send Prompt →</span>
            )}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div style={s.errorCard}>
          <span style={s.errorIcon}>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Result */}
      {result && (
        <div style={s.resultCard}>
          {/* Routing Decision */}
          <div style={s.routingBar}>
            <div style={s.routingItem}>
              <span style={s.routingLabel}>Complexity</span>
              <span style={{ ...s.pill, background: complexityColor[result.complexity] }}>
                {result.complexity.toUpperCase()}
              </span>
            </div>
            <div style={s.arrow}>→</div>
            <div style={s.routingItem}>
              <span style={s.routingLabel}>Routed To</span>
              <span style={{ ...s.pill, background: result.tier === "cheap" ? "#6366f1" : "#f59e0b" }}>
                {result.tier === "cheap" ? "💚 CHEAP" : "🔥 STRONG"}
              </span>
            </div>
            <div style={s.arrow}>→</div>
            <div style={s.routingItem}>
              <span style={s.routingLabel}>Model</span>
              <span style={s.modelTag}>{result.model}</span>
            </div>
          </div>

          {/* Response */}
          <div style={s.responseBox}>
            <div style={s.responseLabel}>Response</div>
            <div style={s.responseText}>{result.response}</div>
          </div>

          {/* Cost Metrics */}
          <div style={s.metricsRow}>
            <div style={s.metric}>
              <div style={s.metricValue}>${result.estimated_cost_usd.toFixed(6)}</div>
              <div style={s.metricLabel}>Estimated Cost</div>
            </div>
            <div style={s.metricDivider} />
            <div style={s.metric}>
              <div style={s.metricValue}>{result.input_tokens}</div>
              <div style={s.metricLabel}>Input Tokens</div>
            </div>
            <div style={s.metricDivider} />
            <div style={s.metric}>
              <div style={s.metricValue}>{result.output_tokens}</div>
              <div style={s.metricLabel}>Output Tokens</div>
            </div>
            <div style={s.metricDivider} />
            <div style={s.metric}>
              <div style={s.metricValue}>{result.input_tokens + result.output_tokens}</div>
              <div style={s.metricLabel}>Total Tokens</div>
            </div>
          </div>
        </div>
      )}

      {/* How it works */}
      {!result && !loading && (
        <div style={s.howItWorks}>
          <div style={s.howTitle}>How it works</div>
          <div style={s.steps}>
            {[
              { icon: "📝", label: "You send a prompt" },
              { icon: "🧠", label: "Classifier detects complexity" },
              { icon: "🔀", label: "Router picks cheap or strong tier" },
              { icon: "✅", label: "Evaluator checks quality" },
              { icon: "💰", label: "Cost tracked & returned" },
            ].map((step, i) => (
              <div key={i} style={s.step}>
                <div style={s.stepIcon}>{step.icon}</div>
                <div style={s.stepLabel}>{step.label}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const s: Record<string, React.CSSProperties> = {
  page: { minHeight: "100vh", background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)", color: "#f1f5f9", fontFamily: "'Inter', system-ui, sans-serif", padding: "32px 20px" },
  header: { display: "flex", alignItems: "center", gap: 16, maxWidth: 760, margin: "0 auto 28px" },
  logo: { fontSize: 40, background: "#6366f1", borderRadius: 16, width: 64, height: 64, display: "flex", alignItems: "center", justifyContent: "center" },
  title: { margin: 0, fontSize: 26, fontWeight: 800, letterSpacing: -0.5 },
  subtitle: { margin: "4px 0 0", color: "#94a3b8", fontSize: 14 },
  statsBar: { maxWidth: 760, margin: "0 auto 24px", background: "#1e293b", borderRadius: 12, padding: "14px 24px", display: "flex", alignItems: "center", gap: 16 },
  statItem: { display: "flex", alignItems: "center", gap: 8, flex: 1, justifyContent: "center" },
  statIcon: { fontSize: 18 },
  statText: { fontSize: 13, color: "#cbd5e1", fontWeight: 500 },
  divider: { width: 1, height: 24, background: "#334155" },
  inputCard: { maxWidth: 760, margin: "0 auto 20px", background: "#1e293b", borderRadius: 16, padding: 24 },
  inputLabel: { fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 10, textTransform: "uppercase", letterSpacing: 0.5 },
  textarea: { width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 10, padding: "14px 16px", color: "#f1f5f9", fontSize: 15, resize: "vertical", boxSizing: "border-box", outline: "none", lineHeight: 1.6 },
  inputFooter: { display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 12 },
  hint: { fontSize: 12, color: "#475569" },
  button: { background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", border: "none", borderRadius: 10, padding: "10px 24px", fontSize: 14, cursor: "pointer", fontWeight: 700, letterSpacing: 0.3 },
  buttonLoading: { background: "#334155", color: "#94a3b8", border: "none", borderRadius: 10, padding: "10px 24px", fontSize: 14, cursor: "not-allowed", fontWeight: 700 },
  errorCard: { maxWidth: 760, margin: "0 auto 20px", background: "#450a0a", border: "1px solid #7f1d1d", borderRadius: 12, padding: "14px 20px", display: "flex", alignItems: "flex-start", gap: 10, color: "#fca5a5", fontSize: 13 },
  errorIcon: { fontSize: 18, flexShrink: 0 },
  resultCard: { maxWidth: 760, margin: "0 auto", background: "#1e293b", borderRadius: 16, overflow: "hidden" },
  routingBar: { display: "flex", alignItems: "center", gap: 12, padding: "16px 24px", background: "#0f172a", flexWrap: "wrap" },
  routingItem: { display: "flex", flexDirection: "column", gap: 4, alignItems: "center" },
  routingLabel: { fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 },
  pill: { padding: "4px 14px", borderRadius: 20, fontSize: 12, fontWeight: 700, color: "#fff" },
  arrow: { color: "#475569", fontSize: 18, fontWeight: 700 },
  modelTag: { background: "#1e293b", border: "1px solid #334155", padding: "4px 12px", borderRadius: 8, fontSize: 12, color: "#94a3b8" },
  responseBox: { padding: 24 },
  responseLabel: { fontSize: 12, fontWeight: 600, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 12 },
  responseText: { fontSize: 15, lineHeight: 1.8, color: "#e2e8f0", whiteSpace: "pre-wrap" },
  metricsRow: { display: "flex", borderTop: "1px solid #334155", padding: "16px 24px", gap: 8 },
  metric: { flex: 1, textAlign: "center" },
  metricValue: { fontSize: 20, fontWeight: 800, color: "#6366f1" },
  metricLabel: { fontSize: 11, color: "#64748b", marginTop: 4, textTransform: "uppercase", letterSpacing: 0.5 },
  metricDivider: { width: 1, background: "#334155" },
  howItWorks: { maxWidth: 760, margin: "24px auto 0", background: "#1e293b", borderRadius: 16, padding: 24 },
  howTitle: { fontSize: 13, fontWeight: 600, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 20 },
  steps: { display: "flex", gap: 8, flexWrap: "wrap" },
  step: { flex: 1, minWidth: 120, background: "#0f172a", borderRadius: 12, padding: "16px 12px", textAlign: "center" },
  stepIcon: { fontSize: 24, marginBottom: 8 },
  stepLabel: { fontSize: 12, color: "#94a3b8", lineHeight: 1.4 },
};