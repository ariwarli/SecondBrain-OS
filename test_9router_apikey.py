#!/usr/bin/env python3
import urllib.request, json, sys

api_key = "sk-55adf8a76c1ad5d1-echhwm-8c4b8b70" # 9Router internal API key
url = "http://100.113.246.119:20128/v1/chat/completions"
payload = {"model":"reed","messages":[{"role":"user","content":"ping"}],"max_tokens":5}
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    data = json.loads(e.read().decode())
    print(json.dumps(data, indent=2))
