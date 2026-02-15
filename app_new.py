"""
🍃 Anime Office Command Center 🌸
A kawaii dashboard to monitor your OpenClaw agents like cute anime employees!
Now with REAL data from OpenClaw + Supabase!
"""

import streamlit as st
import json
import time
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

# ======== Configuration ========
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
OPENCLAW_SESSIONS_DIR = Path("/home/node/.openclaw/agents/main/sessions")
OPENCLAW_CRON_DIR = Path("/home/node/.openclaw/cron")

# ======== Page Config ========
st.set_page_config(
    page_title="🍃 Anime Office Command Center",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======== Initialize Supabase ========
@st.cache_resource
def get_supabase_client():
    """Initialize Supabase client (cached)"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# ======== Custom CSS - Kawaii Anime Office Style ========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Nunito:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', 'Comic Neue', sans-serif !important;
    }
    
    /* Main Background - Anime Office Scene */
    .stApp {
        background: 
            linear-gradient(180deg, rgba(255,248,245,0.97) 0%, rgba(255,240,250,0.97) 50%, rgba(248,240,255,0.97) 100%),
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,182,193,0.03) 35px, rgba(255,182,193,0.03) 70px);
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Title Styling */
    h1 {
        color: #FF6B9D !important;
        text-shadow: 3px 3px 0px #FFE66D, 5px 5px 0px rgba(0,0,0,0.1);
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    h2, h3 {
        color: #9B59B6 !important;
        font-weight: 700 !important;
    }
    
    /* Card Styling */
    .kawaii-card {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F5 100%);
        border: 3px solid #FFB6C1;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(255,182,193,0.4);
        transition: all 0.3s ease;
    }
    
    .kawaii-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(255,182,193,0.6);
    }
    
    /* Employee Desk - The main workspace */
    .desk-area {
        background: linear-gradient(180deg, #E8D5B7 0%, #D4C4A8 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border-bottom: 12px solid #A67C52;
        box-shadow: 
            inset 0 5px 15px rgba(255,255,255,0.3),
            0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .desk-area::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #FFB6C1, #FF69B4, #FFB6C1);
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Employee Card */
    .employee-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF8FA 100%);
        border: 4px solid;
        border-radius: 25px;
        padding: 20px;
        margin: 15px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .employee-card.active {
        border-color: #2ECC71;
        box-shadow: 0 0 25px rgba(46,204,113,0.5), 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .employee-card.idle {
        border-color: #F39C12;
        box-shadow: 0 0 20px rgba(243,156,18,0.4), 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .employee-card.busy {
        border-color: #E74C3C;
        box-shadow: 0 0 20px rgba(231,76,60,0.4), 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .employee-card:hover {
        transform: translateY(-5px) scale(1.02);
    }
    
    /* Worker Emoji - Animated */
    .worker-emoji {
        font-size: 3.5rem;
        display: inline-block;
        animation: work-bounce 1s ease-in-out infinite;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
    }
    
    @keyframes work-bounce {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-3px) rotate(-2deg); }
        50% { transform: translateY(0) rotate(0deg); }
        75% { transform: translateY(-3px) rotate(2deg); }
    }
    
    /* Typing animation for working agents */
    .worker-emoji.typing {
        animation: typing 0.5s steps(2) infinite;
    }
    
    @keyframes typing {
        0% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }
    
    /* Thinking animation */
    .worker-emoji.thinking {
        animation: think 2s ease-in-out infinite;
    }
    
    @keyframes think {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Idle animation */
    .worker-emoji.idle-anim {
        animation: idle-swing 3s ease-in-out infinite;
    }
    
    @keyframes idle-swing {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg); }
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        margin-top: 10px;
    }
    
    .status-active {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
        color: white;
        animation: pulse 1.5s infinite;
    }
    
    .status-idle {
        background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
        color: white;
    }
    
    .status-busy {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    /* Cron Job Board */
    .cron-board {
        background: linear-gradient(135deg, #FFFEF5 0%, #FFF8E7 100%);
        border: 4px solid #FFD700;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(255,215,0,0.3);
    }
    
    .cron-board h3 {
        color: #B8860B !important;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .cron-card {
        background: white;
        border: 3px solid;
        border-left: 8px solid;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .cron-card.running {
        border-color: #2ECC71;
        border-left-color: #2ECC71;
        background: linear-gradient(90deg, #E8F8F0 0%, white 100%);
    }
    
    .cron-card.stopped {
        border-color: #E74C3C;
        border-left-color: #E74C3C;
        background: linear-gradient(90deg, #FDEDED 0%, white 100%);
    }
    
    .cron-card.pending {
        border-color: #F39C12;
        border-left-color: #F39C12;
        background: linear-gradient(90deg, #FEF5E7 0%, white 100%);
    }
    
    .cron-card.failed {
        border-color: #E74C3C;
        border-left-color: #E74C3C;
        background: linear-gradient(90deg, #FDEDED 0%, white 100%);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.95) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: bold;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255,107,157,0.4);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border: 2px solid #FFB6C1;
        box-shadow: 0 5px 15px rgba(255,182,193,0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #9B59B6 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FF6B9D !important;
    }
    
    /* Emoji reactions */
    .emoji-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    /* Sakura petals falling */
    .sakura {
        position: fixed;
        font-size: 1.5rem;
        opacity: 0.6;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); }
        100% { transform: translateY(110vh) rotate(360deg); }
    }
    
    /* Real-time indicator */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: #2ECC71;
        font-weight: bold;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: #2ECC71;
        border-radius: 50%;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Office plant decoration */
    .plant {
        font-size: 2rem;
        position: absolute;
        animation: sway 4s ease-in-out infinite;
    }
    
    @keyframes sway {
        0%, 100% { transform: rotate(-3deg); }
        50% { transform: rotate(3deg); }
    }
    
    /* Task bubble */
    .task-bubble {
        background: linear-gradient(135deg, #E8F4FD 0%, #D4E9F7 100%);
        border-radius: 15px;
        padding: 10px 15px;
        margin-top: 10px;
        position: relative;
        font-size: 0.85rem;
        color: #2C3E50;
    }
    
    .task-bubble::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-bottom: 10px solid #E8F4FD;
    }
    
    /* Status-dot for cron */
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-dot.running {
        background: #2ECC71;
        animation: blink 1s infinite;
    }
    
    .status-dot.stopped {
        background: #E74C3C;
    }
    
    .status-dot.pending {
        background: #F39C12;
    }
    
    .status-dot.failed {
        background: #E74C3C;
        animation: blink 0.5s infinite;
    }
    
    /* Cron job details */
    .cron-details {
        font-size: 0.8rem;
        color: #666;
    }
    
    .cron-schedule {
        background: #f5f5f5;
        padding: 3px 8px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.75rem;
    }
</style>

<!-- Sakura Petals -->
<div class="sakura" style="left: 5%; animation-duration: 15s; animation-delay: 0s;">🌸</div>
<div class="sakura" style="left: 25%; animation-duration: 18s; animation-delay: 2s;">🌸</div>
<div class="sakura" style="left: 45%; animation-duration: 14s; animation-delay: 4s;">🌸</div>
<div class="sakura" style="left: 65%; animation-duration: 16s; animation-delay: 1s;">🌸</div>
<div class="sakura" style="left: 85%; animation-duration: 17s; animation-delay: 3s;">🌸</div>
""", unsafe_allow_html=True)

