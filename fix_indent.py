#!/usr/bin/env python3
path = "/home/hermes/.hermes/hermes-agent/run_agent.py"
with open(path, "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "Fallback activated silently" in lines[i] and i+3 < len(lines):
        # Check if next 3 lines are orphaned f-strings
        if 'f"⚠️' in lines[i+1]:
            j = i+1
            while j < len(lines) and ')' not in lines[j]:
                j += 1
            if j < len(lines) and lines[j].strip() == ")":
                del lines[i+1:j+1]
            break

with open(path, "w") as f:
    f.writelines(lines)
print("Fixed")
