#!/usr/bin/env python3
path = "/home/hermes/.hermes/hermes-agent/run_agent.py"

with open(path, "r") as f:
    content = f.read()

# Replace 1: self._emit_status block at line ~7551-7555
old1 = """            self._emit_status(
                f"🔄 Primary model failed — switching to fallback: "
                f"{fb_model} via {fb_provider}"
            )"""

new1 = """            logging.info(
                "Fallback activated silently: %s → %s (%s)",
                old_model, fb_model, fb_provider,
            )"""

content = content.replace(old1, new1)

# Replace 2: self._emit_status for non-retryable error
old2 = "                        self._emit_status(f\"⚠️ Non-retryable error (HTTP {status_code}) — trying fallback...\")"
new2 = "                        logging.info(\"Non-retryable error (HTTP %s) — trying fallback silently\", status_code)"
content = content.replace(old2, new2)

with open(path, "w") as f:
    f.write(content)

print("Done")
