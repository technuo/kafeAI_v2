# 5. Compliance & Security

This document covers how kafeAI handles data privacy, security, and regulatory compliance — particularly GDPR for EU operations.

---

## GDPR Implementation

### Data Sovereignty by Design

kafeAI's core architecture aligns with GDPR principles through **local-first data storage**:

| GDPR Principle | kafeAI Implementation |
|---------------|----------------------|
| **Data Minimization** | Only collects operational data necessary for decisions (sales, inventory, weather) |
| **Purpose Limitation** | Data is used solely for café operations, never shared with third parties |
| **Storage Limitation** | Historical data retained locally based on user-configurable retention policy |
| **Integrity & Confidentiality** | All data stored on local device; encrypted at rest via OS-level encryption |
| **Accountability** | Transparent logging of all AI decisions in `memory.json` |

### Local-Only Data Storage

```
┌─────────────────────────────────────────────────────────────┐
│                  kafeAI Data Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   LOCAL DEVICE (Your Café)         EXTERNAL SERVICES       │
│   ═════════════════════════        ═══════════════════     │
│                                                             │
│   ┌─────────────────────┐         ┌─────────────────┐      │
│   │ memory.json         │         │ Google Gemini   │      │
│   │ (Decision history)  │         │ (AI reasoning)  │      │
│   └─────────────────────┘         └─────────────────┘      │
│                                                             │
│   ┌─────────────────────┐         ┌─────────────────┐      │
│   │ daily_reports/      │         │ WeatherAPI      │      │
│   │ (Sales data)        │────────▶│ (Forecast only) │      │
│   └─────────────────────┘         └─────────────────┘      │
│                                                             │
│   ┌─────────────────────┐                                  │
│   │ stock.json          │                                  │
│   │ (Inventory)         │                                  │
│   └─────────────────────┘                                  │
│                                                             │
│   ★ NO cloud sync    ★ NO external database               │
│   ★ NO analytics     ★ NO data sharing                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**What leaves your device:**
- Weather API requests (city name only, no business data)
- Gemini API requests (anonymized queries for AI processing)

**What stays local:**
- All sales figures and financial data
- Customer information (if any)
- Inventory levels and supplier details
- Decision history and business strategies

### Data Processing Agreement (DPA)

When using third-party APIs:

| Service | Data Shared | DPA Available |
|---------|-------------|---------------|
| Google Gemini | Anonymized queries only | [Yes](https://cloud.google.com/terms/data-processing-terms) |
| WeatherAPI | City name | [Yes](https://www.weatherapi.com/privacy.aspx) |
| WhatsApp (via Playwright) | Messages sent by you | Meta's standard terms |

**Recommendation**: For maximum privacy, self-host an open-source LLM (e.g., Llama 3 via Ollama) instead of using Google Gemini.

### Subject Access Requests

All personal/business data is stored in plain JSON files. To fulfill a data access request:

```bash
# Generate a complete data export
python -c "
import json
import os

data_export = {}

# Load all data files
for file in ['memory.json', 'stock.json']:
    if os.path.exists(file):
        with open(file, 'r') as f:
            data_export[file] = json.load(f)

# Export daily reports
import glob
data_export['daily_reports'] = []
for report_file in glob.glob('daily_reports/*.json'):
    with open(report_file, 'r') as f:
        data_export['daily_reports'].append(json.load(f))

# Write export
with open('data_export.json', 'w') as f:
    json.dump(data_export, f, indent=2)

print('✓ Data export generated: data_export.json')
"
```

### Right to Erasure

To completely delete all data:

```bash
# Windows (run in kafeAI directory)
del memory.json
del stock.json
rmdir /s /q daily_reports
rmdir /s /q whatsapp_session
rmdir /s /q decision_history

