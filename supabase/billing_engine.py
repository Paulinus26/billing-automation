import os
import requests

def calculate_bill(usage, limit):
    price_per_gb = 0.50
    if usage > limit:
        overage = usage - limit
        return round(overage * price_per_gb, 2)
    return 0.0

def send_to_trello(amount):
    # Using the names we set in GitHub Secrets
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
            'desc': "Automated alert from Paulinus's Billing Engine."
        }
        response = requests.post(url, params=query)
        if response.status_code == 200:
            print(f"SUCCESS: Card for ${amount} created!")
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
    else:
        print("No overage detected.")

bill_total = calculate_bill(150, 100)
send_to_trello(bill_total)
