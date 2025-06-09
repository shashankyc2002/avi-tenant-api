import requests
import urllib3

# Disable SSL warning for self-signed certificate
urllib3.disable_warnings()

# Base URL
base_url = "https://35.200.176.139"

# Credentials
login_url = f"{base_url}/login"
username = "hiring-2"
password = "hiring-2"

# Create a session
session = requests.Session()

# Login
login_response = session.post(
    login_url,
    json={"username": username, "password": password},
    verify=False
)

if login_response.status_code != 200:
    print("❌ Login failed:", login_response.text)
    exit()

print("✅ Logged in successfully")

# Extract session ID and CSRF token from cookies
session_id = session.cookies.get('sessionid')
csrf_token = session.cookies.get('csrftoken') or login_response.headers.get('X-CSRFToken')

if not session_id or not csrf_token:
    print("❌ Required tokens not found.")
    exit()

print(f"✅ Session ID obtained: {session_id}")
print(f"✅ CSRF Token obtained: {csrf_token}")

# Headers with CSRF and Referer
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
    "Referer": f"{base_url}/",
}

# Create a new tenant
tenant_payload = {
    "name": "shashank__tenant"
}

tenant_url = f"{base_url}/api/tenant"
tenant_response = session.post(tenant_url, json=tenant_payload, headers=headers, verify=False)

# Output result
if tenant_response.status_code == 201:
    print("✅ Tenant created successfully")
else:
    print("❌ Failed to create tenant")
    print("Status Code:", tenant_response.status_code)
    print("Response:", tenant_response.text)

# Final display of tokens
print("\n🔐 Session ID:", session_id)
print("🔐 CSRF Token:", csrf_token)
