#!/usr/bin/env python3
"""
🍃 OpenClaw Agent Status Sync - With Supabase
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
import urllib.request
import urllib.parse

# ======== Configuration ========
SUPABASE_URL = "https://czolesxhhfiwzubvbmab.supabase.co"
SUPABASE_KEY = "sb_publishable_UB5d3pLNUYjX7eEryltBNg_S_4Tibew"
OPENCLAW_SESSIONS_DIR = Path("/home/node/.openclaw/agents/main/sessions")
OPENCLAW_CRON_DIR = Path("/home/node/.openclaw/cron")

def supabase_request(table, data, method="POST"):
    """Simple Supabase REST API call"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200 or response.status == 201
    except Exception as e:
        print(f"⚠️  Supabase error: {e}")
        return False

def parse_timestamp(ts):
    """Parse various timestamp formats"""
    if not ts:
        return datetime.now(timezone.utc).timestamp() * 1000
    
    if isinstance(ts, (int, float)):
        return ts
    
    if isinstance(ts, str):
        try:
            if 'T' in ts:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                return dt.timestamp() * 1000
            return float(ts) * 1000
        except:
            return datetime.now(timezone.utc).timestamp() * 1000
    
    return datetime.now(timezone.utc).timestamp() * 1000

def read_sessions_data():
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
            "updated_at": datetime.now(timezone.utc).isoformat(),
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
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
    
    return jobs

def sync_to_supabase(agents, jobs):
    print("🔄 Syncing to Supabase...")
    
    success = 0
    for agent in agents:
        if supabase_request("agent_status", agent):
            success += 1
    
    for job in jobs:
        if supabase_request("cron_jobs", job):
            success += 1
    
    print(f"✅ Synced {success} records to Supabase!")
    return success

def main():
    print("🍃 Starting sync to Supabase...")
    
    sessions_data = read_sessions_data()
    cron_data = read_cron_jobs()
    
    agents = process_agent_status(sessions_data)
    jobs = process_cron_jobs(cron_data)
    
    print(f"\n📊 Found {len(agents)} sessions, {len(jobs)} cron jobs")
    
    sync_to_supabase(agents, jobs)
    
    print("\n✅ Sync complete!")

if __name__ == "__main__":
    main()
