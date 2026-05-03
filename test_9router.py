#!/usr/bin/env python3
import subprocess, json, sys

api_key = "sk-07e0052b117a15d3-po7d8n-baeccd5e"
url = "http://100.113.246.119:20128/v1/chat/completions"
payload = {"model":"reed","messages":[{"role":"user","content":"ping"}],"max_tokens":5}
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

import urllib.request
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    data = json.loads(e.read().decode())
    print(json.dumps(data, indent=2))
