import { useState, useRef, useEffect } from "react";
import "./App.css";

const MODEL_OPTIONS = [
  { label: "GPT", value: "GPT" },
  { label: "LLAMA", value: "LLAMA" },
];

const DARK_THEME = {
  background: "#151A21",
  card: "#212733",
  accent: "#4FD1C5",
  accentLight: "#2D3748",
  userBubble: "#22577A",
  aiBubble: "#1A2636",
  text: "#E3EAF2",
  input: "#232B36",
  border: "#293042",
  placeholder: "#6A7B93",
  clearBtn: "#D7263D",
};

function App() {
  const [model, setModel] = useState("GPT");
  const [chatHistory, setChatHistory] = useState([
    {
      role: "assistant",
      content: "Hi! How can I assist you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streamingMsg, setStreamingMsg] = useState("");
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory, streamingMsg]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: "user", content: input };
    setChatHistory((ch) => [...ch, userMsg]);
    setInput("");
    setLoading(true);
    setStreamingMsg("");

    try {
      const response = await fetch("http://localhost:5698/chat", {
        method: "POST",
        body: JSON.stringify({
          message: input,
          history: chatHistory.map(m => ({ role: m.role, content: m.content })),
          model_choice: model,
        }),
        headers: { "Content-Type": "application/json" },
      });

      const reader = response.body.getReader();
      let aiMsg = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = new TextDecoder().decode(value);
        aiMsg += chunk;
        setStreamingMsg(aiMsg);
      }
      setChatHistory((ch) => [...ch, { role: "assistant", content: aiMsg }]);
      setStreamingMsg("");
    } catch (err) {
      console.error(err);
      setStreamingMsg("Error connecting to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: DARK_THEME.background, color: DARK_THEME.text, display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
      <div style={{ background: DARK_THEME.card, borderRadius: "15px", width: "100%", maxWidth: "600px", border: `1px solid ${DARK_THEME.border}`, overflow: "hidden" }}>
        <div style={{ padding: "20px", background: DARK_THEME.accentLight, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ color: DARK_THEME.accent, margin: 0 }}>Manos PrivateLLMchat</h2>
          <select value={model} onChange={(e) => setModel(e.target.value)} style={{ background: DARK_THEME.background, color: "#fff", padding: "5px", borderRadius: "5px" }}>
            {MODEL_OPTIONS.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
          </select>
        </div>

        <div ref={chatBoxRef} style={{ height: "400px", overflowY: "auto", padding: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>
          {chatHistory.map((msg, i) => (
            <div key={i} style={{ alignSelf: msg.role === "user" ? "flex-end" : "flex-start", background: msg.role === "user" ? DARK_THEME.userBubble : DARK_THEME.aiBubble, padding: "10px", borderRadius: "10px", maxWidth: "80%" }}>
              {msg.content}
            </div>
          ))}
          {streamingMsg && <div style={{ alignSelf: "flex-start", background: DARK_THEME.aiBubble, padding: "10px", borderRadius: "10px" }}>{streamingMsg}</div>}
        </div>

        <div style={{ padding: "20px", borderTop: `1px solid ${DARK_THEME.border}`, display: "flex", gap: "10px" }}>
          <input 
            value={input} 
            onChange={(e) => setInput(e.target.value)} 
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            style={{ flex: 1, background: DARK_THEME.input, border: "none", color: "#fff", padding: "10px", borderRadius: "5px" }} 
            placeholder="Type your message..."
          />
          <button onClick={handleSend} disabled={loading} style={{ background: DARK_THEME.accent, color: "#000", border: "none", padding: "10px 20px", borderRadius: "5px", cursor: "pointer" }}>
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;