import os
import requests
from requests.auth import HTTPBasicAuth
import json

def create_billing_ticket(amount):
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    token = os.getenv('JIRA_API_TOKEN')
    project_key = os.getenv('JIRA_PROJECT_KEY') # This is now 'SUP'

    url = f"https://{domain}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": f"BILLING ALERT: ${amount} Overage",
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [{"text": f"Overage of ${amount} detected in Supabase.", "type": "text"}]}]
            },
            "issuetype": {"name": "Task"}
        }
    })

    response = requests.post(url, data=payload, headers=headers, auth=auth)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

create_billing_ticket(25.0)