# ======== Helper Functions ========
def get_status_emoji(status):
    status_map = {
        "working": "🟢",
        "idle": "🟡", 
        "completed": "✅",
        "failed": "🔴",
        "running": "✅",
        "pending": "⏳",
        "stopped": "⏹️",
        "ok": "✅",
        "error": "❌"
    }
    return status_map.get(status, "⚪")

def get_status_class(status):
    status_map = {
        "working": "active",
        "idle": "idle",
        "completed": "active",
        "failed": "busy",
        "running": "running",
        "pending": "pending",
        "stopped": "stopped"
    }
    return status_map.get(status, "")

def get_worker_emoji(status):
    """Get animated worker emoji based on status"""
    workers = {
        "working": ["👨‍💻", "👩‍💻", "🧑‍💻", "🐱‍💻", "👨‍🔬", "👩‍🔬", "🧑‍🔬"],
        "idle": ["😴", "☕", "🧘", "📱", "🌸", "🐱", "🐶"],
        "active": ["👨‍💻", "👩‍💻", "🧑‍💻", "💪", "🚀", "⭐", "🌟"],
        "busy": ["😤", "🔥", "⚡", "💥", "🎯", "🏃", "🚨"],
        "completed": ["🎉", "🥳", "🎊", "✅", "🌈", "🦄", "✨"],
        "pending": ["⏰", "📅", "🔔", "💤", "😴", "🕐", "📆"],
        "stopped": ["⏸️", "🛑", "💤", "🔴", "😵", "💔", "🌙"],
        "failed": ["😵", "💥", "🔥", "❌", "😱", "🤯", "💣"]
    }
    status_list = workers.get(status, workers["idle"])
    return random.choice(status_list)

