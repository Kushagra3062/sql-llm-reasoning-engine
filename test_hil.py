import requests
import json
import time

url = "http://localhost:8000/query"

def print_step(msg):
    print(f"\n{'='*20}\n{msg}\n{'='*20}")

try:
    print_step("Step 1: Sending ambiguous query ('Show me top artists')")
    payload = {"query": "Show me top artists"} 
    response = requests.post(url, json=payload)
    
    data = response.json()
    print("Response Type:", data.get('type'))
    print("Content:", data.get('content'))
    
    if data.get('type') == 'interruption':
        print("Correctly paused for ambiguity.")
        print("Options:", json.dumps(data.get('mcq_options'), indent=2))
        
    
        print_step("Step 2: Resuming with choice 1")
        resume_payload = {
            "query": "Show me top artists",
            "human_choice": 1
        }
        response_2 = requests.post(url, json=resume_payload)
        data_2 = response_2.json()
        
        print("Final Response Type:", data_2.get('type', 'normal'))
        print("Final Content:", data_2.get('content'))
        
        if data_2.get('sql'):
            print("SQL Generated:", data_2['sql'])
        else:
            print("No SQL in final response (might be expected for this test query)")
            
    else:
        print("Did not pause! HIL failed.")
        print(json.dumps(data, indent=2))

except Exception as e:
    print(f"Test failed: {e}")
