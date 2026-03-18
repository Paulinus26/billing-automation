import os
import requests
from requests.auth import HTTPBasicAuth

def discover_jira_ids():
    domain = os.getenv('JIRA_DOMAIN')
    email = os.getenv('JIRA_EMAIL')
    token = os.getenv('JIRA_API_TOKEN')

    # Endpoint to get all projects
    url = f"https://{domain}/rest/api/3/project"
    auth = HTTPBasicAuth(email, token)
    
    response = requests.get(url, auth=auth)
    
    if response.status_code == 200:
        projects = response.json()
        print("--- JIRA PROJECT LIST ---")
        for p in projects:
            print(f"Project Name: {p['name']} | Key: {p['key']} | ID: {p['id']}")
    else:
        print(f"Error fetching projects: {response.status_code}")
        print(response.text)

discover_jira_ids()
