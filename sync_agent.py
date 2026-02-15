#!/usr/bin/env python3
"""
🍃 OpenClaw Agent Status Sync Daemon
Syncs OpenClaw session and cron data to Supabase every 30 seconds
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ======== Configuration ========
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
OPENCLAW_SESSIONS_DIR = Path("/home/node/.openclaw/agents/main/sessions")
OPENCLAW_CRON_DIR = Path("/home/node/.openclaw/cron")
SYNC_INTERVAL = 30  # seconds

# ======== Supabase Client ========
def get_supabase_client() -> Client:
    """Initialize Supabase client"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️  Supabase credentials not configured. Running in demo mode.")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# ======== Read OpenClaw Data ========
def read_sessions_data():
    """Read OpenClaw sessions from sessions.json"""
    sessions_file = OPENCLAW_SESSIONS_DIR / "sessions.json"
    if not sessions_file.exists():
        return {}
    
    with open(sessions_file, 'r') as f:
        return json.load(f)

def read_cron_jobs():
    """Read OpenClaw cron jobs"""
    jobs_file = OPENCLAW_CRON_DIR / "jobs.json"
    if not jobs_file.exists():
        return {"jobs": []}
    
    with open(jobs_file, 'r') as f:
        return json.load(f)

def get_active_session_files():
    """Get list of active (non-deleted) session files"""
    if not OPENCLAW_SESSIONS_DIR.exists():
        return []
    
    sessions = []
    for f in OPENCLAW_SESSIONS_DIR.glob("*.jsonl"):
        if ".deleted." not in f.name and ".reset." not in f.name and ".lock" not in f.name:
            sessions.append(f)
    return sessions

# ======== Process Data ========
def process_agent_status(sessions_data):
    """Process session data to extract agent statuses"""
    agents = []
    
    for agent_id, session_info in sessions_data.items():
        # Determine status based on session activity
        updated_at = session_info.get("updatedAt", 0)
        current_time = datetime.now().timestamp() * 1000
        time_diff = current_time - updated_at
        
        # Active within last 5 minutes = working
        if time_diff < 5 * 60 * 1000:
            status = "working"
        elif time_diff < 30 * 60 * 1000:
            status = "idle"
        else:
            status = "completed"
        
        # Extract task info from session
        task_name = session_info.get("currentTask", "Active session")
        thinking_level = session_info.get("thinkingLevel", "normal")
        
        agents.append({
            "agent_name": agent_id,
            "status": status,
            "task_name": task_name,
            "started_at": datetime.fromtimestamp(updated_at / 1000).isoformat(),
            "updated_at": datetime.now().isoformat(),
            "details": {
                "session_id": session_info.get("sessionId", ""),
                "thinking_level": thinking_level,
                "system_sent": session_info.get("systemSent", False)
            }
        })
    
    return agents

def process_cron_jobs(jobs_data):
    """Process cron jobs data"""
    jobs = []
    
    for job in jobs_data.get("jobs", []):
        state = job.get("state", {})
        schedule = job.get("schedule", {})
        
        # Determine status
        if not job.get("enabled", True):
            status = "stopped"
        elif state.get("lastStatus") == "ok":
            # Check if next run is soon
            next_run = state.get("nextRunAtMs", 0)
            current_time = datetime.now().timestamp() * 1000
            if next_run > current_time:
                status = "pending"
            else:
                status = "running"
        else:
            status = "failed"
        
        jobs.append({
            "job_id": job.get("id", ""),
            "name": job.get("name", ""),
            "enabled": job.get("enabled", True),
            "schedule_expr": schedule.get("expr", ""),
            "timezone": schedule.get("tz", ""),
            "session_target": job.get("sessionTarget", ""),
            "wake_mode": job.get("wakeMode", ""),
            "payload_message": job.get("payload", {}).get("message", "")[:500],  # Truncate long messages
            "model": job.get("payload", {}).get("model", ""),
            "delivery_mode": job.get("delivery", {}).get("mode", ""),
            "delivery_channel": job.get("delivery", {}).get("channel", ""),
            "delivery_target": job.get("delivery", {}).get("to", ""),
            "last_run_at": datetime.fromtimestamp(state.get("lastRunAtMs", 0) / 1000).isoformat() if state.get("lastRunAtMs") else None,
            "last_status": state.get("lastStatus", ""),
            "last_duration_ms": state.get("lastDurationMs", 0),
            "consecutive_errors": state.get("consecutiveErrors", 0),
            "next_run_at": datetime.fromtimestamp(state.get("nextRunAtMs", 0) / 1000).isoformat() if state.get("nextRunAtMs") else None,
            "updated_at": datetime.now().isoformat()
        })
    
    return jobs

