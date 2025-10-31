from dotenv import load_dotenv
import os
import msal
import requests

CLIENT_ID = os.getenv("CLIENT_ID")  # From Azure App registration
TENANT_ID = os.getenv("TENTANT_ID")  # Use 'common' for personal Microsoft accounts
SCOPES = ["Tasks.ReadWrite"]

import msal
import requests

CLIENT_ID = "YOUR_CLIENT_ID"
TENANT_ID = "common"  # personal Microsoft account
SCOPES = ["Tasks.ReadWrite"]

# Authenticate
app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}")
accounts = app.get_accounts()
result = None

if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if not result:
    result = app.acquire_token_interactive(SCOPES)

access_token = result["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Get all To Do lists
url = "https://graph.microsoft.com/v1.0/me/todo/lists"
response = requests.get(url, headers=headers)

lists = response.json().get("value", [])
for lst in lists:
    print(f"Name: {lst['displayName']}, ID: {lst['id']}")


class To_Do_Connector():

    def authenticate():
        app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}")

        # Try silent login first
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(SCOPES, account=accounts[0])
        else:
            result = None

        # If no token, do interactive login
        if not result:
            result = app.acquire_token_interactive(SCOPES)

        access_token = result["access_token"]
    

    
