"""
🦊 Zootopia Office Dashboard
===========================
Anime-style office monitoring dashboard with Zootopia characters
"""

import streamlit as st
import os
from datetime import datetime

# ===== Configuration =====
st.set_page_config(
    page_title="Zootopia Office",
    page_icon="🦊",
    layout="wide"
)

# Character definitions
CHARACTERS = {
    "code_fox": {
        "name": "Code Fox",
        "emoji": "🦊",
        "role": "GitHub Code Review",
        "image": "characters/code-fox-1771189494211.png",
        "status": "working",
        "task": "Reviewing repositories..."
    },
    "news_bunny": {
        "name": "News Bunny",
        "emoji": "🐰",
        "role": "Daily News",
        "image": "characters/news-bunny-1771189509899.png",
        "status": "idle",
        "task": "Waiting for morning..."
    },
    "backup_bear": {
        "name": "Backup Bear",
        "emoji": "🐻",
        "role": "Backup Management",
        "image": "characters/backup-bear-1771189526301.png",
        "status": "idle",
        "task": "Waiting for backup..."
    },
    "weather_owl": {
        "name": "Weather Owl",
        "emoji": "🦉",
        "role": "Weather Updates",
        "image": "characters/weather-owl-1771189541236.png",
        "status": "idle",
        "task": "Watching the sky..."
    },
    "design_cat": {
        "name": "Design Cat",
        "emoji": "🐱",
        "role": "Midjourney Design",
        "image": "characters/design-cat-1771189556666.png",
        "status": "idle",
        "task": "Waiting for tasks..."
    },
    "monitor_panda": {
        "name": "Monitor Panda",
        "emoji": "🐼",
        "role": "System Monitor",
        "image": "characters/monitor-panda-1771189572021.png",
        "status": "working",
        "task": "Monitoring health..."
    }
}

# ===== CSS =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .main-title {
        font-size: 3rem;
        text-align: center;
        color: #FFD700;
        margin-bottom: 0.5rem;
    }
    .character-card {
        background: linear-gradient(145deg, #1e3a5f, #0d2137);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
    }
    .character-name {
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
    }
    .character-role {
        font-size: 0.9rem;
        color: #B8B8B8;
    }
    .section-header {
        font-size: 1.5rem;
        color: #FFD700;
        margin: 30px 0 20px 0;
        border-bottom: 2px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# ===== Main =====
def main():
    st.markdown('<p class="main-title">🏢 Zootopia Office Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;color:#B8B8B8">{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>', unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team Members", "6")
    col2.metric("Active Now", "2")
    col3.metric("Daily Tasks", "7")
    col4.metric("Status", "✅ OK")
    
    # Team
    st.markdown('<p class="section-header">👥 Meet the Team</p>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, (key, char) in enumerate(CHARACTERS.items()):
        with cols[idx % 3]:
            with st.container():
                st.markdown('<div class="character-card">', unsafe_allow_html=True)
                st.markdown(f"### {char['emoji']} **{char['name']}**")
                st.caption(char['role'])
                status_color = "🟢" if char['status'] == "working" else "🟡"
                st.write(f"{status_color} {char['status']}")
                st.caption(f"📝 {char['task']}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Activity
    st.markdown('<p class="section-header">📋 Recent Activity</p>', unsafe_allow_html=True)
    activities = [
        ("21:00", "🦊 Code Fox completed code review"),
        ("20:00", "🦉 Weather Owl fetched weather"),
        ("19:00", "🐰 News Bunny prepared news"),
        ("18:00", "🐼 Monitor Panda ran health check"),
        ("07:00", "🐻 Backup Bear completed backup")
    ]
    for time, text in activities:
        st.write(f"{time} - {text}")
    
    # Actions
    st.markdown('<p class="section-header">⚡ Quick Actions</p>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("🔄 Code Review")
    c2.button("📰 Get News")
    c3.button("💾 Run Backup")
    c4.button("🌤️ Weather")
    c5.button("🎨 Generate Image")
    c6.button("🏥 Health Check")

if __name__ == "__main__":
    main()
