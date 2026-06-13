# ♟ Chess Analyzer Pro: Grandmaster Anatoly

**Microsoft Agents League Hackathon 2026 — Creative Apps Track**

> "Chess is a struggle against your own stupidity." — Anatoly (AI Coach)

---

## 🌟 The Vision

**Chess Analyzer Pro** is an AI-powered chess coaching platform that goes beyond simple engine evaluations. It leverages a **Soviet Grandmaster persona** (Grandmaster Anatoly) to provide deep, culturally enriched, and technically grounded feedback on your games.

By combining the structural precision of `python-chess` with the agentic knowledge retrieval patterns of **Microsoft Foundry IQ**, we've built a coach that doesn't just tell you that you blundered—it tells you *why*, cites historical precedents, and critiques your "bourgeois tactics" with dry Soviet wit.

---

## 💡 Microsoft Foundry IQ Integration

This project is a flagship implementation of the **Foundry IQ agentic grounding pattern**. We solve the "LLM Hallucination" problem in chess coaching by strictly anchoring the AI's personality and tactical advice to a structured knowledge base.

### The Foundry IQ Pipeline:
1.  **Semantic Retrieval:** When a game is analyzed, the system queries the `FoundryIQ` layer for specific tactical concepts (Pins, Forks, Skewers) and historical opening data relevant to *that specific game state*.
2.  **Contextual Grounding:** The retrieved "Facts" (e.g., Mikhail Tal quotes, 16th-century opening origins) are injected into the LLM prompt.
3.  **Mandated Reasoning:** The Gemini 2.0 model is explicitly instructed to **rely fully** on these retrieved facts as its primary source of truth, citing them like a human researcher would.
4.  **Result:** Accurate, cited, and high-fidelity coaching that feels grounded in centuries of chess history.

---

## 🧠 Architecture

```
User PGN Input
    │
    ▼
[Chess Engine] ───────► Heuristic Move Analysis (Blunders, Checks, Openings)
    │
    ▼
[Foundry IQ] ─────────► Agentic Retrieval of Grounded Tactics & History
    │
    ▼
[Gemini 2.0] ─────────► Soviet Master Persona Generation (Grounded in IQ Context)
    │
    ▼
[Modern Dashboard] ───► Interactive Timeline & Navigation
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **AI Intelligence** | Google Gemini 2.0 Flash (Cloud API) |
| **Knowledge Layer** | Microsoft Foundry IQ Pattern (Agentic Retrieval) |
| **Chess Logic** | python-chess (Move validation & heuristics) |
| **Backend** | Flask (Python 3.14+) |
| **Frontend** | Modern CSS Dashboards + chessboard.js + chess.js |

---

## 🚀 Quick Start (Judge's Guide)

Follow these steps to launch the dashboard and consult with Grandmaster Anatoly in under 2 minutes.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/chess-analyzer
cd chess-analyzer
```

### 2. Install Lean Dependencies
We use a lightweight footprint. No heavy local models are required.
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
1.  Create a file named `.env` in the root directory (or rename `env.example`).
2.  Add your [Google AI Studio API Key](https://aistudio.google.com/app/apikey):
    ```env
    GEMINI_API_KEY=your_free_api_key_here
    ```

### 4. Launch the Server
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🎮 How to Use the Dashboard

1.  **Paste a PGN:** Use the pre-loaded sample or paste any game from Lichess/Chess.com.
2.  **Analyze:** Click **Analyze PGN**. Grandmaster Anatoly will review the "struggle on the 64 squares."
3.  **Interact:** 
    *   Read the **Verdict** for Anatoly's immediate (and often stinging) assessment.
    *   Scroll the **Timeline** to see move-by-move alerts.
    *   **Click any move** in the timeline to jump the interactive board to that exact position.

---

*Built for the Microsoft Agents League Hackathon 2026 · Creative Apps Track*
