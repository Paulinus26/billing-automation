import os
import requests
from requests.auth import HTTPBasicAuth
import json

def create_jira_ticket(amount):
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    token = os.getenv('JIRA_API_TOKEN')
    project_key = os.getenv('JIRA_PROJECT_KEY')

    url = f"https://{domain}/rest/api/3/issue"
    
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": f"Billing Alert: ${amount} Overage Detected",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"text": f"Automated billing engine detected a total due of ${amount}.", "type": "text"}
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Task"}
        }
    })

    response = requests.post(url, data=payload, headers=headers, auth=auth)
    
    if response.status_code == 201:
        print(f"SUCCESS: Jira Ticket created in project {project_key}!")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")

# Trigger the alert
create_jira_ticket(25.0)
