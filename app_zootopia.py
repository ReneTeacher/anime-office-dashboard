"""
🦊 Zootopia Office Dashboard v2
=============================
Enhanced with animations and modern UI like reference designs
"""

import streamlit as st
import os
from datetime import datetime

# ===== Config =====
st.set_page_config(
    page_title="Zootopia Office",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Characters - Using raw URLs from GitHub
CHARACTERS = [
    {
        "id": "fox",
        "name": "Code Fox",
        "emoji": "🦊",
        "role": "GitHub Code Review",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/code-fox-1771189494211.png",
        "status": "working",
        "task": "Reviewing repositories...",
        "color": "#FF6B35"
    },
    {
        "id": "bunny",
        "name": "News Bunny",
        "emoji": "🐰",
        "role": "Daily News",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/news-bunny-1771189509899.png",
        "status": "idle",
        "task": "Waiting for morning...",
        "color": "#FFB6C1"
    },
    {
        "id": "bear",
        "name": "Backup Bear",
        "emoji": "🐻",
        "role": "Backup Management",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/backup-bear-1771189526301.png",
        "status": "idle",
        "task": "Scheduled backup at 00:00",
        "color": "#8B4513"
    },
    {
        "id": "owl",
        "name": "Weather Owl",
        "emoji": "🦉",
        "role": "Weather Updates",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/weather-owl-1771189541236.png",
        "status": "idle",
        "task": "Watching the sky...",
        "color": "#4A90D9"
    },
    {
        "id": "cat",
        "name": "Design Cat",
        "emoji": "🐱",
        "role": "Midjourney Design",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/design-cat-1771189556666.png",
        "status": "idle",
        "task": "Ready for creative tasks...",
        "color": "#FF69B4"
    },
    {
        "id": "panda",
        "name": "Monitor Panda",
        "emoji": "🐼",
        "role": "System Monitor",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/monitor-panda-1771189572021.png",
        "status": "working",
        "task": "Monitoring system...",
        "color": "#2E8B57"
    }
]

# ===== CSS =====
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    /* Title */
    .title-container {
        text-align: center;
        padding: 30px 0 20px;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 5px;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 400;
    }
    
    /* Character Avatar Circle */
    .avatar-container {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto 15px;
    }
    
    .avatar-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .avatar-circle:hover {
        transform: scale(1.08);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 
                    inset 0 0 30px rgba(255, 255, 255, 0.2);
    }
    
    .avatar-circle img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Status Indicator */
    .status-dot {
        position: absolute;
        bottom: 5px;
        right: 5px;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 3px solid #1a1a2e;
    }
    
    .status-working {
        background: linear-gradient(135deg, #00E676, #69F0AE);
        box-shadow: 0 0 15px #00E676;
        animation: pulse 2s infinite;
    }
    
    .status-idle {
        background: linear-gradient(135deg, #FFD700, #FFB300);
        box-shadow: 0 0 15px #FFD700;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Character Card */
    .char-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 24px;
        padding: 25px 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .char-card:hover {
        transform: translateY(-10px);
        background: linear-gradient(145deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 100%);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .char-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 10px 0 5px;
    }
    
    .char-role {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        margin-bottom: 10px;
    }
    
    .char-task {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
        font-style: italic;
    }
    
    /* Stats Card */
    .stat-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 5px;
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFD700;
        margin: 40px 0 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(255, 215, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Activity Item */
    .activity-item {
        background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #FFD700;
        transition: all 0.3s ease;
    }
    
    .activity-item:hover {
        background: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
        transform: translateX(5px);
    }
    
    .activity-time {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
    }
    
    .activity-text {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
    }
    
    /* Action Button */
    .action-btn {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 15px 10px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .action-btn:hover {
        background: linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,165,0,0.2) 100%);
        border-color: rgba(255, 215, 0, 0.5);
        transform: translateY(-3px);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden}
    header {visibility: hidden}
</style>
""", unsafe_allow_html=True)

# ===== Main =====
def main():
    # Title
    st.markdown("""
    <div class="title-container">
        <h1 class="main-title">🏢 Zootopia Office</h1>
        <p class="subtitle">Welcome to the AI Office • {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
    
    # ===== Stats =====
    cols = st.columns(4)
    stats = [("👥", "6", "Team Members"), ("⚡", "2", "Active Now"), ("📅", "7", "Daily Tasks"), ("✅", "100%", "Uptime")]
    
    for idx, (icon, value, label) in enumerate(stats):
        with cols[idx]:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 5px;">{}</div>
                <div class="stat-value">{}</div>
                <div class="stat-label">{}</div>
            </div>
            """.format(icon, value, label), unsafe_allow_html=True)
    
    # ===== Team Section =====
    st.markdown('<div class="section-header">👥 Meet the Team</div>', unsafe_allow_html=True)
    
    # 3x2 Grid
    cols = st.columns(3)
    
    for idx, char in enumerate(CHARACTERS):
        with cols[idx % 3]:
            # Status dot class
            status_class = "status-working" if char["status"] == "working" else "status-idle"
            
            st.markdown(f"""
            <div class="char-card">
                <div class="avatar-container">
                    <div class="avatar-circle" style="border-color: {char['color']};">
                        <img src="{char['image']}" alt="{char['name']}" onerror="this.src='https://via.placeholder.com/120?text={char['emoji']}'">
                    </div>
                    <div class="status-dot {status_class}"></div>
                </div>
                <div class="char-name">{char['emoji']} {char['name']}</div>
                <div class="char-role">{char['role']}</div>
                <div class="char-task">📝 {char['task']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== Activity Section =====
    st.markdown('<div class="section-header">📋 Recent Activity</div>', unsafe_allow_html=True)
    
    activities = [
        ("21:30", "🦊 Code Fox completed code review for todo-list"),
        ("21:00", "🦉 Weather Owl fetched today's weather forecast"),
        ("20:00", "🐰 News Bunny prepared daily news summary"),
        ("19:00", "🐼 Monitor Panda ran system health check"),
        ("07:00", "🐻 Backup Bear completed daily database backup"),
        ("06:00", "🦊 Code Fox reviewed 4 GitHub repositories")
    ]
    
    for time, text in activities:
        st.markdown(f"""
        <div class="activity-item">
            <div class="activity-time">{}</div>
            <div class="activity-text">{}</div>
        </div>
        """.format(time, text), unsafe_allow_html=True)
    
    # ===== Actions =====
    st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    cols = st.columns(6)
    actions = [
        ("🔄", "Run Code Review"),
        ("📰", "Get News"),
        ("💾", "Run Backup"),
        ("🌤️", "Check Weather"),
        ("🎨", "Generate Image"),
        ("🏥", "Health Check")
    ]
    
    for idx, (icon, label) in enumerate(actions):
        with cols[idx]:
            if st.button(f"{icon} {label}", key=f"btn_{idx}", use_container_width=True):
                st.toast(f"⚡ {label} triggered!")

if __name__ == "__main__":
    main()
