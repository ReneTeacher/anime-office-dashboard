"""
🍃 Anime Office Command Center 🌸
A kawaii dashboard to monitor your agents like cute anime employees!
"""

import streamlit as st
import json
import time
import random
from datetime import datetime
from pathlib import Path

# ======== Page Config ========
st.set_page_config(
    page_title="🍃 Anime Office Command Center",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    /* Decorative Elements */
    .sparkle {
        position: absolute;
        animation: sparkle 1.5s infinite;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #FFF0F5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FFB6C1;
        border-radius: 10px;
    }
    
    /* Emoji reactions */
    .emoji-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
</style>
""", unsafe_allow_html=True)

# ======== Session State for Real-time Updates ========
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# ======== Sample Data - Anime Employees ========
EMPLOYEES = [
    {
        "name": "Sakura-chan",
        "role": "Main Agent",
        "emoji": "🌸",
        "color": "#FFB6C1",
        "status": "active",
        "task": "Processing requests",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sakura&backgroundColor=ffeaa7",
        "quote": "I'll do my best! ✨"
    },
    {
        "name": "Yuki-kun", 
        "role": "Data Analyst",
        "emoji": "❄️",
        "color": "#74b9ff",
        "status": "active",
        "task": "Analyzing logs",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Yuki&backgroundColor=dfe6e9",
        "quote": "Data is beautiful! 📊"
    },
    {
        "name": "Hana-san",
        "role": "Scheduler",
        "emoji": "🌺",
        "color": "#fd79a8",
        "status": "idle",
        "task": "Waiting for cron",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hana&backgroundColor=fab1a0",
        "quote": "Time management! ⏰"
    },
    {
        "name": "Kaito-kun",
        "role": "Messenger",
        "emoji": "🎵",
        "color": "#a29bfe",
        "status": "busy",
        "task": "Delivering messages",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaito&backgroundColor=81ecec",
        "quote": "Message delivered! 💌"
    },
    {
        "name": "Mochi-chan",
        "role": "Memory Keeper",
        "emoji": "🍡",
        "color": "#ffeaa7",
        "status": "active",
        "task": "Storing memories",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mochi&backgroundColor=dfe6e9",
        "quote": "So sweet! 💕"
    }
]

# ======== Sample Cron Jobs ========
CRON_JOBS = [
    {"name": "Morning Check-in", "schedule": "0 8 * * *", "status": "completed", "last_run": "08:00 AM"},
    {"name": "Hourly Sync", "schedule": "0 * * * *", "status": "running", "last_run": "12:00 PM"},
    {"name": "Data Backup", "schedule": "0 2 * * *", "status": "pending", "last_run": "Yesterday"},
    {"name": "Cleanup Task", "schedule": "0 0 * * *", "status": "completed", "last_run": "12:00 AM"},
    {"name": "Health Check", "schedule": "*/15 * * * *", "status": "running", "last_run": "12:45 PM"},
]

# ======== Helper Functions ========
def get_status_emoji(status):
    status_map = {
        "active": "🟢",
        "idle": "🟡", 
        "busy": "🔴",
        "running": "✅",
        "completed": "🎉",
        "pending": "⏳",
        "stopped": "⏹️"
    }
    return status_map.get(status, "⚪")

def get_status_class(status):
    status_map = {
        "active": "active",
        "idle": "idle",
        "busy": "busy",
        "running": "running",
        "completed": "running",
        "pending": "pending",
        "stopped": "stopped"
    }
    return status_map.get(status, "")

# ======== Sidebar ========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #FF6B9D !important;">🌸 Menu 🌸</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Office Stats")
    
    active_count = sum(1 for e in EMPLOYEES if e["status"] == "active")
    idle_count = sum(1 for e in EMPLOYEES if e["status"] == "idle")
    busy_count = sum(1 for e in EMPLOYEES if e["status"] == "busy")
    
    col1, col2 = st.columns(2)
    col1.metric("🟢 Active", active_count)
    col2.metric("🟡 Idle", idle_count)
    st.metric("🔴 Busy", busy_count)
    
    st.markdown("---")
    
    # Auto-refresh toggle
    st.session_state.auto_refresh = st.toggle("🔄 Auto Refresh", value=True)
    
    refresh_rate = st.slider("⏱️ Refresh Rate (sec)", 1, 10, 3)
    
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

# ======== Top Stats Row ========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Employees", len(EMPLOYEES))

with col2:
    st.metric("✅ Working Now", active_count + busy_count)

with col3:
    running_crons = sum(1 for c in CRON_JOBS if c["status"] == "running")
    st.metric("⚙️ Active Tasks", running_crons)

with col4:
    st.metric("📅 Today", datetime.now().strftime("%Y-%m-%d"))

# ======== Employee Office Grid ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">🏢 Our Hard-Working Team 🏢</h2>
    <p style="color: #666;">Watch your cute employees work hard! ✨</p>
</div>
""", unsafe_allow_html=True)

