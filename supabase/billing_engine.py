import os
import requests
from requests.auth import HTTPBasicAuth
import json

def get_supabase_costs():
    """Fetches real-time billing data from Supabase"""
    token = os.getenv('SUPABASE_ACCESS_TOKEN')
    project_ref = os.getenv('SUPABASE_PROJECT_REF')
    
    # Supabase Management API endpoint for costs
    url = f"https://api.supabase.com/v1/projects/{project_ref}/billing/costs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Returns the total amount billed so far
        return data.get('amount', 0.0)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None

def create_jira_ticket(amount):
    """Logs the overage into the Jira SUP project"""
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    token = os.getenv('JIRA_API_TOKEN')
    project_key = "SUP"

    url = f"https://{domain}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": f"LIVE BILLING ALERT: ${amount} Overage",
            "description": {
                "type": "doc", "version": 1,
                "content": [{
                    "type": "paragraph", 
                    "content": [{"text": f"Automated Scan: Current Supabase cost is ${amount}. Please review usage.", "type": "text"}]
                }]
            },
            "issuetype": {"name": "Task"},
            "priority": {"name": "High"}
        }
    })

    res = requests.post(url, data=payload, headers=headers, auth=auth)
    print(f"Jira Ticket Created. Status: {res.status_code}")

# Execution Logic
cost = get_supabase_costs()
if cost is not None and cost > 0:
    create_jira_ticket(cost)
else:
    print(f"Check Complete: Current cost is ${cost}. No ticket needed.")
