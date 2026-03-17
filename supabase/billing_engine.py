import os
import requests

def send_to_trello():
    # Pulling from your GitHub Secrets
    key = os.getenv('TRELLO_KEY')
    token = os.getenv('TRELLO_TOKEN')
    list_id = os.getenv('TRELLO_LIST_ID')

    url = "https://api.trello.com/1/cards"
    query = {
        'key': key,
        'token': token,
        'idList': list_id,
        'name': "Automation Success: $25.0 Due",
        'desc': "Sent from GitHub Actions."
    }
    
    response = requests.post(url, params=query)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

send_to_trello()
