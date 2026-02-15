#!/usr/bin/env python3
"""
🍃 OpenClaw Agent Status Sync - Demo Mode
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

OPENCLAW_SESSIONS_DIR = Path("/home/node/.openclaw/agents/main/sessions")
OPENCLAW_CRON_DIR = Path("/home/node/.openclaw/cron")

def parse_timestamp(ts):
    """Parse various timestamp formats"""
    if not ts:
        return datetime.now(timezone.utc).timestamp() * 1000
    
    # If it's already a number
    if isinstance(ts, (int, float)):
        return ts
    
    # If it's a string, try to parse
    if isinstance(ts, str):
        try:
            # Try ISO format
            if 'T' in ts:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                return dt.timestamp() * 1000
            # Try Unix timestamp string
            return float(ts) * 1000
        except:
            return datetime.now(timezone.utc).timestamp() * 1000
    
    return datetime.now(timezone.utc).timestamp() * 1000

def read_sessions_data():
    """Read OpenClaw sessions from .jsonl files"""
    sessions = {}
    
    if not OPENCLAW_SESSIONS_DIR.exists():
        return {}
    
    for f in OPENCLAW_SESSIONS_DIR.glob("*.jsonl"):
        if ".deleted." in f.name or ".lock" in f.name:
            continue
        
        try:
            with open(f, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = json.loads(lines[-1])
                    session_id = f.stem
                    ts = parse_timestamp(last_line.get("timestamp"))
                    sessions[session_id] = {
                        "sessionId": session_id,
                        "updatedAt": ts,
                        "currentTask": last_line.get("content", "")[:100] if "content" in last_line else "Active session",
                    }
        except Exception as e:
            print(f"⚠️  Error reading {f.name}: {e}")
    
    return sessions

def read_cron_jobs():
    """Read OpenClaw cron jobs"""
    jobs_file = OPENCLAW_CRON_DIR / "jobs.json"
    if not jobs_file.exists():
        return {"jobs": []}
    
    with open(jobs_file, 'r') as f:
        return json.load(f)

def process_agent_status(sessions_data):
    agents = []
    current_time = datetime.now(timezone.utc).timestamp() * 1000
    
    for session_id, session_info in sessions_data.items():
        updated_at = session_info.get("updatedAt", 0)
        time_diff = current_time - updated_at
        
        if time_diff < 5 * 60 * 1000:
            status = "working"
        elif time_diff < 30 * 60 * 1000:
            status = "idle"
        else:
            status = "completed"
        
        task_name = session_info.get("currentTask", "Active session")
        
        agents.append({
            "agent_name": session_id[:50],
            "status": status,
            "task_name": task_name,
        })
    
    return agents

def process_cron_jobs(jobs_data):
    jobs = []
    current_time = datetime.now(timezone.utc).timestamp() * 1000
    
    for job in jobs_data.get("jobs", []):
        state = job.get("state", {})
        schedule = job.get("schedule", {})
        
        if not job.get("enabled", True):
            status = "stopped"
        elif state.get("lastStatus") == "ok":
            next_run = state.get("nextRunAtMs", 0)
            status = "pending" if next_run > current_time else "running"
        else:
            status = "failed"
        
        jobs.append({
            "job_id": job.get("id", ""),
            "name": job.get("name", ""),
            "schedule": schedule.get("expr", ""),
            "status": status,
            "last_status": state.get("lastStatus", ""),
        })
    
    return jobs

def main():
    print("🍃 Reading OpenClaw data...")
    
    sessions_data = read_sessions_data()
    cron_data = read_cron_jobs()
    
    agents = process_agent_status(sessions_data)
    jobs = process_cron_jobs(cron_data)
    
    print("\n" + "="*50)
    print("🍃 Anime Office Dashboard - Status Preview")
    print("="*50)
    
    print(f"\n👥 Active Sessions: {len(agents)}")
    if agents:
        for agent in agents:
            emoji = "🟢" if agent["status"] == "working" else "🟡" if agent["status"] == "idle" else "🔴"
            print(f"  {emoji} {agent['agent_name'][:30]}")
            print(f"     Status: {agent['status']} | Task: {agent['task_name'][:40]}")
    else:
        print("  (No active sessions)")
    
    print(f"\n⚙️ Cron Jobs: {len(jobs)}")
    for job in jobs:
        emoji = "✅" if job.get("last_status") == "ok" else "❌" if job.get("last_status") == "error" else "⏳"
        print(f"  {emoji} {job['name']}")
        print(f"     Schedule: {job['schedule']} | Last: {job.get('last_status', 'never')}")
    
    print("\n" + "="*50)
    print("✅ Data reading works! Ready to sync to Supabase.")

if __name__ == "__main__":
    main()
