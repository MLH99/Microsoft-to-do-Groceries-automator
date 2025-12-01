from dotenv import load_dotenv
import os
import msal
import requests

CLIENT_ID = os.getenv("CLIENT_ID")  # From Azure App registration
TENANT_ID = os.getenv("TENANT_ID")  # Use 'common' for personal Microsoft accounts
TO_DO_LIST_ID = os.getenv("TO_DO_LIST_ID")  # Your To Do list ID
SCOPES = ["Tasks.ReadWrite"]



class To_Do_Connector():

    def __init__(self):
        # Initialize the token cache
        self.token_cache = msal.SerializableTokenCache()
        cache_file = os.path.join(os.path.dirname(__file__), '..', 'token_cache.bin')

        # Load cache if it exists
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                self.token_cache.deserialize(f.read())

        self.cache_file = cache_file  # Save path to write back later
    def authenticate(self):
        app = msal.PublicClientApplication(
            CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{TENANT_ID}",
            token_cache=self.token_cache
        )

        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(SCOPES, account=accounts[0])
        else:
            result = None

        if not result:
            flow = app.initiate_device_flow(scopes=SCOPES)
            if "user_code" not in flow:
                raise ValueError(f"Failed to create device flow: {flow}")
            print(flow["message"])
            result = app.acquire_token_by_device_flow(flow)

        if "access_token" not in result:
            raise SystemExit(f"Failed to acquire token: {result}")

        CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'token_cache.bin')
        with open(CACHE_FILE, "w") as f:
            f.write(self.token_cache.serialize())

        return result["access_token"]

    def add_task(self, title, item):
            access_token = self.authenticate()
            endpoint = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TO_DO_LIST_ID}/tasks"

            task_data = {
                "title": title,
                "body": {
                    "content": item
                }
            }

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(endpoint, headers=headers, json=task_data)

            if response.status_code == 201:
                print("Task added successfully.")
                print("Task ID:", response.json().get("id"))
            else:
                print(f"Error adding task: {response.status_code} - {response.text}")