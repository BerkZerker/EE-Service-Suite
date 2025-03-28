import http.client
import json
import base64

def login():
    conn = http.client.HTTPConnection("localhost", 8000)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = "username=admin@example.com&password=adminpassword"
    conn.request("POST", "/api/auth/login", body, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    
    if response.status == 200:
        return json.loads(data)
    else:
        print(f"Login failed: {response.status} {response.reason}")
        print(data)
        return None

def make_request(path, method="GET", token=None):
    conn = http.client.HTTPConnection("localhost", 8000)
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    conn.request(method, path, headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    print(f"Status: {response.status} {response.reason}")
    if data:
        try:
            json_data = json.loads(data)
            print(json.dumps(json_data, indent=2))
        except json.JSONDecodeError:
            print(data)
    else:
        print("No data returned")
    conn.close()

# Login first
print("Logging in...")
tokens = login()
if tokens and 'access_token' in tokens:
    token = tokens["access_token"]
    print(f"Login successful, token: {token[:10]}...")
    
    # Test endpoints with token
    print("\nTesting /api/tickets/ endpoint with token...")
    make_request("/api/tickets/", token=token)
    
    # Test specific ticket
    print("\nTesting ticket archive field...")
    make_request("/api/tickets/?archived=true", token=token)
else:
    print("Login failed, running tests without token...")
    make_request("/api/tickets/")