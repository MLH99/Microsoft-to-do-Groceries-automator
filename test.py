# add_todo_task_cached.py
# pip install msal requests

from msal import PublicClientApplication, SerializableTokenCache
import os
import json
import requests

CLIENT_ID = "5941a2e7-b381-4083-8900-bd8946e7a0d8"
TODO_LIST_ID = "AQMkADAwATNiZmYAZC0yNGI3LWE2MTYtMDACLTAwCgAuAAADl1p-P_9au0Ot_FBTGdaB7AEAeWLLN6msK0yEcVEiDa7DHAAECY-UQAAAAA=="
SCOPES = ["Tasks.ReadWrite"]

# Token cache file
CACHE_FILE = "token_cache.bin"

# Initialize token cache
token_cache = SerializableTokenCache()
if os.path.exists(CACHE_FILE):
    token_cache.deserialize(open(CACHE_FILE, "r").read())

app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority="https://login.microsoftonline.com/common",
    token_cache=token_cache
)

# Try to get a token silently
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
else:
    result = None

# If no valid token, use device code flow
if not result:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow: %s" % flow)
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    raise SystemExit("Failed to acquire token: %s" % result)

# Save cache to file
with open(CACHE_FILE, "w") as f:
    f.write(token_cache.serialize())

access_token = result["access_token"]

# Create the task
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

task_data = {"title": "test"}
url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID}/tasks"
response = requests.post(url, headers=headers, json=task_data)

if response.status_code == 201:
    print("Task created successfully!")
    print("Task ID:", response.json().get("id"))
else:
    print("Error creating task:", response.status_code, response.text)