# Create office grid
cols = st.columns(5)

for i, emp in enumerate(EMPLOYEES):
    with cols[i % 5]:
        status_class = get_status_class(emp["status"])
        
        st.markdown(f"""
        <div class="employee-card {status_class}">
            <img src="{emp['avatar']}" width="80" style="border-radius: 50%; border: 3px solid {emp['color']};">
            <h3 style="margin: 10px 0 5px 0; color: #333 !important;">{emp['emoji']} {emp['name']}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{emp['role']}</p>
            <span class="status-badge status-{emp['status']}">{get_status_emoji(emp['status'])} {emp['status'].upper()}</span>
            <p style="margin: 10px 0 5px 0; font-size: 0.85rem;">📝 {emp['task']}</p>
            <p style="margin: 0; font-size: 0.8rem; font-style: italic; color: #888;">"{emp['quote']}"</p>
        </div>
        """, unsafe_allow_html=True)

# ======== Cron Jobs Section ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">⚙️ Schedule Board ⚙️</h2>
    <p style="color: #666;">Current tasks and scheduled jobs! 📅</p>
</div>
""", unsafe_allow_html=True)

cron_cols = st.columns([2, 3, 2, 2, 1])

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
for cron in CRON_JOBS:
    with cron_cols[0]:
        st.markdown(f"📌 {cron['name']}")
    with cron_cols[1]:
        st.code(cron['schedule'], language="bash")
    with cron_cols[2]:
        status_class = get_status_class(cron['status'])
        st.markdown(f"""
        <span class="cron-card {status_class}" style="display: inline-block; padding: 5px 10px; border-radius: 10px; border: none;">
            {get_status_emoji(cron['status'])} {cron['status']}
        </span>
        """, unsafe_allow_html=True)
    with cron_cols[3]:
        st.markdown(f"🕐 {cron['last_run']}")
    with cron_cols[4]:
        if cron['status'] == 'running':
            st.markdown("🔵")
        elif cron['status'] == 'completed':
            st.markdown("✅")
        else:
            st.markdown("⏳")

# ======== Activity Log ========
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #9B59B6 !important;">📝 Activity Log 📝</h2>
    <p style="color: #666;">What's happening in the office today! 📌</p>
</div>
""", unsafe_allow_html=True)

# Sample activity log
activities = [
    ("🌸", "Sakura-chan", "Started processing new request", "Just now"),
    ("❄️", "Yuki-kun", "Completed data analysis", "2 min ago"),
    ("🌺", "Hana-san", "Scheduled new cron job", "5 min ago"),
    ("🎵", "Kaito-kun", "Delivered 5 messages", "10 min ago"),
    ("🍡", "Mochi-chan", "Saved memory to database", "15 min ago"),
]

for emoji, name, action, time_ago in activities:
    st.markdown(f"""
    <div class="kawaii-card">
        <span style="font-size: 1.5rem;" class="emoji-float">{emoji}</span>
        <strong>{name}</strong> - {action}
        <span style="float: right; color: #888;">{time_ago}</span>
    </div>
    """, unsafe_allow_html=True)

# ======== Footer ========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p>🌸 Made with 💕 and ☕ by anime office team your 🌸</p>
    <p>✨ Working hard or hardly working? Both! ✨</p>
</div>
""", unsafe_allow_html=True)

# ======== Auto-refresh ========
if st.session_state.auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
