import lxml.etree as ET
from dateutil.parser import parse
import json
from .config import CONFIG
from .database import insert_transaction

def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    transactions = []
    for sms in root.findall('sms'):
        # Example XML structure assumed: <sms><date>2023-01-01</date><phone>+123...</phone><amount>100.0</amount></sms>
        date = sms.find('date').text
        phone = sms.find('phone').text
        amount = float(sms.find('amount').text)
        transactions.append({'date': date, 'phone': phone, 'amount': amount})
    return transactions

def clean_data(transactions):
    cleaned = []
    for t in transactions:
        # Normalize phone (e.g., remove spaces, ensure + prefix)
        phone = t['phone'].replace(' ', '').strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        # Parse date
        date = parse(t['date']).strftime('%Y-%m-%d')
        cleaned.append({'date': date, 'phone': phone, 'amount': t['amount']})
    return cleaned

def categorize_transaction(amount):
    # Simple rule-based categorization
    return 'payment' if amount > 0 else 'withdrawal'

def process_etl():
    # Parse
    transactions = parse_xml(CONFIG['xml_path'])
    # Clean
    cleaned = clean_data(transactions)
    # Categorize and load
    for t in cleaned:
        category = categorize_transaction(t['amount'])
        insert_transaction(CONFIG['db_path'], t['date'], t['phone'], t['amount'], category)
    # Export to JSON for frontend
    with open(CONFIG['json_output'], 'w') as f:
        json.dump(cleaned, f)