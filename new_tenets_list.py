import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings()

# Base URL
base_url = "https://35.200.176.139"

# Credentials
username = "hiring-2"
password = "hiring-2"

# Login URL
login_url = f"{base_url}/login"

# Create session
session = requests.Session()

# Login to get sessionid and csrftoken
login_resp = session.post(
    login_url,
    json={"username": username, "password": password},
    verify=False
)

if login_resp.status_code != 200:
    print("❌ Login failed:", login_resp.text)
    exit()

# Extract tokens
session_id = session.cookies.get("sessionid")
csrf_token = session.cookies.get("csrftoken")

if not session_id or not csrf_token:
    print("❌ Missing session or CSRF token.")
    exit()

print("✅ Logged in and tokens obtained.")

# Headers required for fetching tenants
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
    "Referer": f"{base_url}/"
}

# Use session with correct cookies
tenant_url = f"{base_url}/api/tenant"
response = session.get(tenant_url, headers=headers, verify=False)

# Output tenants
if response.status_code == 200:
    tenants = response.json().get("results", [])
    print("\n📋 Tenant List:")
    for tenant in tenants:
        print(" -", tenant["name"])
else:
    print("❌ Failed to fetch tenants:", response.status_code)
    print(response.text)
