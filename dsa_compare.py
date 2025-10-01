# dsa/search_dsa.py
import json
import time

with open('transactions.json') as f:
    transactions = json.load(f)
transactions_dict = {t['id']: t for t in transactions}

# Linear Search
def linear_search(tid):
    for t in transactions:
        if t['id'] == tid:
            return t
    return None

# Dictionary Lookup
def dict_lookup(tid):
    return transactions_dict.get(tid)

# Timing comparison
tid = transactions[0]['id']  # Example
start = time.time(); linear_search(tid); print("Linear:", time.time()-start)
start = time.time(); dict_lookup(tid); print("Dict:", time.time()-start)
