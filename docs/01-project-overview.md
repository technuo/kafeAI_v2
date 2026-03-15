# 1. Project Overview

## Mission Statement

**kafeAI** is a real-world, field-tested AI system built to solve a specific problem:

> *"How can a small café owner in Sweden make better operational decisions every day — without needing a data team, a dashboard, or any technical background?"*

Specifically, kafeAI addresses two pain points in the hospitality industry:

1. **Data Sovereignty**: Small businesses generate rich operational data (daily sales, inventory, costs), but this data is typically locked inside POS systems or ignored entirely. kafeAI liberates this data into a structured "Digital Twin" of the café and makes it actionable.

2. **Decision Automation**: Managers make dozens of decisions daily — what to order, how many staff to schedule, what promotions to run. kafeAI automates this reasoning pipeline using a multi-agent orchestration system powered by LangGraph and Google Gemini, then delivers decisions via WhatsApp — the channel the manager is already using.

---

## The "Field Project" Concept

kafeAI is not a demo. It runs live at a real café in **Sundsvall, Sweden** (59°N — where weather patterns heavily influence hospitality demand).

The core philosophy is what we call **"Real-World AI"**:

- Code is tested in production, not just in a notebook.
- Failure is documented (see the *Failure Log* in each newsletter issue).
- The system must be operated by a non-technical café owner, not a developer.

This "field project" context drives every architectural decision: from using WhatsApp (instead of a custom app) as the primary UI, to building a Setup Bot that eliminates the need for any terminal interaction.

---

## Core Principles

| Principle | Implementation |
|---|---|
| **Data stays local** | All data files (`stock.json`, `memory.json`, `daily_reports/`) are stored on the local machine. No cloud sync by default. |
| **Messaging as the OS** | The primary interaction layer is WhatsApp, not a web dashboard. The best UI for a café manager is no UI. |
| **Agents, not just models** | kafeAI is built on LangGraph. Each "Agent Node" is a specialist (Inventory, Finance, Weather, Pricing), and they collaborate sequentially to produce a holistic strategy. |
| **Human remains in the loop** | Critical decisions are presented for human approval (HITL) before the system executes automated actions like updating `stock.json`. |
| **Open and extendable** | Published under Apache 2.0. Designed for other developers to fork, adapt to a new POS format, or extend with new agent nodes. |

---

## Version History

| Version | Key Feature | Newsletter Issue |
|---|---|---|
| v1.0 | CLI-based multi-agent pipeline | Issue 001–008 |
| v2.0 | Streamlit GUI Dashboard + HITL approval system | Issue 009–010 |
| v2.1 | WhatsApp integration via Playwright (Messaging OS) | Issue 011 |
| v2.2 | One-Click Setup Bot (`setup.bat`) for non-technical deployment | Issue 012 |
| v2.3 | `@mention` on-demand routing (Single Agent Mode) | Issue 013 |

---

## System at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    kafeAI v2.3 Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  User Layer        │  WhatsApp (via Playwright)              │
│  Interaction       │  Streamlit Dashboard (HITL Approval)    │
├─────────────────────────────────────────────────────────────┤
│  Orchestration     │  LangGraph Workflow Engine              │
│                    │  Manager Agent (Router)                 │
├─────────────────────────────────────────────────────────────┤
│  Specialist        │  ┌─────────────┐  ┌─────────────────┐  │
│  Agents            │  │  Weather    │  │  Inventory      │  │
│                    │  │  (Forecast) │  │  (Stock/Menu)   │  │
│                    │  └─────────────┘  └─────────────────┘  │
│                    │  ┌─────────────┐  ┌─────────────────┐  │
│                    │  │  Finance    │  │  Creative       │  │
│                    │  │  (Pricing)  │  │  (Posters)      │  │
│                    │  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Data Layer        │  memory.json (Long-term Memory)         │
│                    │  daily_reports/ (Historical Data)       │
│                    │  stock.json (Real-time Inventory)       │
│                    │  Menu.md (Product Catalog)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Target Users

### Café Owners (End Users)
- Zero technical background required
- Interact entirely through WhatsApp
- Receive daily operational decisions automatically
- Approve critical actions via simple responses

### Developers (Contributors)
- Extend agent capabilities
- Integrate new POS systems
- Customize for different hospitality contexts
- Build on top of the LangGraph framework
