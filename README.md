# ♟ Chess Analyzer Pro: Grandmaster Anatoly

**Microsoft Agents League Hackathon 2026 — Creative Apps Track**

> "Chess is a struggle against your own stupidity." — Anatoly (AI Coach)

---

## 🌟 The Vision

**Chess Analyzer Pro** is an AI-powered chess coaching platform that uses the **Microsoft Foundry IQ agentic grounding pattern** to create a high-fidelity educational experience. It features **Grandmaster Anatoly**, a strict 1980s Soviet Master persona that provides deep, technically grounded, and culturally enriched feedback.

---

## 💡 Microsoft IQ Integration (Foundry IQ)

This project is a flagship implementation of **Foundry IQ**. We solve the "LLM Hallucination" problem in chess coaching by strictly anchoring the AI's personality and tactical advice to a structured knowledge base.

### The Analysis Pipeline:
1.  **Foundry IQ Semantic Retrieval:** The system queries a specialized knowledge index for tactical concepts (Pins, Forks, Skewers) and historical opening data relevant to the specific game state.
2.  **Grounded Reasoning:** Using advanced LLM reasoning, the system processes a raw chronological log of moves.
3.  **Knowledge Injection:** The retrieved "Facts" from the **Foundry IQ intelligence layer** are injected into the prompt, mandating that the coach cites his sources (e.g., "Foundry IQ Archives").
4.  **Result:** Accurate, cited, and high-fidelity coaching that feels like a real lesson from a grandmaster.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Intelligence Layer** | **Microsoft Foundry IQ Pattern** (Grounded Retrieval) |
| **Reasoning Engine** | Qwen 3.7-max (via Alibaba Cloud Model Studio) |
| **Chess Logic** | `python-chess` (Raw timeline extraction) |
| **Backend** | Flask (Python 3.14+) |
| **Frontend** | Interactive CSS Dashboard + chessboard.js |

---

## 🚀 Quick Start (Judge's Guide)

### 1. Configure Your Environment
Create a `.env` file and add your DashScope API key:
```env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

### 2. Launch the Server
```bash
pip install -r requirements.txt
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🏆 Evaluation Criteria Alignment
- **Accuracy & Relevance:** Uses Foundry IQ for grounded, cited coaching.
- **Reasoning:** AI independently deduces blunders from raw SAN logs.
- **Creativity:** Unique 1980s Soviet persona and interactive timeline.
- **Safety:** Secure environment variable management and robust text parsing.

---

## 📽️ Demo Video
**[Click here to watch the Grandmaster Anatoly Demo Video](https://youtu.be/Io7gTIgcSUA)**

---

*Built for the Microsoft Agents League Hackathon 2026*