def get_work_animation(status):
    """Get animation class based on status"""
    animations = {
        "working": "typing",
        "active": "typing",
        "idle": "idle-anim",
        "completed": "thinking",
        "pending": "idle-anim",
        "stopped": "idle-anim",
        "failed": "thinking",
        "busy": "typing"
    }
    return animations.get(status, "")

# ======== Data Fetching Functions ========
@st.cache_data(ttl=10)
def fetch_agent_status_from_supabase():
    """Fetch real agent status from Supabase"""
    if not supabase:
        return None
    try:
        result = supabase.table("agent_status").select("*").execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching agents: {e}")
        return None

@st.cache_data(ttl=10)
def fetch_cron_jobs_from_supabase():
    """Fetch real cron jobs from Supabase"""
    if not supabase:
        return None
    try:
        result = supabase.table("cron_jobs").select("*").execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching cron jobs: {e}")
        return None

@st.cache_data(ttl=10)
def fetch_recent_activity_from_supabase(limit=10):
    """Fetch recent activity from Supabase"""
    if not supabase:
        return None
    try:
        result = supabase.table("activity_log").select("*").order("recorded_at", desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching activity: {e}")
        return None

def read_sessions_from_openclaw():
    """Read sessions directly from OpenClaw filesystem"""
    sessions_file = OPENCLAW_SESSIONS_DIR / "sessions.json"
    if not sessions_file.exists():
        return {}
    try:
        with open(sessions_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {}

def read_cron_from_openclaw():
    """Read cron jobs directly from OpenClaw filesystem"""
    jobs_file = OPENCLAW_CRON_DIR / "jobs.json"
    if not jobs_file.exists():
        return {"jobs": []}
    try:
        with open(jobs_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {"jobs": []}

def process_openclaw_sessions(sessions_data):
    """Process OpenClaw sessions into agent cards"""
    agents = []
    current_time = datetime.now().timestamp() * 1000
    
    for agent_id, session_info in sessions_data.items():
        updated_at = session_info.get("updatedAt", 0)
        time_diff = current_time - updated_at
        
        # Determine status
        if time_diff < 5 * 60 * 1000:  # Active in last 5 min
            status = "working"
        elif time_diff < 30 * 60 * 1000:  # Active in last 30 min
            status = "idle"
        else:
            status = "completed"
        
        # Get details
        details = session_info.get("skillsSnapshot", {})
        
        agents.append({
            "name": agent_id.replace("agent:", "").title(),
            "agent_id": agent_id,
            "status": status,
            "task": f"Session: {session_info.get('sessionId', 'N/A')[:8]}...",
            "thinking_level": session_info.get("thinkingLevel", "normal"),
            "last_update": datetime.fromtimestamp(updated_at / 1000).strftime("%H:%M:%S"),
            "session_id": session_info.get("sessionId", ""),
            "skills_count": len(details.get("skills", []))
        })
    
    return agents

def process_openclaw_crons(cron_data):
    """Process OpenClaw cron jobs"""
    jobs = []
    
    for job in cron_data.get("jobs", []):
        state = job.get("state", {})
        schedule = job.get("schedule", {})
        
        # Determine status
        if not job.get("enabled", True):
            status = "stopped"
        elif state.get("lastStatus") == "ok":
            next_run = state.get("nextRunAtMs", 0)
            current_time = datetime.now().timestamp() * 1000
            if next_run > current_time:
                status = "pending"
            else:
                status = "running"
        elif state.get("lastStatus") == "error":
            status = "failed"
        else:
            status = "pending"
        
        # Format last run time
        last_run = state.get("lastRunAtMs")
        last_run_str = "Never"
        if last_run:
            last_run_dt = datetime.fromtimestamp(last_run / 1000)
            if last_run_dt.date() == datetime.now().date():
                last_run_str = last_run_dt.strftime("%H:%M")
            else:
                last_run_str = last_run_dt.strftime("%m-%d %H:%M")
        
        # Format next run time
        next_run = state.get("nextRunAtMs")
        next_run_str = "Not scheduled"
        if next_run:
            next_run_dt = datetime.fromtimestamp(next_run / 1000)
            if next_run_dt.date() == datetime.now().date():
                next_run_str = next_run_dt.strftime("%H:%M")
            else:
                next_run_str = next_run_dt.strftime("%m-%d %H:%M")
        
        # Format duration
        duration_ms = state.get("lastDurationMs", 0)
        if duration_ms < 1000:
            duration_str = f"{duration_ms}ms"
        elif duration_ms < 60000:
            duration_str = f"{duration_ms/1000:.1f}s"
        else:
            duration_str = f"{duration_ms/60000:.1f}m"
        
        jobs.append({
            "name": job.get("name", "Unnamed Job"),
            "job_id": job.get("id", ""),
            "status": status,
            "schedule": schedule.get("expr", "N/A"),
            "timezone": schedule.get("tz", "UTC"),
            "last_run": last_run_str,
            "next_run": next_run_str,
            "last_status": state.get("lastStatus", "never"),
            "last_duration": duration_str,
            "next_run_raw": state.get("nextRunAtMs", 0),
            "enabled": job.get("enabled", True),
            "delivery": job.get("delivery", {}),
            "session_target": job.get("sessionTarget", ""),
            "payload_message": job.get("payload", {}).get("message", "")[:100] if job.get("payload", {}).get("message") else ""
        })
    
    return jobs

# ======== Main Data Loading ========
# Try Supabase first, fall back to OpenClaw filesystem
agents_data = []
cron_data_list = []
use_supabase = supabase is not None

if use_supabase:
    agents_data = fetch_agent_status_from_supabase() or []
    cron_data_list = fetch_cron_jobs_from_supabase() or []

# If no Supabase data, read from OpenClaw directly
if not agents_data:
    sessions = read_sessions_from_openclaw()
    agents_data = process_openclaw_sessions(sessions)

if not cron_data_list:
    crons = read_cron_from_openclaw()
    cron_data_list = process_openclaw_crons(crons)

# ======== Sidebar ========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #FF6B9D !important;">🌸 Menu 🌸</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Connection status
    if use_supabase:
        st.markdown('<div class="live-indicator"><span class="live-dot"></span> Connected to Supabase</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Demo Mode - No Supabase")
        st.caption("Set SUPABASE_URL and SUPABASE_KEY env vars")
    
    st.markdown("### 📊 Office Stats")
    
    active_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) in ["working", "active"])
    idle_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) == "idle")
    busy_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) in ["failed", "busy"])
    
    col1, col2 = st.columns(2)
    col1.metric("🟢 Working", active_count)
    col2.metric("🟡 Idle", idle_count)
    st.metric("🔴 Issues", busy_count)
    
    st.markdown("---")
    
    # Cron stats
    running_crons = sum(1 for c in cron_data_list if c.get("status") == "running")
    enabled_crons = sum(1 for c in cron_data_list if c.get("enabled", True))
    st.markdown("### ⚙️ Cron Jobs")
    st.metric("⚡ Active", running_crons, f"/ {enabled_crons} enabled")
    
    pending_crons = sum(1 for c in cron_data_list if c.get("status") == "pending")
    failed_crons = sum(1 for c in cron_data_list if c.get("status") == "failed")
    if failed_crons > 0:
        st.warning(f"❌ {failed_crons} failed jobs")
    if pending_crons > 0:
        st.info(f"⏳ {pending_crons} pending")
    
    st.markdown("---")
    
    # Auto-refresh toggle
    st.session_state.auto_refresh = st.toggle("🔄 Auto Refresh", value=True)
    refresh_rate = st.slider("⏱️ Refresh Rate (sec)", 1, 30, 5)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔔 Call Meeting"):
        st.toast("📢 Meeting called! All employees notified! 🎉")
    
    if st.button("☕ Coffee Break"):
        st.toast("☕ Coffee break time! Everyone takes a rest! 🍵")
    
    if st.button("📝 Generate Report"):
        st.toast("📊 Report generation started! 📈")
