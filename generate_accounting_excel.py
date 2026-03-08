
import os
import json
import pandas as pd
from datetime import datetime

base_dir = r"d:\2026\kafeAI v2\daily_reports"
output_file = r"d:\2026\kafeAI v2\January_2026_Accounting_Report.xlsx"

# January files
files = sorted([f for f in os.listdir(base_dir) if f.startswith("2026_01_") and f.endswith(".json")])

all_data = []

# Accounting Totals
totals = {
    "3001_Net": 0, # Food/Coffee 12%
    "3005_Net": 0, # Alcohol 25%
    "2611_VAT": 0, # VAT 25%
    "2621_VAT": 0, # VAT 12%
    "1580_Card": 0,
    "1580_Swish": 0,
    "1910_Cash": 0
}

for filename in files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    date = data['report_info']['period_end'].split(' ')[0]
    sales = data['sales_summary']
    vat_list = sales.get('vat_details', [])
    payments = data.get('payment_methods', {})
    
    row = {
        "Date": date,
        "Total Gross": sales.get('total_gross', 0),
        "Total Net": sales.get('total_net', 0),
        "Total VAT": sales.get('total_vat', 0),
        "Card": payments.get('card', 0),
        "Swish": payments.get('swish', 0),
        "Cash": payments.get('cash', 0)
    }
    
    # Process VAT details for accounting
    for v in vat_list:
        rate = v.get('rate', '').replace('%', '')
        if rate == "25":
            totals["3005_Net"] += v.get('net_amount', 0)
            totals["2611_VAT"] += v.get('vat_amount', 0)
        elif rate == "12":
            totals["3001_Net"] += v.get('net_amount', 0)
            totals["2621_VAT"] += v.get('vat_amount', 0)
            
    totals["1580_Card"] += payments.get('card', 0)
    totals["1580_Swish"] += payments.get('swish', 0)
    totals["1910_Cash"] += payments.get('cash', 0)
    
    # Process categories for the summary sheet
    cat_data = {c['category']: c['amount'] for c in data.get('sales_by_category', [])}
    row.update(cat_data)
    
    all_data.append(row)

# Create Daily Summary DataFrame
df_daily = pd.DataFrame(all_data)

# Create Accounting Entry DataFrame
accounting_entries = [
    {"Account": "1580", "Description": "Fordringar Kontokort (应收卡款)", "Debit": totals["1580_Card"], "Credit": 0},
    {"Account": "1580", "Description": "Fordringar Swish (应收Swish)", "Debit": totals["1580_Swish"], "Credit": 0},
    {"Account": "1910", "Description": "Kassa (现金账户)", "Debit": totals["1910_Cash"], "Credit": 0},
    {"Account": "3001", "Description": "Försäljning mat/kaffe 12% (食品销售-净额)", "Debit": 0, "Credit": totals["3001_Net"]},
    {"Account": "3005", "Description": "Försäljning alkohol 25% (酒精类销售-净额)", "Debit": 0, "Credit": totals["3005_Net"]},
    {"Account": "2611", "Description": "Utgående moms 25% (销项增值税-25%)", "Debit": 0, "Credit": totals["2611_VAT"]},
    {"Account": "2621", "Description": "Utgående moms 12% (销项增值税-12%)", "Debit": 0, "Credit": totals["2621_VAT"]},
]

df_accounting = pd.DataFrame(accounting_entries)

# Add Total Row
total_debit = df_accounting['Debit'].sum()
total_credit = df_accounting['Credit'].sum()
df_accounting.loc[len(df_accounting)] = ["", "TOTAL SUMMARY", total_debit, total_credit]

# Save to Excel
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_daily.to_excel(writer, sheet_name='Daily_Sales_Summary', index=False)
    df_accounting.to_excel(writer, sheet_name='Accounting_Entries', index=False)

print(f"Report generated successfully: {output_file}")
