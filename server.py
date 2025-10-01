"""
Mobile Money SMS REST API Server
Implements CRUD operations with Basic Authentication
"""

import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from datetime import datetime
import time

# Configuration
PORT = 8000
VALID_CREDENTIALS = {
    "admin": "password123",
    "user1": "securepass"
}

class TransactionStore:
    """In-memory storage for transactions with dictionary lookup"""
    
    def __init__(self):
        self.transactions = {}
        self.next_id = 1
    
    def load_from_xml(self, xml_file):
        """Parse XML file and load transactions"""
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for sms in root.findall('sms'):
            transaction = {
                'id': self.next_id,
                'type': sms.get('type', 'unknown'),
                'amount': float(sms.get('amount', 0)),
                'sender': sms.get('sender', ''),
                'receiver': sms.get('receiver', ''),
                'timestamp': sms.get('timestamp', ''),
                'message': sms.text.strip() if sms.text else ''
            }
            self.transactions[self.next_id] = transaction
            self.next_id += 1
    
    def get_all(self):
        """Return all transactions as list"""
        return list(self.transactions.values())
    
    def get_by_id(self, trans_id):
        """Dictionary lookup - O(1)"""
        return self.transactions.get(trans_id)
    
    def linear_search(self, trans_id):
        """Linear search - O(n) - for comparison"""
        for transaction in self.transactions.values():
            if transaction['id'] == trans_id:
                return transaction
        return None
    
    def add(self, transaction):
        """Add new transaction"""
        transaction['id'] = self.next_id
        transaction['timestamp'] = datetime.now().isoformat()
        self.transactions[self.next_id] = transaction
        self.next_id += 1
        return transaction
    
    def update(self, trans_id, updates):
        """Update existing transaction"""
        if trans_id in self.transactions:
            self.transactions[trans_id].update(updates)
            self.transactions[trans_id]['id'] = trans_id  # Keep ID unchanged
            return self.transactions[trans_id]
        return None
    
    def delete(self, trans_id):
        """Delete transaction"""
        if trans_id in self.transactions:
            return self.transactions.pop(trans_id)
        return None

# Initialize transaction store
store = TransactionStore()

class APIHandler(BaseHTTPRequestHandler):
    
    def _authenticate(self):
        """Check Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            return False
        
        try:
            auth_type, credentials = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False
            
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            return VALID_CREDENTIALS.get(username) == password
        except:
            return False
    
    def _send_response(self, status_code, data=None, error=None):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {}
        if data is not None:
            response['data'] = data
        if error:
            response['error'] = error
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def _send_unauthorized(self):
        """Send 401 Unauthorized"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'error': 'Unauthorized - Valid credentials required'
        }).encode())
    
    def do_GET(self):
        """Handle GET requests"""
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # GET /transactions - List all
        if path == '/transactions':
            transactions = store.get_all()
            self._send_response(200, data=transactions)
        
        # GET /transactions/{id} - Get one
        elif path.startswith('/transactions/'):
            try:
                trans_id = int(path.split('/')[-1])
                transaction = store.get_by_id(trans_id)
                
                if transaction:
                    self._send_response(200, data=transaction)
                else:
                    self._send_response(404, error=f'Transaction {trans_id} not found')
            except ValueError:
                self._send_response(400, error='Invalid transaction ID')
        
        else:
            self._send_response(404, error='Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests"""
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        if self.path == '/transactions':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                transaction_data = json.loads(post_data.decode())
                
                # Validate required fields
                required = ['type', 'amount', 'sender', 'receiver']
                if not all(field in transaction_data for field in required):
                    self._send_response(400, error=f'Missing required fields: {required}')
                    return
                
                new_transaction = store.add(transaction_data)
                self._send_response(201, data=new_transaction)
            
            except json.JSONDecodeError:
                self._send_response(400, error='Invalid JSON')
            except Exception as e:
                self._send_response(500, error=str(e))
        else:
            self._send_response(404, error='Endpoint not found')
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        if self.path.startswith('/transactions/'):
            try:
                trans_id = int(self.path.split('/')[-1])
                
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                update_data = json.loads(put_data.decode())
                
                updated = store.update(trans_id, update_data)
                
                if updated:
                    self._send_response(200, data=updated)
                else:
                    self._send_response(404, error=f'Transaction {trans_id} not found')
            
            except ValueError:
                self._send_response(400, error='Invalid transaction ID')
            except json.JSONDecodeError:
                self._send_response(400, error='Invalid JSON')
            except Exception as e:
                self._send_response(500, error=str(e))
        else:
            self._send_response(404, error='Endpoint not found')
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        if self.path.startswith('/transactions/'):
            try:
                trans_id = int(self.path.split('/')[-1])
                deleted = store.delete(trans_id)
                
                if deleted:
                    self._send_response(200, data={'message': f'Transaction {trans_id} deleted', 'deleted': deleted})
                else:
                    self._send_response(404, error=f'Transaction {trans_id} not found')
            
            except ValueError:
                self._send_response(400, error='Invalid transaction ID')
        else:
            self._send_response(404, error='Endpoint not found')
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(xml_file='modified_sms_v2.xml'):
    """Start the API server"""
    try:
        # Load data from XML
        print(f"Loading data from {xml_file}...")
        store.load_from_xml(xml_file)
        print(f"Loaded {len(store.get_all())} transactions")
        
        # Start server
        server = HTTPServer(('localhost', PORT), APIHandler)
        print(f"\n{'='*60}")
        print(f"🚀 Mobile Money API Server running on http://localhost:{PORT}")
        print(f"{'='*60}")
        print(f"\nAuthentication credentials:")
        print(f"  Username: admin | Password: password123")
        print(f"  Username: user1 | Password: securepass")
        print(f"\nAvailable endpoints:")
        print(f"  GET    /transactions")
        print(f"  GET    /transactions/{{id}}")
        print(f"  POST   /transactions")
        print(f"  PUT    /transactions/{{id}}")
        print(f"  DELETE /transactions/{{id}}")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        server.serve_forever()
    
    except FileNotFoundError:
        print(f"❌ Error: {xml_file} not found")
        print("Please ensure the XML file is in the same directory")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        server.socket.close()

if __name__ == '__main__':
    run_server()



