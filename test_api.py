import requests
import json

try:
    url = "http://localhost:8000/query"
    payload = {"query": "How many albums are there?"}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Test failed: {e}")
