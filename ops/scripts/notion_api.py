#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse

NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

def create_task(title, status="To Do", deadline=None):
    if not NOTION_TOKEN or not DATABASE_ID:
        print("Error: NOTION_API_KEY or NOTION_DATABASE_ID environment variables are missing.")
        sys.exit(1)

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    properties = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Status": {"status": {"name": status}}
    }
    if deadline:
        properties["Deadline"] = {"date": {"start": deadline}}

    data = json.dumps({
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f"Success: Task '{title}' created in Notion.")
    except Exception as e:
        print(f"Failed to create task: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: notion_api.py <title> [status] [deadline]")
        sys.exit(1)
    
    title = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "To Do"
    deadline = sys.argv[3] if len(sys.argv) > 3 else None
    
    create_task(title, status, deadline)
