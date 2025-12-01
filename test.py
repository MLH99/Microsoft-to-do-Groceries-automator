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

#task data should be a aegument variable for this function using the same style 
# and type as below
task_data = {"title": "bajs"}
url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID}/tasks"
response = requests.post(url, headers=headers, json=task_data)

if response.status_code == 201:
    print("Task created successfully!")
    print("Task ID:", response.json().get("id"))
else:
    print("Error creating task:", response.status_code, response.text)
    class TodoTaskManager:
        def __init__(self, client_id, todo_list_id, scopes):
            self.client_id = client_id
            self.todo_list_id = todo_list_id
            self.scopes = scopes
            self.token_cache = SerializableTokenCache()
            self.cache_file = "token_cache.bin"
            self.access_token = self.authenticate()

        def authenticate(self):
            if os.path.exists(self.cache_file):<<<<<<< SEARCH
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
=======
class To_Do_Connector:
    """
    Connector class for interacting with Microsoft To Do list API.

    This class uses environment variables for configuration and authentication.
    """

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.tenant_id = os.getenv("TENANT_ID")
        self.scopes = ["Tasks.ReadWrite"]

    def authenticate(self):
        app = msal.PublicClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}"
        )

        # Try silent login first
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
        else:
            result = None

        # If no token, do interactive login
        if not result:
            result = app.acquire_token_interactive(self.scopes)

        access_token = result["access_token"]
        return access_token
>>>>>>> REPLACE

                self.token_cache.deserialize(open(self.cache_file, "r").read())

            app = PublicClientApplication(
                client_id=self.client_id,
                authority="https://login.microsoftonline.com/common",
                token_cache=self.token_cache
            )

            accounts = app.get_accounts()
            if accounts:
                result = app.acquire_token_silent(self.scopes, account=accounts[0])
            else:
                result = None

            if not result:
                flow = app.initiate_device_flow(scopes=self.scopes)
                if "user_code" not in flow:
                    raise ValueError("Failed to create device flow: %s" % flow)
                print(flow["message"])
                result = app.acquire_token_by_device_flow(flow)

            if "access_token" not in result:
                raise SystemExit("Failed to acquire token: %s" % result)

            with open(self.cache_file, "w") as f:
                f.write(self.token_cache.serialize())

            return result["access_token"]

        def add_task(self, task_data):
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{self.todo_list_id}/tasks"
            response = requests.post(url, headers=headers, json=task_data)

            if response.status_code == 201:
                print("Task created successfully!")
                print("Task ID:", response.json().get("id"))
            else:
                print("Error creating task:", response.status_code, response.text)

    # Example usage:
    # todo_manager = TodoTaskManager(CLIENT_ID, TODO_LIST_ID, SCOPES)
    # todo_manager.add_task({"title": "New Task"})