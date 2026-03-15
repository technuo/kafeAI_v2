# 4. Customization & Extension

This guide is for developers who want to adapt kafeAI to new contexts — different POS systems, new locations, or specialized agent behaviors.

---

## Integrating New POS Systems

kafeAI is designed to work with any POS system that can export sales data. The current implementation parses JSON exports from **AnkerPOS** (Swedish system).

### The POS Adapter Pattern

To add a new POS system, create an adapter that converts its format to kafeAI's standard:

```python
# pos_adapters/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class POSAdapter(ABC):
    """Base class for POS system adapters."""

    @abstractmethod
    def parse_report(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert POS-specific format to kafeAI standard.

        Returns:
            {
                "report_info": {...},
                "sales_summary": {...},
                "sales_by_category": [...],
                "payment_methods": {...},
                "performance_metrics": {...}
            }
        """
        pass

    @abstractmethod
    def detect_format(self, file_path: str) -> bool:
        """Check if this adapter can handle the given file."""
        pass
```

### Example: Square POS Adapter

```python
# pos_adapters/square_adapter.py
import json
from datetime import datetime
from .base import POSAdapter

class SquareAdapter(POSAdapter):
    """Adapter for Square POS JSON exports."""

    def detect_format(self, file_path: str) -> bool:
        """Check for Square-specific fields."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return 'location_id' in data and 'payment_id' in str(data)
        except:
            return False

    def parse_report(self, raw_data: dict) -> dict:
        """Convert Square format to kafeAI standard."""

        # Square uses different field names
        payments = raw_data.get('payments', [])

        total_gross = sum(p['total_money']['amount'] for p in payments) / 100
        total_vat = sum(p.get('tax_money', {}).get('amount', 0) for p in payments) / 100

        # Categorize items (you'll need to map Square categories to kafeAI categories)
        category_map = {
            'Beverages': 'VARM DRYCK (热饮)',
            'Food': 'MAT (食物)',
            'Desserts': 'BAKVERK (甜点)',
        }

        sales_by_category = []
        for category, kafeai_category in category_map.items():
            items = [p for p in payments if self._get_category(p) == category]
            amount = sum(p['total_money']['amount'] for p in items) / 100
            count = len(items)

            sales_by_category.append({
                "category": kafeai_category,
                "count": count,
                "amount": amount
            })

        return {
            "report_info": {
                "report_type": "SQUARE_POS_EXPORT",
                "company_name": raw_data.get('location_id', 'Unknown'),
                "period_start": self._parse_time(payments[0]['created_at']),
                "period_end": self._parse_time(payments[-1]['created_at']),
            },
            "sales_summary": {
                "total_gross": total_gross,
                "total_net": total_gross - total_vat,
                "total_vat": total_vat,
            },
            "sales_by_category": sales_by_category,
            "payment_methods": {
                "card": sum(p['total_money']['amount'] for p in payments
                           if p['source_type'] == 'CARD') / 100,
                "cash": sum(p['total_money']['amount'] for p in payments
                           if p['source_type'] == 'CASH') / 100,
                "total_transactions": len(payments),
            },
            "performance_metrics": {
                "average_purchase_per_customer": total_gross / len(payments) if payments else 0
            }
        }

    def _parse_time(self, timestamp: str) -> str:
        """Parse Square timestamp to kafeAI format."""
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def _get_category(self, payment: dict) -> str:
        """Extract category from payment (Square-specific logic)."""
        # Implementation depends on Square's data structure
        items = payment.get('itemizations', [])
        if items:
            return items[0].get('item_detail', {}).get('category_name', 'Unknown')
        return 'Unknown'
```

### Auto-Detection Router

```python
# pos_adapters/__init__.py
import os
from typing import List
from .base import POSAdapter
from .anker_adapter import AnkerAdapter
from .square_adapter import SquareAdapter

# Register all adapters
ADAPTERS: List[POSAdapter] = [
    AnkerAdapter(),
    SquareAdapter(),
    # Add your adapter here
]

def parse_pos_report(file_path: str) -> dict:
    """Auto-detect POS format and parse."""

    for adapter in ADAPTERS:
        if adapter.detect_format(file_path):
            print(f"✓ Detected format: {adapter.__class__.__name__}")
            with open(file_path, 'r') as f:
                raw_data = json.load(f)
            return adapter.parse_report(raw_data)

    raise ValueError(f"Unknown POS format for file: {file_path}")
```

### Integration with kafeAI

