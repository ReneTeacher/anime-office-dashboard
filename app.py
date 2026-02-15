"""
🍃 Anime Office Command Center 🌸
A kawaii dashboard to monitor your OpenClaw agents like cute anime employees!
Now with REAL data from OpenClaw + Supabase!
"""

import streamlit as st
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

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

# ======== Custom CSS - Kawaii Anime Style ========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Nunito:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', 'Comic Neue', sans-serif !important;
    }
    
    /* Main Background - Cute Office Scene */
    .stApp {
        background: 
            linear-gradient(180deg, rgba(255,248,240,0.95) 0%, rgba(255,240,245,0.95) 100%),
            url('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80');
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
    
    /* Employee Card */
    .employee-card {
        background: white;
        border: 4px solid;
        border-radius: 25px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .employee-card.active {
        border-color: #2ECC71;
        box-shadow: 0 0 20px rgba(46,204,113,0.4);
    }
    
    .employee-card.idle {
        border-color: #F39C12;
        box-shadow: 0 0 15px rgba(243,156,18,0.3);
    }
    
    .employee-card.busy {
        border-color: #E74C3C;
        box-shadow: 0 0 15px rgba(231,76,60,0.3);
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .status-active {
        background: #2ECC71;
        color: white;
        animation: pulse 1.5s infinite;
    }
    
    .status-idle {
        background: #F39C12;
        color: white;
    }
    
    .status-busy {
        background: #E74C3C;
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Office Desk */
    .desk-container {
        background: linear-gradient(180deg, #D4A574 0%, #C49A6C 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-bottom: 8px solid #A67C52;
    }
    
    /* Cron Job Status */
    .cron-card {
        background: white;
        border-left: 5px solid;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
    }
    
    .cron-card.running {
        border-left-color: #2ECC71;
    }
    
    .cron-card.stopped {
        border-left-color: #E74C3C;
    }
    
    .cron-card.pending {
        border-left-color: #F39C12;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.9) !important;
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
</style>
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
        "stopped": "⏹️"
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
            if next_run > current_time := datetime.now().timestamp() * 1000:
                status = "pending"
            else:
                status = "running"
        else:
            status = "failed"
        
        # Format last run time
        last_run = state.get("lastRunAtMs")
        last_run_str = "Never"
        if last_run:
            last_run_dt = datetime.fromtimestamp(last_run / 1000)
            if last_run_dt.date() == datetime.now().date():
                last_run_str = last_run_dt.strftime("%H:%M")
            else:
                last_run_str = last_run_dt.strftime("%m-%d %H:%M")
        
        jobs.append({
            "name": job.get("name", "Unnamed Job"),
            "job_id": job.get("id", ""),
            "status": status,
            "schedule": schedule.get("expr", "N/A"),
            "timezone": schedule.get("tz", "UTC"),
            "last_run": last_run_str,
            "last_status": state.get("lastStatus", "never"),
            "last_duration": state.get("lastDurationMs", 0),
            "next_run": state.get("nextRunAtMs", 0),
            "enabled": job.get("enabled", True),
            "delivery": job.get("delivery", {})
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
    
    active_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) == "working")
    idle_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) == "idle")
    busy_count = sum(1 for a in agents_data if a.get("status", a.get("status", "")) == "failed")
    
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

# ======== Main Content ========
st.title("🍃 Anime Office Command Center 🌸")
st.markdown("### *Welcome to your kawaii workplace! Let's get things done!*\n")

# Live indicator
st.markdown(f"""
<div class="live-indicator" style="text-align: center; margin-bottom: 20px;">
    <span class="live-dot"></span> LIVE DATA - Last updated: {datetime.now().strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)

# ======== Top Stats Row ========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Agents", len(agents_data))

with col2:
    st.metric("✅ Working Now", active_count + busy_count)

with col3:
    st.metric("📅 Cron Jobs", len(cron_data_list))

with col4:
    st.metric("🕐 Today", datetime.now().strftime("%Y-%m-%d"))

# ======== Agent Office Grid ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">🏢 Our Hard-Working Team 🏢</h2>
    <p style="color: #666;">Watch your cute employees work hard! ✨</p>
</div>
""", unsafe_allow_html=True)

# Create office grid - handle both dict and list formats
if agents_data:
    num_cols = min(5, len(agents_data))
    cols = st.columns(num_cols)
    
    for i, agent in enumerate(agents_data[:10]):  # Show max 10 agents
        with cols[i % num_cols]:
            # Handle both dict and object formats
            if isinstance(agent, dict):
                name = agent.get("name", agent.get("agent_name", "Unknown"))
                status = agent.get("status", "idle")
                task = agent.get("task", agent.get("task_name", "No task"))
                last_update = agent.get("last_update", "")
                session_id = agent.get("session_id", "")
            else:
                name = str(agent)
                status = "working"
                task = "Active"
                last_update = ""
                session_id = ""
            
            status_class = get_status_class(status)
            
            # Generate avatar based on name
            import hashlib
            seed = hashlib.md5(name.encode()).hexdigest()[:8]
            avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=ffeaa7"
            
            st.markdown(f"""
            <div class="employee-card {status_class}">
                <img src="{avatar}" width="80" style="border-radius: 50%; border: 3px solid #FFB6C1;">
                <h3 style="margin: 10px 0 5px 0; color: #333 !important;">👤 {name}</h3>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">Agent</p>
                <span class="status-badge status-{status}">{get_status_emoji(status)} {status.upper()}</span>
                <p style="margin: 10px 0 5px 0; font-size: 0.85rem;">📝 {task}</p>
                {f'<p style="margin: 0; font-size: 0.8rem; color: #888;">🕐 {last_update}</p>' if last_update else ''}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📭 No active agents found. Start an agent to see it here!")

# ======== Cron Jobs Section ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">⚙️ Schedule Board ⚙️</h2>
    <p style="color: #666;">Current tasks and scheduled jobs! 📅</p>
</div>
""", unsafe_allow_html=True)

if cron_data_list:
    cron_cols = st.columns([2, 2, 2, 2, 1])
    
    # Header
    with cron_cols[0]:
        st.markdown("**📋 Task Name**")
    with cron_cols[1]:
        st.markdown("**⏰ Schedule**")
    with cron_cols[2]:
        st.markdown("**🔄 Status**")
    with cron_cols[3]:
        st.markdown("**🕐 Last Run**")
    with cron_cols[4]:
        st.markdown("**⚡**")
    
    # Rows
    for job in cron_data_list[:8]:  # Show max 8 cron jobs
        with cron_cols[0]:
            emoji = "🔔" if job.get("delivery", {}).get("channel") else "📋"
            st.markdown(f"{emoji} {job.get('name', 'Unnamed')}")
        with cron_cols[1]:
            st.code(job.get('schedule', 'N/A'), language="bash")
        with cron_cols[2]:
            status = job.get("status", "unknown")
            status_class = get_status_class(status)
            st.markdown(f"""
            <span class="cron-card {status_class}" style="display: inline-block; padding: 5px 10px; border-radius: 10px; border: none;">
                {get_status_emoji(status)} {status}
            </span>
            """, unsafe_allow_html=True)
        with cron_cols[3]:
            st.markdown(f"🕐 {job.get('last_run', 'Never')}")
        with cron_cols[4]:
            last_status = job.get("last_status", "")
            if last_status == "ok":
                st.markdown("✅")
            elif last_status == "error":
                st.markdown("❌")
            else:
                st.markdown("⏳")
else:
    st.info("📭 No cron jobs configured.")

# ======== Activity Log ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">📝 Recent Activity 📝</h2>
    <p style="color: #666;">What's happening in the office today! 📌</p>
</div>
""", unsafe_allow_html=True)

# Try to get activity from Supabase, fallback to generated
activities = []

if use_supabase:
    activity_data = fetch_recent_activity_from_supabase(5)
    if activity_data:
        for act in activity_data:
            activities.append((
                "📡",
                act.get("agent_name", "System"),
                act.get("description", "Activity logged"),
                act.get("recorded_at", "")[:16] if act.get("recorded_at") else "Unknown"
            ))

# If no Supabase activity, show cron job activities
if not activities:
    for job in cron_data_list[:5]:
        if job.get("last_status") == "ok":
            activities.append((
                "⚙️",
                "Cron",
                f"Completed: {job.get('name', 'Job')}",
                job.get('last_run', 'Unknown')
            ))

if not activities:
    activities = [
        ("🌸", "System", "Dashboard loaded", datetime.now().strftime("%H:%M")),
        ("⚙️", "System", "Connected to OpenClaw", datetime.now().strftime("%H:%M")),
    ]

for emoji, name, action, time_ago in activities:
    st.markdown(f"""
    <div class="kawaii-card">
        <span style="font-size: 1.5rem;" class="emoji-float">{emoji}</span>
        <strong>{name}</strong> - {action}
        <span style="float: right; color: #888;">{time_ago}</span>
    </div>
    """, unsafe_allow_html=True)

# ======== System Status ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">💻 System Status 💻</h2>
    <p style="color: #666;">OpenClaw connection info! 🔌</p>
</div>
""", unsafe_allow_html=True)

sys_cols = st.columns(3)

with sys_cols[0]:
    st.markdown("""
    <div class="kawaii-card" style="text-align: center;">
        <h3>📁 Sessions Dir</h3>
        <p style="color: #666;">{}</p>
    </div>
    """.format(OPENCLAW_SESSIONS_DIR), unsafe_allow_html=True)

with sys_cols[1]:
    sessions_count = len(agents_data)
    st.metric("📄 Active Sessions", sessions_count)

with sys_cols[2]:
    cron_enabled = sum(1 for c in cron_data_list if c.get("enabled", True))
    st.metric("✅ Enabled Jobs", cron_enabled)

# ======== Footer ========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p>🌸 Made with 💕 and ☕ by anime office team 🌸</p>
    <p>✨ Working hard or hardly working? Both! ✨</p>
    <p class="live-indicator">
        <span class="live-dot"></span> 
        Data synced from OpenClaw {}
    </p>
</div>
""".format(datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)

# ======== Auto-refresh ========
if st.session_state.auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