# ======== Sync to Supabase ========
def sync_agent_status(supabase: Client, agents):
    """Sync agent statuses to Supabase"""
    if not supabase:
        return
    
    for agent in agents:
        try:
            # Check if agent exists
            existing = supabase.table("agent_status").select("id").eq("agent_name", agent["agent_name"]).execute()
            
            if existing.data:
                # Update existing
                supabase.table("agent_status").update({
                    "status": agent["status"],
                    "task_name": agent["task_name"],
                    "updated_at": agent["updated_at"],
                    "details": json.dumps(agent["details"])
                }).eq("agent_name", agent["agent_name"]).execute()
            else:
                # Insert new
                supabase.table("agent_status").insert({
                    "agent_name": agent["agent_name"],
                    "status": agent["status"],
                    "task_name": agent["task_name"],
                    "started_at": agent["started_at"],
                    "updated_at": agent["updated_at"],
                    "details": json.dumps(agent["details"])
                }).execute()
            
            print(f"✅ Synced agent: {agent['agent_name']} - {agent['status']}")
        except Exception as e:
            print(f"❌ Error syncing agent {agent['agent_name']}: {e}")

def sync_cron_jobs(supabase: Client, jobs):
    """Sync cron jobs to Supabase"""
    if not supabase:
        return
    
    for job in jobs:
        try:
            # Check if job exists
            existing = supabase.table("cron_jobs").select("id").eq("job_id", job["job_id"]).execute()
            
            if existing.data:
                # Update existing
                supabase.table("cron_jobs").update(job).eq("job_id", job["job_id"]).execute()
            else:
                # Insert new
                supabase.table("cron_jobs").insert(job).execute()
            
            print(f"✅ Synced cron job: {job['name']} - {job.get('last_status', 'unknown')}")
        except Exception as e:
            print(f"❌ Error syncing cron job {job['name']}: {e}")

def log_activity(supabase: Client, activity_type: str, description: str, agent_name: str = ""):
    """Log activity to Supabase"""
    if not supabase:
        return
    
    try:
        supabase.table("activity_log").insert({
            "agent_name": agent_name,
            "activity_type": activity_type,
            "description": description,
            "recorded_at": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        print(f"⚠️  Activity log error: {e}")

# ======== Demo Mode (No Supabase) ========
def print_demo_status(agents, jobs):
    """Print status when Supabase is not configured"""
    print("\n" + "="*50)
    print("🍃 Anime Office - OpenClaw Status (Demo Mode)")
    print("="*50)
    
    print("\n👥 Active Agents:")
    for agent in agents:
        emoji = "🟢" if agent["status"] == "working" else "🟡" if agent["status"] == "idle" else "🔴"
        print(f"  {emoji} {agent['agent_name']}: {agent['status']} - {agent['task_name']}")
    
    print("\n⚙️ Cron Jobs:")
    for job in jobs:
        emoji = "✅" if job.get("last_status") == "ok" else "❌" if job.get("last_status") == "error" else "⏳"
        print(f"  {emoji} {job['name']}: {job.get('schedule_expr', 'N/A')} (Last: {job.get('last_status', 'never')})")
    
    print("\n" + "="*50 + "\n")

# ======== Main Loop ========
def main():
    print("🍃 Starting OpenClaw Agent Status Sync Daemon...")
    print(f"📁 Sessions: {OPENCLAW_SESSIONS_DIR}")
    print(f"📁 Cron: {OPENCLAW_CRON_DIR}")
    print(f"⏱️  Sync interval: {SYNC_INTERVAL} seconds")
    
    supabase = get_supabase_client()
    
    if supabase:
        print("✅ Connected to Supabase!")
    else:
        print("⚠️  Running in demo mode (no Supabase)")
    
    print("\n🚀 Daemon started! Press Ctrl+C to stop.\n")
    
    while True:
        try:
            # Read OpenClaw data
            sessions_data = read_sessions_data()
            cron_data = read_cron_jobs()
            
            # Process data
            agents = process_agent_status(sessions_data)
            jobs = process_cron_jobs(cron_data)
            
            # Sync to Supabase or demo mode
            if supabase:
                sync_agent_status(supabase, agents)
                sync_cron_jobs(supabase, jobs)
                log_activity(supabase, "sync", f"Synced {len(agents)} agents and {len(jobs)} cron jobs")
            else:
                print_demo_status(agents, jobs)
            
            # Wait for next sync
            time.sleep(SYNC_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Daemon stopped by user. Sayonara! 🌸")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    main()
