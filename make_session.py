"""Convert Antigravity transcript_full.jsonl into an OpenAI-format handed-over session JSON."""
import json, os

TRANSCRIPT = r"C:\Users\mirza\.gemini\antigravity\brain\c7bc4fd4-8b19-47d3-ad6d-9d5b794b917c\.system_generated\logs\transcript_full.jsonl"
OUT = r"d:\project\news-image-18-entry\session.json"

messages = []

with open(TRANSCRIPT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        step = json.loads(line)
        stype = step.get("type", "")
        content = step.get("content", "") or ""

        if stype == "USER_INPUT":
            messages.append({"role": "user", "content": content or "(system message)"})
        elif stype == "PLANNER_RESPONSE":
            # Combine content, thinking and tool calls into one content string
            parts = []
            thinking = step.get("thinking", "")
            if thinking:
                parts.append(f"[Thinking]: {thinking[:500]}")
            if content:
                parts.append(content)
            tool_calls = step.get("tool_calls", [])
            if tool_calls:
                for tc in tool_calls:
                    name = tc.get("name", "")
                    args = tc.get("arguments", {})
                    result = tc.get("result", "")
                    parts.append(f"[Tool: {name}] args={json.dumps(args)[:300]}")
                    if result:
                        parts.append(f"[Result]: {str(result)[:500]}")
            messages.append({"role": "assistant", "content": "\n".join(parts) if parts else "(no content)"})

session = {
    "harness": "antigravity",
    "model": "gemini-2.5-pro",
    "handed_over": "Antigravity IDE swarm worker; sessions stored in app brain dir which bundle cannot match to external repo",
    "messages": messages
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(session, f, indent=None, ensure_ascii=False)

print(f"Wrote {len(messages)} messages to {OUT}")
print(f"File size: {os.path.getsize(OUT) / 1024:.0f} KB")
