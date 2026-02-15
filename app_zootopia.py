"""
🦊 Zootopia Office Dashboard v3
=============================
Animated office scene with moving characters
"""

import streamlit as st
from datetime import datetime

# ===== Config =====
st.set_page_config(
    page_title="Zootopia Office",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Characters with positions for office layout
CHARACTERS = [
    {
        "id": "fox",
        "name": "Code Fox",
        "emoji": "🦊",
        "role": "GitHub Code Review",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/code-fox-1771189494211.png",
        "status": "working",
        "task": "Coding...",
        "color": "#FF6B35",
        "position": "left"
    },
    {
        "id": "bunny",
        "name": "News Bunny", 
        "emoji": "🐰",
        "role": "Daily News",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/news-bunny-1771189509899.png",
        "status": "idle",
        "task": "Reading news...",
        "color": "#FFB6C1",
        "position": "center-left"
    },
    {
        "id": "bear",
        "name": "Backup Bear",
        "emoji": "🐻",
        "role": "Backup",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/backup-bear-1771189526301.png",
        "status": "idle",
        "task": "Resting...",
        "color": "#8B4513",
        "position": "center"
    },
    {
        "id": "owl",
        "name": "Weather Owl",
        "emoji": "🦉",
        "role": "Weather",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/weather-owl-1771189541236.png",
        "status": "idle",
        "task": "Watching sky...",
        "color": "#4A90D9",
        "position": "center-right"
    },
    {
        "id": "cat",
        "name": "Design Cat",
        "emoji": "🐱",
        "role": "Design",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/design-cat-1771189556666.png",
        "status": "idle",
        "task": "Creating...",
        "color": "#FF69B4",
        "position": "right"
    },
    {
        "id": "panda",
        "name": "Monitor Panda",
        "emoji": "🐼",
        "role": "Monitor",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/monitor-panda-1771189572021.png",
        "status": "working",
        "task": "Monitoring...",
        "color": "#2E8B57",
        "position": "desk-right"
    }
]

# ===== CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Main Container - Office Scene */
    .office-container {
        position: relative;
        width: 100%;
        height: 700px;
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }
    
    /* Office Background Elements */
    .office-bg {
        position: absolute;
        width: 100%;
        height: 100%;
        background: 
            /* Windows */
            radial-gradient(ellipse at 20% 10%, rgba(255,215,0,0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 10%, rgba(255,215,0,0.1) 0%, transparent 50%),
            /* Floor reflection */
            linear-gradient(180deg, transparent 60%, rgba(255,215,0,0.05) 100%),
            /* Main gradient */
            linear-gradient(180deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    }
    
    /* Desk */
    .desk {
        position: absolute;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 120px;
        background: linear-gradient(180deg, #3d2914 0%, #2a1d0f 100%);
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -5px 30px rgba(0,0,0,0.5);
    }
    
    /* Monitor on desk */
    .monitor {
        position: absolute;
        bottom: 200px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 130px;
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        border: 8px solid #333;
        border-radius: 10px;
        box-shadow: 0 0 30px rgba(0,200,255,0.3);
    }
    
    .monitor-screen {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #00c853 0%, #69f0ae 100%);
        border-radius: 5px;
        animation: screenGlow 3s ease-in-out infinite;
    }
    
    @keyframes screenGlow {
        0%, 100% { box-shadow: inset 0 0 30px rgba(0,200,100,0.3); }
        50% { box-shadow: inset 0 0 50px rgba(0,200,100,0.5); }
    }
    
    /* Character Container */
    .character-wrapper {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: all 0.5s ease;
    }
    
    /* Character Avatar */
    .character-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    
    .character-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Character Name Tag */
    .character-tag {
        background: rgba(0,0,0,0.7);
        padding: 5px 15px;
        border-radius: 20px;
        margin-top: 10px;
        backdrop-filter: blur(5px);
    }
    
    .character-name {
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .character-task {
        color: rgba(255,255,255,0.6);
        font-size: 0.7rem;
        text-align: center;
    }
    
    /* Status Indicator */
    .status-indicator {
        position: absolute;
        top: -5px;
        right: -5px;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        border: 3px solid #1a1a2e;
    }
    
    .status-working {
        background: linear-gradient(135deg, #00E676, #69F0AE);
        animation: pulse 1.5s infinite;
    }
    
    .status-idle {
        background: linear-gradient(135deg, #FFD700, #FFB300);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes floatReverse {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(10px); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    /* Position-based animations */
    .float-slow { animation: float 4s ease-in-out infinite; }
    .float-medium { animation: float 3s ease-in-out infinite; }
    .float-fast { animation: bounce 2s ease-in-out infinite; }
    .float-reverse { animation: floatReverse 3.5s ease-in-out infinite; }
    
    /* Title */
    .title-section {
        text-align: center;
        padding: 20px 0;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 40px;
        padding: 20px;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFD700;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.5);
    }
    
    /* Activity Panel */
    .activity-panel {
        position: absolute;
        bottom: 20px;
        left: 20px;
        right: 20px;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px 20px;
        display: flex;
        gap: 20px;
        overflow-x: auto;
    }
    
    .activity-item {
        white-space: nowrap;
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
    }
    
    /* Hide scrollbar */
    ::-webkit-scrollbar { display: none; }
    
    /* Window light effect */
    .window-light {
        position: absolute;
        top: 0;
        width: 150px;
        height: 200px;
        background: linear-gradient(180deg, rgba(255,215,0,0.15) 0%, transparent 100%);
        border-radius: 0 0 50% 50%;
    }
    
    .window-left { left: 10%; }
    .window-right { right: 10%; }
    
    /* Plants */
    .plant {
        position: absolute;
        bottom: 80px;
        font-size: 3rem;
    }
    
    .plant-left { left: 5%; }
    .plant-right { right: 5%; }
</style>
""", unsafe_allow_html=True)

# ===== Main =====
def main():
    # Title
    st.markdown("""
    <div class="title-section">
        <h1 class="main-title">🏢 Zootopia Office</h1>
        <p style="color: rgba(255,255,255,0.5);">{}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-value">6</div>
            <div class="stat-label">Team</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">2</div>
            <div class="stat-label">Active</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">7</div>
            <div class="stat-label">Tasks</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">100%</div>
            <div class="stat-label">Uptime</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Office Scene
    st.markdown('<div class="office-container">', unsafe_allow_html=True)
    
    # Background
    st.markdown('<div class="office-bg">', unsafe_allow_html=True)
    
    # Windows
    st.markdown('<div class="window-light window-left"></div>', unsafe_allow_html=True)
    st.markdown('<div class="window-light window-right"></div>', unsafe_allow_html=True)
    
    # Plants
    st.markdown('<div class="plant plant-left">🪴</div>', unsafe_allow_html=True)
    st.markdown('<div class="plant plant-right">🌵</div>', unsafe_allow_html=True)
    
    # Monitor
    st.markdown("""
    <div class="monitor">
        <div class="monitor-screen"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Desk
    st.markdown('<div class="desk"></div>', unsafe_allow_html=True)
    
    # Characters positioned in office
    positions = {
        "left": ("15%", "float-slow"),
        "center-left": ("30%", "float-medium"),
        "center": ("50%", "float-slow"),
        "center-right": ("70%", "float-reverse"),
        "right": ("85%", "float-medium"),
        "desk-right": ("75%", "float-fast")
    }
    
    for idx, char in enumerate(CHARACTERS):
        pos, anim = positions.get(char["position"], ("50%", "float-slow"))
        status_class = "status-working" if char["status"] == "working" else "status-idle"
        
        st.markdown(f"""
        <div class="character-wrapper" style="left: {pos}; bottom: 180px;" class="{anim}">
            <div style="position: relative;">
                <div class="character-avatar" style="border-color: {char['color']};">
                    <img src="{char['image']}" alt="{char['name']}">
                </div>
                <div class="status-indicator {status_class}"></div>
            </div>
            <div class="character-tag">
                <div class="character-name">{char['emoji']} {char['name']}</div>
                <div class="character-task">{char['task']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Activity bar at bottom
    st.markdown("""
    <div class="activity-panel">
        <div class="activity-item">🦊 Code Fox - Completed code review</div>
        <div class="activity-item">🐼 Monitor Panda - System healthy</div>
        <div class="activity-item">🦉 Weather Owl - Weather updated</div>
        <div class="activity-item">🐰 News Bunny - News ready</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)  # Close office-bg and office-container

if __name__ == "__main__":
    main()
