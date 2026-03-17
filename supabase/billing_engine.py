import os
import requests

# 1. Your Calculation Logic (The "Accountant")
def calculate_bill(usage, limit):
    price_per_gb = 0.50
    if usage > limit:
        overage = usage - limit
        return round(overage * price_per_gb, 2)
    return 0.0

# 2. The Trello Logic (The "Messenger")
def send_to_trello(amount):
    key = os.getenv('TRELLO_KEY')
    token = os.getenv('TRELLO_TOKEN')
    list_id = os.getenv('TRELLO_LIST_ID')

    if amount > 0:
        url = "https://api.trello.com/1/cards"
        query = {
            'key': key,
            'token': token,
            'idList': list_id,
            'name': f"Billing Alert: ${amount} Due",
            'desc': "Overage detected and calculated by Paulinus's Billing Engine."
        }
        response = requests.post(url, params=query)
        if response.status_code == 200:
            print(f"Success! Card for ${amount} created on Trello.")
        else:
            print(f"Error: {response.text}")
    else:
        print("No overage detected. No Trello card needed.")

# 3. Running the Engine
bill_total = calculate_bill(150, 100) # Result is 25.0
send_to_trello(bill_total)