# Linux/Mac
rm memory.json stock.json
rm -rf daily_reports/ whatsapp_session/ decision_history/
```

---

## Security Best Practices

### API Key Management

1. **Never commit `.env` to git**
   ```bash
   # .gitignore
   .env
   *.env
   ```

2. **Use environment-specific keys**
   ```bash
   # Development
   GOOGLE_API_KEY=dev_key_here

   # Production (different key with usage limits)
   GOOGLE_API_KEY=prod_key_here
   ```

3. **Rotate keys quarterly**
   - Google Cloud Console → APIs & Services → Credentials
   - WeatherAPI → Account Settings → API Key

4. **Monitor API usage**
   ```python
   # Add to manageragent.py
   import logging

   logging.basicConfig(
       filename='logs/api_usage.log',
       level=logging.INFO
   )

   def log_api_call(service: str, tokens_used: int):
       logging.info(f"{service}: {tokens_used} tokens")
   ```

### WhatsApp Security

1. **Session Isolation**
   - WhatsApp Web session is isolated to `whatsapp_session/` folder
   - No other application can access this session
   - Session cookies are stored locally

2. **Phone Number Verification**
   - Only configured number can trigger automated responses
   - Unknown numbers receive: "This kafeAI instance is private."

3. **QR Code Security**
   - QR codes expire after 60 seconds
   - Re-authentication required every 14 days (WhatsApp default)
   - Session folder can be deleted to force re-auth

### File System Security

```python
# File permissions (Unix/Linux)
os.chmod('memory.json', 0o600)  # Owner read/write only
os.chmod('stock.json', 0o600)
os.chmod('.env', 0o600)

# Windows equivalent (using icacls)
# Not directly supported in Python, document for users:
```

**Windows Users**: Right-click file → Properties → Security → Advanced → Disable inheritance → Remove all users except your account.

### Network Security

1. **Firewall Rules**
   - Only outbound connections required
   - Block inbound ports (kafeAI doesn't need to accept external connections)

2. **API Communication**
   - All external APIs use HTTPS
   - Certificate verification enabled by default

3. **WhatsApp Web**
   - Uses wss:// (WebSocket Secure) for real-time messaging
   - Same security as standard WhatsApp Web

---

## Audit and Logging

### Decision Audit Trail

Every AI decision is logged with:

```json
{
  "episodes": [
    {
      "date": "2026-02-15",
      "timestamp": "2026-02-14T20:00:00Z",
      "prediction_summary": "Forecast: Sunny, -13.9°C",
      "decision": "Indoor Yield Maximization strategy",
      "decision_hash": "sha256:a1b2c3...",
      "status": "PENDING",
      "approved_by": "human",
      "approval_timestamp": "2026-02-14T20:05:00Z",
      "bias_correction": ""
    }
  ]
}
```

### Access Logging

Enable access logging for compliance:

```python
# logging_config.py
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename=f'logs/access_{datetime.now().strftime("%Y%m")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_decision_access(user: str, decision_id: str, action: str):
    logging.info(f"User: {user}, Decision: {decision_id}, Action: {action}")
```

---

## Compliance Checklist

### Pre-Deployment

- [ ] API keys secured in `.env` (not in code)
- [ ] `.env` added to `.gitignore`
- [ ] File permissions set correctly
- [ ] No personal customer data in training data
- [ ] WhatsApp number verified
- [ ] Data retention policy documented

### Ongoing

- [ ] Review API key usage monthly
- [ ] Rotate API keys quarterly
- [ ] Archive old daily reports (older than 2 years)
- [ ] Review decision logs for accuracy
- [ ] Test data export/erasure procedures

### Incident Response

If data breach suspected:

1. **Immediate (0-24 hours)**
   - Rotate all API keys
   - Check access logs for unauthorized access
   - Preserve evidence (don't delete logs)

2. **Assessment (24-72 hours)**
   - Determine scope of breach
   - Identify if personal data was accessed
   - Document timeline

3. **Notification (if required)**
   - GDPR requires notification within 72 hours
   - Contact: datainspektionen@datainspektionen.se (Sweden)

---

## License

### Apache 2.0 Summary

kafeAI is published under the Apache License 2.0:

```
Copyright 2026 kafeAI Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

### What This Means

| You Can | You Must | You Cannot |
|---------|----------|------------|
| Use commercially | Include copyright notice | Hold liable |
| Modify | Include license text | Use trademarks |
| Distribute | State changes | |
| Patent use | | |
| Use privately | | |

### Third-Party Dependencies

kafeAI uses the following open-source packages (all Apache/MIT/BSD licensed):

| Package | License | Purpose |
|---------|---------|---------|
| LangGraph | MIT | Agent orchestration |
| LangChain | MIT | LLM framework |
| Streamlit | Apache 2.0 | Dashboard UI |
| Playwright | Apache 2.0 | WhatsApp automation |
| Google Generative AI | Apache 2.0 | LLM client |

---

## Security Contacts

Report security vulnerabilities:

- Email: security@kafeai.dev (fictional example)
- GitHub: Create a private security advisory
- Response time: Within 48 hours

**Please do not disclose security issues publicly until they are resolved.**
