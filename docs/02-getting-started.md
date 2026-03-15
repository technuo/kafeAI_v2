# 2. Getting Started

This guide covers everything you need to deploy and use kafeAI — from hardware requirements to daily operations.

---

## Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Device** | Any Windows PC/laptop | Industrial PC (工控机) for 24/7 operation |
| **RAM** | 4 GB | 8 GB |
| **Storage** | 10 GB free space | SSD for faster I/O |
| **Internet** | Stable broadband | Dedicated connection |
| **Display** | Not required for operation | Monitor for initial setup |

### Software Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Python**: Version 3.9 or higher
- **Browser**: Chrome or Edge (for WhatsApp Web)
- **WhatsApp**: Active mobile account with QR code capability

### API Keys Required

Before starting, you'll need to obtain these API keys:

1. **Google Gemini API Key** (for AI reasoning)
   - Get it from: https://makersuite.google.com/app/apikey
   - Free tier: 1,500 requests/day

2. **WeatherAPI Key** (for weather forecasting)
   - Get it from: https://www.weatherapi.com/
   - Free tier: 1 million calls/month

---

## One-Click Deployment

### Step 1: Download and Extract

1. Download the latest kafeAI release
2. Extract to a folder (e.g., `C:\kafeAI\`)
3. Ensure you have a stable internet connection

### Step 2: Run Setup

1. Double-click **`setup.bat`** in the `kafeAI` folder
2. The wizard will automatically:
   - Check Python installation
   - Create virtual environment
   - Install dependencies
   - Guide you through API key configuration
   - Launch the application

```
╔════════════════════════════════════════╗
║         Welcome to kafeAI Setup        ║
╚════════════════════════════════════════╝
[✓] Python 3.11 detected
[✓] Virtual environment created
[✓] Dependencies installed
[?] Enter your Google Gemini API Key: _
[?] Enter your WeatherAPI Key: _
[✓] Configuration saved

Launching kafeAI...
```

### Step 3: WhatsApp QR Code Scan

On first launch:

1. A browser window will open with **WhatsApp Web**
2. Open WhatsApp on your phone
3. Go to **Settings > Linked Devices > Link a Device**
4. Scan the QR code displayed on screen
5. Wait for "Session connected" confirmation

**Session Persistence**: Once authenticated, kafeAI will maintain the session in the `whatsapp_session/` folder. You only need to re-scan if:
- You manually log out from WhatsApp Web
- The session expires (after ~14 days of inactivity)
- You delete the `whatsapp_session` folder

---

## Daily Operation

### Automated Daily Decisions

Every morning, kafeAI automatically:

1. **Fetches weather forecast** for tomorrow
2. **Analyzes inventory** against menu and storage targets
3. **Generates pricing strategy** based on demand signals
4. **Sends you a decision summary** via WhatsApp

Example morning message:

```
📊 kafeAI Daily Strategy — 2026-03-16

🌤️ Weather: Sunny, -5°C. Rain: 0%
📦 Inventory Alert: Burger bröd (3/10 cartons) — LOW
💰 Pricing: Lunch combo ↑10% (high demand expected)
📢 Poster: "Warm Up Wednesday" campaign ready

Reply APPROVE to execute, or reply with changes.
```

### On-Demand Agent Queries (@Mentions)

Interact with specific agents using `@` mentions:

| Command | Description | Example Response |
|---------|-------------|------------------|
| `@Finance` | Analyze sales, costs, pricing | "Yesterday's revenue was 5,114 SEK. Recommend 12% price increase on weekends." |
| `@Inventory` | Check stock levels, reorder alerts | "Low stock: burger bröd (3 cartons). Suggest order: 5 cartons." |
| `@Creative` | Generate marketing content | Creates promotional poster with today's specials |
| `@Weather` | Get forecast and recommendations | "Tomorrow: Sunny, -3°C. Expect 20% more foot traffic." |

**Example Conversations:**

```
You: @Finance how did we do yesterday?
kafeAI: 📈 Yesterday (Feb 17): Total revenue 5,114 SEK
        - Food: 3,422 SEK (67%)
        - Beverages: 1,582 SEK (31%)
        - Average ticket: 146 SEK

        💡 Insight: 28 food orders with strong attach rate.

You: @Inventory what should I order?
kafeAI: 📦 Reorder Recommendations:
        URGENT: Burger bröd (3 → order 5)
        LOW: Tomat (2 cartons → order 3)
        OK: All other items above threshold

You: @Creative make a poster for tomorrow
kafeAI: 🎨 Generated: "Sunny Tuesday Special"
        Location: generated_assets/poster_20260316.png

        Featuring: BBQ Bacon Burger + Iced Coffee combo
        Optimized for: Instagram Stories (9:16)
```

### Human-in-the-Loop (HITL) Approval

For critical decisions, kafeAI requires explicit approval:

1. **Stock Updates**: Before modifying `stock.json`
2. **Price Changes**: Before applying dynamic pricing
3. **Bulk Orders**: Before confirming large inventory purchases

**Approval Flow:**

```
kafeAI: ⚠️ ACTION REQUIRED

        Proposed: Update "burger bröd" from 3 → 8 cartons
        Reason: Forecast shows high demand Tue-Wed

        Reply: APPROVE  or  REJECT

You: APPROVE

kafeAI: ✅ Stock updated. 5 cartons added to order queue.
```

---

## Dashboard Access (Optional)

For detailed analytics and manual overrides:

1. Open browser to: `http://localhost:8501`
2. The Streamlit dashboard provides:
   - Real-time inventory visualization
   - Historical sales charts
   - Agent decision logs
   - Manual stock adjustment interface

**Note**: The dashboard is optional. All core functionality works through WhatsApp.

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python 3.9+ and check "Add to PATH" |
| WhatsApp QR expires | Close browser, delete `whatsapp_session/`, restart |
| "API key invalid" | Verify keys in `kafeAI/.env` file |
| Slow responses | Check internet connection; Gemini API may be throttled |
| No messages received | Ensure your phone number is in `.env` as `WHATSAPP_PHONE_NUMBER` |

### Getting Help

1. Check the [Architecture Guide](./03-architecture.md) for technical details
2. Review [Customization Guide](./04-customization.md) for extensions
3. File an issue on GitHub with logs from `logs/` directory

---

## Next Steps

- Learn about the [Architecture & Core Logic](./03-architecture.md)
- Explore [Customization options](./04-customization.md)
- Review [Security & Compliance](./05-compliance-security.md)
