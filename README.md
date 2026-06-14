# ♟ Chess Analyzer Pro: Grandmaster Anatoly

**Microsoft Agents League Hackathon 2026 — Creative Apps Track**

> "Chess is a struggle against your own stupidity." — Anatoly (AI Coach)

---

## 🌟 The Vision

**Chess Analyzer Pro** is an AI-powered chess coaching platform that goes beyond simple engine evaluations. It leverages a **Soviet Grandmaster persona** (Grandmaster Anatoly) to provide deep, culturally enriched, and technically grounded feedback on your games.

By combining the structural precision of `python-chess` with the advanced reasoning of **Alibaba Cloud's Qwen 3.7-max**, we've built a coach that doesn't just tell you that you blundered—it identifies the tactical flaws itself, cites historical precedents, and critiques your "bourgeois tactics" with dry Soviet wit.

---

## 💡 Alibaba Cloud & Foundry IQ Integration

This project implements a sophisticated **agentic grounding pattern** powered by **Alibaba Cloud Model Studio**. We solve the "LLM Hallucination" problem in chess coaching by strictly anchoring the AI's personality and tactical advice to a structured knowledge base.

### The Analysis Pipeline:
1.  **Raw Timeline Extraction:** The system uses `python-chess` to extract a clean, chronological log of moves, including capture data, without pre-calculating blunders.
2.  **Semantic Retrieval (Foundry IQ):** The system queries the `FoundryIQ` layer for specific tactical concepts (Pins, Forks, Skewers) and historical opening data relevant to the game.
3.  **Autonomous Reasoning (Qwen 3.7-max):** The raw game log and retrieved context are passed to **Alibaba Cloud's Qwen 3.7-max**. The model uses its advanced chess reasoning to independently deduce blunders, tactical errors, and brilliant moves.
4.  **Soviet Master Persona:** Grandmaster Anatoly delivers the final verdict, strictly incorporating the retrieved facts and formatting the response with a mandated `[MASTER'S JUDGMENT]` rating.

---

## 🧠 Architecture

```
User PGN Input
    │
    ▼
[Chess Engine] ───────► Raw Timeline Extraction (SAN, Captures, Openings)
    │
    ▼
[Foundry IQ] ─────────► Agentic Retrieval of Grounded Tactics & History
    │
    ▼
[Qwen 3.7-max] ───────► Autonomous Tactical Reasoning & Soviet Persona (Alibaba Cloud)
    │
    ▼
[Modern Dashboard] ───► Interactive Timeline & Navigation
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **AI Intelligence** | Alibaba Cloud Qwen 3.7-max (via DashScope) |
| **Knowledge Layer** | Microsoft Foundry IQ Pattern (Agentic Retrieval) |
| **Chess Logic** | python-chess (Move validation & timeline extraction) |
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

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
1.  Create a file named `.env` in the root directory (or rename `env.example`).
2.  Add your **Alibaba Cloud DashScope API Key**:
    ```env
    DASHSCOPE_API_KEY=your_dashscope_api_key_here
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
    *   Read the **Verdict** for Anatoly's immediate (and often stinging) assessment, topped with the `[MASTER'S JUDGMENT]` rating.
    *   Scroll the **Timeline** to see the game's progression.
    *   **Click any move** in the timeline to jump the interactive board to that exact position.

---

*Built for the Microsoft Agents League Hackathon 2026 · Creative Apps Track*