```python
# In your agent code
from pos_adapters import parse_pos_report

def finance_agent(state: AgentState):
    # Auto-detect and parse
    report = parse_pos_report("daily_sales.json")

    # Now use standard kafeAI structure
    revenue = report["sales_summary"]["total_gross"]
    categories = report["sales_by_category"]

    # ... rest of agent logic
```

---

## Vision Agent Tuning

The Finance Agent uses OCR to parse receipt images and extract line items. You may need to tune this for different countries' receipt formats.

### Current OCR Prompt

```python
# In dynamic_pricing_agent.py or similar
VISION_PROMPT = """
You are an expert at extracting structured data from Swedish café receipts.
Analyze the receipt image and extract:

1. Total amount (including VAT)
2. VAT breakdown by rate (6%, 12%, 25%)
3. Line items with quantities and prices
4. Payment method

Output as JSON:
{
    "total": float,
    "vat_breakdown": {"6%": float, "12%": float, "25%": float},
    "items": [{"name": str, "qty": int, "price": float}],
    "payment_method": str
}

Note: Swedish receipts often use "inkl. moms" for VAT-inclusive prices.
"""
```

### Adapting for US Receipts

```python
US_VISION_PROMPT = """
You are an expert at extracting structured data from US restaurant receipts.
Analyze the receipt image and extract:

1. Subtotal (before tax)
2. Tax amount (varies by state, usually 4-10%)
3. Tip amount (if present)
4. Total amount
5. Line items with quantities and prices
6. Payment method

Output as JSON:
{
    "subtotal": float,
    "tax": float,
    "tip": float,
    "total": float,
    "tax_rate": float,  # e.g., 8.25 for 8.25%
    "items": [{"name": str, "qty": int, "price_each": float}],
    "payment_method": str  # "Credit Card", "Cash", etc.
}

Note: US receipts typically show subtotal + tax + tip = total.
"""
```

### Adapting for German Receipts (GDPR-compliant)

```python
DE_VISION_PROMPT = """
You are an expert at extracting structured data from German café receipts (Kassenbon).
Analyze the receipt image and extract:

1. Total amount (Gesamtsumme)
2. VAT (MwSt.) breakdown:
   - 7% (reduced rate for food)
   - 19% (standard rate for beverages)
3. Line items with quantities
4. Payment method (Zahlungsart)
5. Receipt number (Beleg-Nr.) for compliance

Output as JSON:
{
    "gesamtsumme": float,
    "mwst": {"7%": float, "19%": float},
    "items": [{"name": str, "menge": int, "preis": float}],
    "zahlungsart": str,
    "beleg_nr": str
}

Note: German receipts must include Geschäftsnummer for tax compliance.
"""
```

### Configurable Prompt Loading

```python
# config/receipt_formats.py
RECEIPT_PROMPTS = {
    "SE": SWEDISH_PROMPT,  # Default
    "US": US_PROMPT,
    "DE": GERMAN_PROMPT,
    "FR": FRENCH_PROMPT,
    # Add more...
}

def get_vision_prompt(country_code: str = None) -> str:
    """Load appropriate prompt based on configuration."""
    country = country_code or os.getenv("RECEIPT_COUNTRY", "SE")
    return RECEIPT_PROMPTS.get(country, RECEIPT_PROMPTS["SE"])
```

---

## Adding New Agent Nodes

To extend kafeAI with a new specialist agent:

### Step 1: Create the Agent Function

```python
# agents/staffing_agent.py
import os
from datetime import datetime, timedelta
from manageragent import AgentState

def staffing_agent(state: AgentState) -> dict:
    """
    Recommends staffing levels based on forecasted demand.
    """

    # Load historical staffing data (you'd create this)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staff_history_path = os.path.join(base_path, "staffing_history.json")

    # Get forecast context from previous agents
    forecast_context = "\n".join(state["context"])

    # Analyze patterns
    tomorrow = datetime.now() + timedelta(days=1)
    day_of_week = tomorrow.strftime("%A")

    # Simple rule-based (replace with LLM call for sophistication)
    if "high demand" in forecast_context.lower():
        recommendation = "Schedule 3 FOH + 2 BOH staff"
    elif "rain" in forecast_context.lower():
        recommendation = "Schedule 1 FOH + 1 BOH staff (minimum)"
    else:
        recommendation = "Schedule 2 FOH + 1 BOH staff"

    return {
        "context": [f"Staffing: {recommendation} for {day_of_week}"]
    }
```

