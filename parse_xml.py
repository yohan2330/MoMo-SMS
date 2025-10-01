# dsa/parse_sms.py
import xml.etree.ElementTree as ET
import json

def parse_sms_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall('sms'):
        transaction = {
            'id': sms.get('id'),
            'type': sms.find('type').text,
            'amount': float(sms.find('amount').text),
            'sender': sms.find('sender').text,
            'receiver': sms.find('receiver').text,
            'timestamp': sms.find('timestamp').text
        }
        transactions.append(transaction)
    
    return transactions

if __name__ == "__main__":
    transactions = parse_sms_xml('modified_sms_v2.xml')
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)
