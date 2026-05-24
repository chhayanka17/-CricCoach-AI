# 🏏 CricCoach AI — 60 Second Pitch

> Built at GDG Raipur × IPL Hackathon 2025 | Solo | 2.5 Hours | Python + Streamlit

---

## The Problem

During a live IPL match, a captain makes **50+ micro-decisions** — bowling changes, field settings, batting orders — often in under 30 seconds with 50,000 fans watching.

There is no tool that answers *"what should the captain do RIGHT NOW?"* using real historical data, in real time.

---

## What I Built

**CricCoach AI** — a data-driven live match strategy advisor.

You update the live scoreboard. It scans **243,815 real IPL deliveries** from 2008–2024 and tells you:

- ✅ What to do **right now**
- 📊 **Why** — based on real historical patterns
- ⚠️ What the **risk** is

---

## The Demo

> *Update the sidebar with the live match score on screen.*
> *Type the current bowler and striker.*
> *Click Analyze Now.*

The app finds every historically similar situation — same over, same pressure, same phase — and tells you what worked and what didn't across 16 seasons of IPL cricket.

---

## Why It's Agentic

This isn't a chatbot. Every single query is **automatically enriched with the live match context** from the scoreboard.

```
Scoreboard updates  →  context auto-injected  →  AI reasons over live state  →  strategy output
        ↑                                                                               |
        └───────────────── captain updates score next over ────────────────────────────┘
```

Change one number. The entire reasoning changes. That's the agentic pattern — **reasoning over a changing environment, not just a static question.**

---

## What the Output Looks Like

For input: *MI chasing 185, score 142/4, over 16, RRR 12.4, Hardik batting, Chahal bowling*

```
Phase: Death Overs  |  Pressure: 🔴 CRITICAL

Bowler — YS Chahal
  Economy: 8.4  |  Wickets: 47  |  Dot%: 38%  |  Boundary%: 18%
  ⚠️ Consider change — leaks runs in death overs

Striker — HH Pandya  
  SR: 162.3  |  Boundary%: 24%  |  Six%: 11%
  ✅ Keep on strike — dangerous in this phase

Recommended Action:
  ATTACK NOW — RRR 12.4 is near impossible with dots.
  Keep Hardik on strike. Target Chahal for maximums.

Risk:
  Going reckless risks losing Hardik. Any wicket from
  here = near impossible chase.
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Data engine | Pandas |
| Dataset | IPL Ball-by-Ball 2008–2024 (Kaggle) |
| Language | Python 3.10+ |
| Internet needed | ❌ Fully offline |
| API key needed | ❌ None |

---

## Why This Over a Generic AI Chatbot

| | ChatGPT / Generic AI | CricCoach AI |
|---|---|---|
| Data source | Training knowledge | 243,815 real deliveries |
| Hallucination risk | High | None — pure data |
| Works offline | ❌ | ✅ |
| API key needed | ✅ | ❌ |
| Updates with match | ❌ | ✅ Live context |
| Explainable output | Sometimes | Always — shows source |

---

## Built By

**Chhayanka Dabhadker** 
GDG Raipur × IPL Hackathon 2025  

[GitHub](https://github.com/yourusername/criccoach-ai) · [LinkedIn](https://linkedin.com/in/yourprofile)