### Step 2: Register in Manager Agent

```python
# In manageragent.py

from staffing_agent import staffing_agent

# Add to the graph
workflow.add_node("staffing", staffing_agent)

# Define routing logic
def route_after_inventory(state: AgentState):
    if "staffing" in state["issue"].lower() or "@Staffing" in state["issue"]:
        return "staffing"
    return "finance"  # Default path

workflow.add_conditional_edges(
    "inventory",
    route_after_inventory,
    {
        "staffing": "staffing",
        "finance": "finance"
    }
)

workflow.add_edge("staffing", "finance")  # Continue to finance after staffing
```

### Step 3: Add @Mention Routing

```python
# In whatsapp_bot.py or routing logic

AGENT_ROUTES = {
    "@Finance": "finance",
    "@Inventory": "inventory",
    "@Weather": "weather",
    "@Creative": "creative",
    "@Staffing": "staffing",  # New route
}

def route_query(message: str) -> str:
    """Determine which agent should handle the query."""
    for mention, node in AGENT_ROUTES.items():
        if mention in message:
            return node
    return "full"  # Run full pipeline
```

---

## Customizing Menu and Inventory

### Menu.md Format

```markdown
## [Category Name]
[Item Name] ([ingredients]) [Price][Currency]

## Storage
[Item] [Target Quantity] [Unit]
```

Example:
```markdown
## Burgers
Classic Beef Burger (beef+cheese+lettuce+tomato+aioli) $12.00

## Storage
beef 50 lb
cheese 20 lb
```

### Automatic Stock.json Generation

```python
# utils/menu_parser.py
import re
import json

def parse_menu_to_stock(menu_path: str, output_path: str):
    """Parse Menu.md and generate stock.json template."""

    with open(menu_path, 'r') as f:
        content = f.read()

    # Extract storage section
    storage_match = re.search(r'## Storage\n(.+)', content, re.DOTALL)
    if not storage_match:
        raise ValueError("No Storage section found in Menu.md")

    storage_section = storage_match.group(1)

    # Parse each line: "item quantity unit"
    inventory = []
    for line in storage_section.strip().split('\n'):
        if not line.strip():
            continue

        parts = line.strip().split()
        if len(parts) >= 3:
            item = parts[0]
            quantity = float(parts[1])
            unit = ' '.join(parts[2:])

            inventory.append({
                "item": item,
                "quantity": 0,  # Start at zero, update via app
                "unit": unit
            })

    stock_data = {
        "inventory": inventory,
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "source": "Menu.md"
        }
    }

    with open(output_path, 'w') as f:
        json.dump(stock_data, f, indent=4)

    print(f"✓ Generated stock.json with {len(inventory)} items")
```

---

## Environment Configuration

### .env File Template

```bash
# Required API Keys
GOOGLE_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_weatherapi_key_here

# WhatsApp Configuration
WHATSAPP_PHONE_NUMBER=+46701234567

# Optional: Customization
CITY=Sundsvall
COUNTRY=SE
LANGUAGE=sv
RECEIPT_COUNTRY=SE

# Optional: Feature Flags
ENABLE_STAFFING_AGENT=false
ENABLE_AUTO_PRICING=true
ENABLE_POSTER_GENERATION=true

# Optional: Paths
DAILY_REPORTS_PATH=./daily_reports
STOCK_FILE_PATH=./stock.json
MEMORY_FILE_PATH=./memory.json
```

---

## Testing Your Customizations

```python
# tests/test_custom_adapter.py
import unittest
from pos_adapters.square_adapter import SquareAdapter

class TestSquareAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = SquareAdapter()

    def test_parse_sample(self):
        sample_data = {
            "payments": [
                {
                    "total_money": {"amount": 1200},
                    "tax_money": {"amount": 100},
                    "created_at": "2026-03-15T10:00:00Z",
                    "source_type": "CARD"
                }
            ]
        }

        result = self.adapter.parse_report(sample_data)

        self.assertEqual(result["sales_summary"]["total_gross"], 12.00)
        self.assertEqual(result["payment_methods"]["card"], 12.00)

if __name__ == '__main__':
    unittest.main()
```

---

## Contributing Back

If you build a useful extension:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/square-pos-adapter`
3. Add your code with tests
4. Update documentation
5. Submit a Pull Request

We especially welcome:
- New POS system adapters
- Language localization
- Additional agent types
- Improved prompts for different regions
