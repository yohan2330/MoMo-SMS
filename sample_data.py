"""
Create Sample Mobile Money SMS XML Data
Generates modified_sms_v2.xml with realistic transaction records
"""

import random
from datetime import datetime, timedelta

def generate_sample_xml(num_records=50, filename='modified_sms_v2.xml'):
    """Generate sample XML file with mobile money transactions"""
    
    # Sample data
    transaction_types = ['deposit', 'withdrawal', 'transfer', 'payment']
    senders = [
        'John Doe', 'Jane Smith', 'Alice Brown', 'Bob Wilson',
        'Emma Davis', 'Michael Johnson', 'Sarah Williams', 'David Miller',
        'Olivia Martinez', 'James Anderson', 'Sophia Taylor', 'William Thomas',
        'Isabella Garcia', 'Robert Moore', 'Mia Jackson', 'Charles White'
    ]
    
    receivers_by_type = {
        'deposit': ['MTN_MOMO', 'AIRTEL_MONEY', 'TIGO_CASH', 'Mobile_Wallet'],
        'withdrawal': ['ATM_KIGALI', 'ATM_REMERA', 'ATM_NYARUTARAMA', 'AGENT_001', 'AGENT_002'],
        'transfer': senders,  # Person-to-person
        'payment': ['ShopRite', 'Nakumatt', 'Simba_Supermarket', 'UTC_Mall', 'Restaurant_Le_Must']
    }
    
    # Generate XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<sms_records>\n'
    
    base_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        # Random transaction details
        trans_type = random.choice(transaction_types)
        sender = random.choice(senders)
        receiver = random.choice(receivers_by_type[trans_type])
        
        # Ensure sender != receiver for transfers
        if trans_type == 'transfer':
            while receiver == sender:
                receiver = random.choice(receivers_by_type[trans_type])
        
        amount = random.randint(5, 500) * 1000  # 5,000 to 500,000 RWF
        
        # Random timestamp
        days_offset = random.randint(0, 180)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        timestamp = base_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
        timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Generate message based on type
        messages = {
            'deposit': f'You have deposited {amount:,} RWF to your mobile money account. New balance: {amount + random.randint(10000, 100000):,} RWF. Transaction ID: TXN{random.randint(100000, 999999)}',
            'withdrawal': f'Withdrawal of {amount:,} RWF from {receiver} successful. Remaining balance: {random.randint(10000, 200000):,} RWF. Ref: WD{random.randint(100000, 999999)}',
            'transfer': f'Transfer of {amount:,} RWF to {receiver} successful. Fee: {int(amount * 0.01):,} RWF. Ref: TRF{random.randint(100000, 999999)}',
            'payment': f'Payment of {amount:,} RWF to {receiver} successful. Thank you for your purchase. Ref: PAY{random.randint(100000, 999999)}'
        }
        
        message = messages[trans_type]
        
        # Add XML record
        xml_content += f'    <sms type="{trans_type}" amount="{amount}" sender="{sender}" receiver="{receiver}" timestamp="{timestamp_str}">\n'
        xml_content += f'        {message}\n'
        xml_content += '    </sms>\n'
    
    xml_content += '</sms_records>'
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Successfully created {filename}")
    print(f"📊 Generated {num_records} transaction records")
    print(f"\n📝 Sample record:")
    print("="*70)
    lines = xml_content.split('\n')
    for line in lines[2:7]:  # Show first record
        print(line)
    print("="*70)
    
    return filename

def main():
    """Main execution"""
    print("="*70)
    print("🔧 MOBILE MONEY SMS DATA GENERATOR")
    print("="*70)
    print()
    
    # Get number of records from user
    try:
        num_records = input("Enter number of records to generate (default: 50): ").strip()
        num_records = int(num_records) if num_records else 50
        
        if num_records < 1:
            print("❌ Number must be at least 1. Using default: 50")
            num_records = 50
        elif num_records > 10000:
            print("⚠️  Large dataset. This may take a moment...")
    except ValueError:
        print("❌ Invalid input. Using default: 50")
        num_records = 50
    
    print()
    generate_sample_xml(num_records)
    
    print()
    print("🎉 Done! You can now run the API server:")
    print("   python api_server.py")
    print()

if __name__ == '__main__':
    main()