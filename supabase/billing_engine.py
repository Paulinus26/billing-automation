import os
import requests
from requests.auth import HTTPBasicAuth
import json

def trigger_supabase_alert(amount):
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    token = os.getenv('JIRA_API_TOKEN')
    project_key = "SUP" # We are sticking with the working project

    url = f"https://{domain}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": f"CRITICAL: Supabase Billing Overage - ${amount}",
            "description": {
                "type": "doc", "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"text": f"Cloud Ops Alert: Current usage has exceeded the free tier. Total overage: ${amount}.", "type": "text"}]
                    }
                ]
            },
            "issuetype": {"name": "Task"},
            "labels": ["supabase-billing", "cloud-ops"],
            "priority": {"name": "High"}
        }
    })

    response = requests.post(url, data=payload, headers=headers, auth=auth)
    print(f"Status: {response.status_code} - Ticket Created: SUP-1")

trigger_supabase_alert(25.0)
