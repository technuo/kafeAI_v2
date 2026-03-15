# kafeAI Documentation

Welcome to the kafeAI documentation. This guide is organized for two audiences:

- **Café Owners**: Focus on [Getting Started](./02-getting-started.md) for deployment and daily operation
- **Developers**: Explore [Architecture](./03-architecture.md) and [Customization](./04-customization.md) for extending the system

---

## Documentation Structure

| Document | Audience | Purpose |
|----------|----------|---------|
| [1. Project Overview](./01-project-overview.md) | Both | Mission, principles, version history |
| [2. Getting Started](./02-getting-started.md) | Users | Installation, WhatsApp setup, daily operation |
| [3. Architecture & Core Logic](./03-architecture.md) | Developers | LangGraph framework, memory layer, data flow |
| [4. Customization & Extension](./04-customization.md) | Developers | POS adapters, agent tuning, adding new features |
| [5. Compliance & Security](./05-compliance-security.md) | Both | GDPR, security best practices, license |

---

## Quick Links

### For Café Owners

- [Prerequisites](./02-getting-started.md#prerequisites) — Hardware and software requirements
- [One-Click Deployment](./02-getting-started.md#one-click-deployment) — Run `setup.bat` and go
- [Daily Operation](./02-getting-started.md#daily-operation) — WhatsApp commands and HITL approval
- [Troubleshooting](./02-getting-started.md#troubleshooting) — Common issues and solutions

### For Developers

- [Agentic Framework](./03-architecture.md#agentic-framework) — How LangGraph orchestrates agents
- [The Memory Layer](./03-architecture.md#the-memory-layer) — Understanding data persistence
- [Integrating New POS](./04-customization.md#integrating-new-pos-systems) — Build adapters for new systems
- [Vision Agent Tuning](./04-customization.md#vision-agent-tuning) — Adapt OCR for different countries
- [Adding New Agents](./04-customization.md#adding-new-agent-nodes) — Extend the agent graph

---

## System Architecture at a Glance

```
User (WhatsApp)
    ↓
WhatsApp Bot (Playwright)
    ↓
Manager Agent (Router)
    ↓
Specialist Agents (Weather, Inventory, Finance, Creative)
    ↓
Data Layer (memory.json, daily_reports/, stock.json)
```

---

## Contributing to Documentation

Found an error or want to improve the docs?

1. Fork the repository
2. Edit the relevant `.md` file in `/docs`
3. Submit a Pull Request

Documentation improvements are always welcome!

---

## License

This documentation is licensed under [Apache 2.0](../LICENSE).

Copyright 2026 kafeAI Contributors
