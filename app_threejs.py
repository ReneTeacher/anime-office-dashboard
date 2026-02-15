"""
🦊 Zootopia Office - Three.js Game Engine
==========================================
Real 3D game-like dashboard using Three.js
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ===== Config =====
st.set_page_config(
    page_title="Zootopia Office 3D",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Character URLs from GitHub
CHARACTERS = [
    {
        "name": "Code Fox",
        "emoji": "🦊",
        "role": "GitHub Code Review",
        "color": "#FF6B35",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/code-fox-1771189494211.png",
        "position": {"x": -3, "y": 0, "z": 2},
        "status": "working"
    },
    {
        "name": "News Bunny",
        "emoji": "🐰",
        "role": "Daily News",
        "color": "#FFB6C1",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/news-bunny-1771189509899.png",
        "position": {"x": -1.5, "y": 0, "z": 1},
        "status": "idle"
    },
    {
        "name": "Backup Bear",
        "emoji": "🐻",
        "role": "Backup",
        "color": "#8B4513",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/backup-bear-1771189526301.png",
        "position": {"x": 0, "y": 0, "z": 3},
        "status": "idle"
    },
    {
        "name": "Weather Owl",
        "emoji": "🦉",
        "role": "Weather",
        "color": "#4A90D9",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/weather-owl-1771189541236.png",
        "position": {"x": 1.5, "y": 0, "z": 1.5},
        "status": "idle"
    },
    {
        "name": "Design Cat",
        "emoji": "🐱",
        "role": "Design",
        "color": "#FF69B4",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/design-cat-1771189556666.png",
        "position": {"x": 3, "y": 0, "z": 2},
        "status": "idle"
    },
    {
        "name": "Monitor Panda",
        "emoji": "🐼",
        "role": "Monitor",
        "color": "#2E8B57",
        "image": "https://raw.githubusercontent.com/ReneTeacher/anime-office-dashboard/main/characters/monitor-panda-1771189572021.png",
        "position": {"x": 0, "y": 0, "z": 0},
        "status": "working"
    }
]

# ===== Three.js Game Engine =====
THREE_JS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { overflow: hidden; background: #0a0a1a; }
        #game-container { width: 100vw; height: 100vh; }
        
        /* UI Overlay */
        #ui-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            padding: 20px;
            pointer-events: none;
            z-index: 100;
        }
        
        .title {
            font-family: 'Nunito', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FF6B35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        }
        
        .subtitle {
            font-family: 'Nunito', sans-serif;
            color: rgba(255,255,255,0.6);
            text-align: center;
            font-size: 1rem;
        }
        
        /* Stats Panel */
        #stats-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 20px;
            border: 1px solid rgba(255,215,0,0.3);
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            color: white;
            font-family: 'Nunito', sans-serif;
        }
        
        .stat-value {
            font-weight: 700;
            color: #FFD700;
        }
        
        /* Character Info Panel */
        #char-info {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 15px 30px;
            border: 1px solid rgba(255,215,0,0.3);
            display: none;
            text-align: center;
        }
        
        #char-info.visible { display: block; }
        
        #char-name {
            font-family: 'Nunito', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
        }
        
        #char-role {
            font-family: 'Nunito', sans-serif;
            color: rgba(255,255,255,0.6);
            font-size: 0.9rem;
        }
        
        #char-status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-top: 5px;
        }
        
        /* Loading */
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #FFD700;
            font-family: 'Nunito', sans-serif;
            font-size: 1.5rem;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div id="game-container"></div>
    
    <div id="ui-overlay">
        <div class="title">🏢 Zootopia Office 3D</div>
        <div class="subtitle" id="datetime">Loading...</div>
    </div>
    
    <div id="stats-panel">
        <div class="stat-item">👥 <span class="stat-value">6</span> Team Members</div>
        <div class="stat-item">⚡ <span class="stat-value">2</span> Active</div>
        <div class="stat-item">📅 <span class="stat-value">7</span> Daily Tasks</div>
        <div class="stat-item">✅ <span class="stat-value">100%</span> Uptime</div>
    </div>
    
    <div id="char-info">
        <div id="char-name"></div>
        <div id="char-role"></div>
        <div id="char-status"></div>
    </div>
    
    <div id="loading">Loading 3D Scene...</div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Character data from Python
        const characters = CHARACTER_DATA;
        
        // Three.js setup
        let scene, camera, renderer;
        let characterSprites = [];
        let raycaster, mouse;
        
        function init() {
            // Scene
            scene = new THREE.Scene();
            scene.fog = new THREE.Fog(0x0a0a1a, 5, 20);
            
            // Camera
            camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 3, 8);
            camera.lookAt(0, 1, 0);
            
            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setClearColor(0x0a0a1a);
            document.getElementById('game-container').appendChild(renderer.domElement);
            
            // Lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffd700, 0.8);
            directionalLight.position.set(5, 10, 5);
            scene.add(directionalLight);
            
            const pointLight1 = new THREE.PointLight(0xff6b35, 0.5, 10);
            pointLight1.position.set(-3, 2, 2);
            scene.add(pointLight1);
            
            const pointLight2 = new THREE.PointLight(0x4a90d9, 0.5, 10);
            pointLight2.position.set(3, 2, 2);
            scene.add(pointLight2);
            
            // Create floor
            createFloor();
            
            // Create windows
            createWindows();
            
            // Create desks
            createDesks();
            
            // Create character sprites
            createCharacters();
            
            // Create particles
            createParticles();
            
            // Raycaster for interaction
            raycaster = new THREE.Raycaster();
            mouse = new THREE.Vector2();
            
            // Events
            window.addEventListener('resize', onWindowResize);
            window.addEventListener('mousemove', onMouseMove);
            window.addEventListener('click', onClick);
            
            // Update datetime
            updateDateTime();
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
            
            // Start animation
            animate();
        }
        
        function createFloor() {
            // Main floor with gradient
            const floorGeometry = new THREE.PlaneGeometry(20, 20);
            const floorMaterial = new THREE.MeshStandardMaterial({
                color: 0x1a1a2e,
                roughness: 0.8,
                metalness: 0.2
            });
            const floor = new THREE.Mesh(floorGeometry, floorMaterial);
            floor.rotation.x = -Math.PI / 2;
            floor.position.y = 0;
            scene.add(floor);
            
            // Grid pattern
            const gridHelper = new THREE.GridHelper(20, 20, 0x2a2a4e, 0x1a1a3e);
            gridHelper.position.y = 0.01;
            scene.add(gridHelper);
        }
        
        function createWindows() {
            // Window frames with glow
            const windowGeometry = new THREE.PlaneGeometry(3, 4);
            
            // Left window
            const windowMaterial1 = new THREE.MeshBasicMaterial({
                color: 0xffd700,
                transparent: true,
                opacity: 0.3
            });
            const window1 = new THREE.Mesh(windowGeometry, windowMaterial1);
            window1.position.set(-5, 2, -3);
            scene.add(window1);
            
            // Right window
            const window2 = new THREE.Mesh(windowGeometry, windowMaterial1.clone());
            window2.position.set(5, 2, -3);
            scene.add(window2);
            
            // Window glow
            const glowGeometry = new THREE.PlaneGeometry(3.5, 4.5);
            const glowMaterial = new THREE.MeshBasicMaterial({
                color: 0xffd700,
                transparent: true,
                opacity: 0.1
            });
            
            const glow1 = new THREE.Mesh(glowGeometry, glowMaterial);
            glow1.position.set(-5, 2, -3.1);
            scene.add(glow1);
            
            const glow2 = new THREE.Mesh(glowGeometry, glowMaterial.clone());
            glow2.position.set(5, 2, -3.1);
            scene.add(glow2);
        }
        
        function createDesks() {
            // Simple desk representation
            const deskGeometry = new THREE.BoxGeometry(1.5, 0.1, 1);
            const deskMaterial = new THREE.MeshStandardMaterial({
                color: 0x3d2914,
                roughness: 0.7
            });
            
            // Create multiple desks
            const deskPositions = [
                {x: -3, z: 2}, {x: -1.5, z: 1}, {x: 0, z: 3},
                {x: 1.5, z: 1.5}, {x: 3, z: 2}, {x: 0, z: 0}
            ];
            
            deskPositions.forEach(pos => {
                const desk = new THREE.Mesh(deskGeometry, deskMaterial);
                desk.position.set(pos.x, 0.5, pos.z);
                scene.add(desk);
                
                // Desk legs
                const legGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.5);
                const legMaterial = new THREE.MeshStandardMaterial({color: 0x333333});
                
                const legPositions = [
                    {x: -0.6, z: -0.4}, {x: 0.6, z: -0.4},
                    {x: -0.6, z: 0.4}, {x: 0.6, z: 0.4}
                ];
                
                legPositions.forEach(lp => {
                    const leg = new THREE.Mesh(legGeometry, legMaterial);
                    leg.position.set(pos.x + lp.x, 0.25, pos.z + lp.z);
                    scene.add(leg);
                });
            });
        }
        
        function createCharacters() {
            const textureLoader = new THREE.TextureLoader();
            
            characters.forEach((char, index) => {
                textureLoader.load(char.image, (texture) => {
                    // Create sprite
                    const material = new THREE.SpriteMaterial({ 
                        map: texture,
                        transparent: true
                    });
                    const sprite = new THREE.Sprite(material);
                    
                    // Position
                    sprite.position.set(char.position.x, 1.2 + Math.sin(index) * 0.1, char.position.z);
                    sprite.scale.set(1.5, 1.5, 1);
                    
                    // Store data
                    sprite.userData = {
                        name: char.name,
                        emoji: char.emoji,
                        role: char.role,
                        color: char.color,
                        status: char.status,
                        originalY: sprite.position.y
                    };
                    
                    scene.add(sprite);
                    characterSprites.push(sprite);
                });
            });
        }
        
        function createParticles() {
            // Floating particles
            const particleCount = 100;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 20;
                positions[i + 1] = Math.random() * 5;
                positions[i + 2] = (Math.random() - 0.5) * 20;
            }
            
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            
            const material = new THREE.PointsMaterial({
                color: 0xffd700,
                size: 0.05,
                transparent: true,
                opacity: 0.6
            });
            
            const particles = new THREE.Points(geometry, material);
            particles.userData.isParticles = true;
            scene.add(particles);
        }
        
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
        
        function onMouseMove(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            
            // Subtle camera movement
            camera.position.x = mouse.x * 0.5;
            camera.lookAt(0, 1, 0);
        }
        
        function onClick() {
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(characterSprites);
            
            if (intersects.length > 0) {
                const char = intersects[0].object.userData;
                showCharacterInfo(char);
            } else {
                hideCharacterInfo();
            }
        }
        
        function showCharacterInfo(char) {
            const info = document.getElementById('char-info');
            document.getElementById('char-name').textContent = char.emoji + ' ' + char.name;
            document.getElementById('char-role').textContent = char.role;
            
            const statusEl = document.getElementById('char-status');
            statusEl.textContent = char.status.toUpperCase();
            statusEl.style.background = char.status === 'working' 
                ? 'linear-gradient(90deg, #00C853, #69F0AE)' 
                : 'linear-gradient(90deg, #FFD700, #FFB300)';
            statusEl.style.color = '#000';
            
            info.classList.add('visible');
        }
        
        function hideCharacterInfo() {
            document.getElementById('char-info').classList.remove('visible');
        }
        
        function updateDateTime() {
            const now = new Date();
            document.getElementById('datetime').textContent = now.toLocaleString();
        }
        
        function animate() {
            requestAnimationFrame(animate);
            
            const time = Date.now() * 0.001;
            
            // Animate characters (bobbing)
            characterSprites.forEach((sprite, i) => {
                sprite.position.y = sprite.userData.originalY + Math.sin(time + i) * 0.1;
            });
            
            // Animate particles
            scene.children.forEach(child => {
                if (child.userData && child.userData.isParticles) {
                    child.rotation.y += 0.001;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        // Initialize
        init();
    </script>
</body>
</html>
"""

# ===== Main =====
def main():
    # Inject character data
    html = THREE_JS_HTML.replace("CHARACTER_DATA = CHARACTER_DATA", f"const characters = {CHARACTERS}")
    
    # Render Three.js
    components.html(html, height=700)

if __name__ == "__main__":
    main()
