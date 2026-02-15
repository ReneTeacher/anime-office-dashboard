"""
🦊 Zootopia Office 3D - Optimized Version
==========================================
Lightweight 3D game dashboard
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(
    page_title="Zootopia Office 3D",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Character data
CHARACTERS = [
    {"name": "Code Fox", "emoji": "🦊", "role": "GitHub Code Review", "color": "#FF6B35", "status": "working", "x": -3, "z": 2},
    {"name": "News Bunny", "emoji": "🐰", "role": "Daily News", "color": "#FFB6C1", "status": "idle", "x": -1.5, "z": 1},
    {"name": "Backup Bear", "emoji": "🐻", "role": "Backup", "color": "#8B4513", "status": "idle", "x": 0, "z": 3},
    {"name": "Weather Owl", "emoji": "🦉", "role": "Weather", "color": "#4A90D9", "status": "idle", "x": 1.5, "z": 1.5},
    {"name": "Design Cat", "emoji": "🐱", "role": "Design", "color": "#FF69B4", "status": "idle", "x": 3, "z": 2},
    {"name": "Monitor Panda", "emoji": "🐼", "role": "Monitor", "color": "#2E8B57", "status": "working", "x": 0, "z": 0}
]

THREE_JS = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Zootopia Office 3D</title>
    <style>
        * { margin: 0; padding: 0; }
        body { overflow: hidden; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); font-family: 'Segoe UI', sans-serif; }
        #container { width: 100vw; height: 100vh; }
        
        /* Title */
        #title {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FF6B35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            z-index: 100;
            text-shadow: 0 0 30px rgba(255,215,0,0.5);
        }
        
        /* Stats */
        #stats {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            border-radius: 15px;
            border: 1px solid rgba(255,215,0,0.3);
            color: white;
            z-index: 100;
        }
        
        #stats div { margin: 5px 0; }
        .stat-val { color: #FFD700; font-weight: bold; }
        
        /* Character Popup */
        #popup {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(15px);
            padding: 20px 40px;
            border-radius: 20px;
            border: 2px solid;
            text-align: center;
            display: none;
            z-index: 100;
        }
        
        #popup.visible { display: block; }
        
        #popup-name { font-size: 1.5rem; font-weight: bold; color: white; }
        #popup-role { color: rgba(255,255,255,0.6); margin: 5px 0; }
        #popup-status { 
            display: inline-block; padding: 5px 15px; border-radius: 20px; 
            font-weight: bold; font-size: 0.8rem;
        }
        
        /* Instructions */
        #instructions {
            position: absolute;
            bottom: 20px;
            right: 20px;
            color: rgba(255,255,255,0.5);
            font-size: 0.8rem;
            z-index: 100;
        }
        
        /* Loading */
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #FFD700;
            font-size: 1.2rem;
            z-index: 100;
        }
    </style>
</head>
<body>
    <div id="title">🏢 Zootopia Office 3D</div>
    <div id="stats">
        <div>👥 Team: <span class="stat-val">6</span></div>
        <div>⚡ Active: <span class="stat-val">2</span></div>
        <div>📅 Tasks: <span class="stat-val">7</span></div>
    </div>
    <div id="popup">
        <div id="popup-name"></div>
        <div id="popup-role"></div>
        <div id="popup-status"></div>
    </div>
    <div id="instructions">🖱️ Click on characters to interact</div>
    <div id="loading">Loading 3D Scene...</div>
    <div id="container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const characters = CHAR_DATA;
        
        let scene, camera, renderer;
        let characterMeshes = [];
        let raycaster, mouse;
        
        function init() {
            // Scene
            scene = new THREE.Scene();
            scene.fog = new THREE.Fog(0x0f0c29, 5, 25);
            
            // Camera
            camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
            camera.position.set(0, 4, 10);
            camera.lookAt(0, 1, 0);
            
            // Renderer
            renderer = new THREE.WebGLRenderer({antialias: true});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor(0x0f0c29);
            document.getElementById('container').appendChild(renderer.domElement);
            
            // Lights
            scene.add(new THREE.AmbientLight(0xffffff, 0.7));
            
            const dirLight = new THREE.DirectionalLight(0xffd700, 0.6);
            dirLight.position.set(5, 10, 5);
            scene.add(dirLight);
            
            // Floor
            const floorGeo = new THREE.PlaneGeometry(30, 30);
            const floorMat = new THREE.MeshStandardMaterial({color: 0x1a1a2e, roughness: 0.8});
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI/2;
            floor.position.y = 0;
            scene.add(floor);
            
            // Grid
            scene.add(new THREE.GridHelper(30, 30, 0x2a2a4e, 0x1a1a3e));
            
            // Windows (glowing)
            createWindows();
            
            // Desks
            createDesks();
            
            // Characters (simple shapes first, then try textures)
            createCharacters();
            
            // Particles
            createParticles();
            
            // Interaction
            raycaster = new THREE.Raycaster();
            mouse = new THREE.Vector2();
            
            window.addEventListener('resize', onResize);
            window.addEventListener('click', onClick);
            window.addEventListener('mousemove', onMouseMove);
            
            document.getElementById('loading').style.display = 'none';
            
            animate();
        }
        
        function createWindows() {
            const winGeo = new THREE.PlaneGeometry(4, 5);
            const winMat = new THREE.MeshBasicMaterial({
                color: 0xffd700, transparent: true, opacity: 0.2, side: THREE.DoubleSide
            });
            
            [-6, 6].forEach(x => {
                const win = new THREE.Mesh(winGeo, winMat);
                win.position.set(x, 2.5, -5);
                scene.add(win);
            });
        }
        
        function createDesks() {
            const deskGeo = new THREE.BoxGeometry(1.5, 0.1, 1);
            const deskMat = new THREE.MeshStandardMaterial({color: 0x3d2914});
            
            characters.forEach(c => {
                const desk = new THREE.Mesh(deskGeo, deskMat);
                desk.position.set(c.x, 0.5, c.z);
                scene.add(desk);
            });
        }
        
        function createCharacters() {
            characters.forEach((c, i) => {
                // Create group for character
                const group = new THREE.Group();
                group.position.set(c.x, 0.8, c.z);
                
                // Body (capsule shape)
                const bodyGeo = new THREE.CapsuleGeometry(0.4, 0.6, 4, 8);
                const bodyMat = new THREE.MeshStandardMaterial({
                    color: c.color,
                    emissive: c.color,
                    emissiveIntensity: 0.2
                });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = 0.4;
                group.add(body);
                
                // Head (sphere)
                const headGeo = new THREE.SphereGeometry(0.35, 16, 16);
                const head = new THREE.Mesh(headGeo, bodyMat);
                head.position.y = 1;
                group.add(head);
                
                // Eyes
                const eyeGeo = new THREE.SphereGeometry(0.08, 8, 8);
                const eyeMat = new THREE.MeshBasicMaterial({color: 0xffffff});
                
                const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
                leftEye.position.set(-0.12, 1.05, 0.28);
                group.add(leftEye);
                
                const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
                rightEye.position.set(0.12, 1.05, 0.28);
                group.add(rightEye);
                
                // Pupils
                const pupilGeo = new THREE.SphereGeometry(0.04, 8, 8);
                const pupilMat = new THREE.MeshBasicMaterial({color: 0x000000});
                
                const leftPupil = new THREE.Mesh(pupilGeo, pupilMat);
                leftPupil.position.set(-0.12, 1.05, 0.35);
                group.add(leftPupil);
                
                const rightPupil = new THREE.Mesh(pupilGeo, pupilMat);
                rightPupil.position.set(0.12, 1.05, 0.35);
                group.add(rightPupil);
                
                // Status indicator
                const statusGeo = new THREE.SphereGeometry(0.1, 8, 8);
                const statusMat = new THREE.MeshBasicMaterial({
                    color: c.status === 'working' ? 0x00ff00 : 0xffaa00
                });
                const status = new THREE.Mesh(statusGeo, statusMat);
                status.position.set(0.4, 1.4, 0);
                status.name = 'status';
                group.add(status);
                
                // Emoji label
                group.userData = c;
                group.name = 'character';
                
                scene.add(group);
                characterMeshes.push(group);
            });
        }
        
        function createParticles() {
            const count = 50;
            const geo = new THREE.BufferGeometry();
            const pos = new Float32Array(count * 3);
            
            for(let i=0; i<count*3; i+=3) {
                pos[i] = (Math.random()-0.5)*20;
                pos[i+1] = Math.random()*5;
                pos[i+2] = (Math.random()-0.5)*20;
            }
            
            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            
            const mat = new THREE.PointsMaterial({color: 0xffd700, size: 0.05, transparent: true, opacity: 0.5});
            const particles = new THREE.Points(geo, mat);
            particles.name = 'particles';
            scene.add(particles);
        }
        
        function onResize() {
            camera.aspect = window.innerWidth/window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
        
        function onMouseMove(e) {
            mouse.x = (e.clientX/window.innerWidth)*2 - 1;
            mouse.y = -(e.clientY/window.innerHeight)*2 + 1;
            camera.position.x = mouse.x * 0.5;
            camera.lookAt(0,1,0);
        }
        
        function onClick(e) {
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(characterMeshes, true);
            
            if(intersects.length > 0) {
                // Find parent group
                let obj = intersects[0].object;
                while(obj.parent && !obj.userData.name) {
                    obj = obj.parent;
                }
                
                if(obj.userData) {
                    showPopup(obj.userData);
                }
            } else {
                hidePopup();
            }
        }
        
        function showPopup(c) {
            const popup = document.getElementById('popup');
            document.getElementById('popup-name').textContent = c.emoji + ' ' + c.name;
            document.getElementById('popup-role').textContent = c.role;
            
            const status = document.getElementById('popup-status');
            status.textContent = c.status.toUpperCase();
            status.style.background = c.status === 'working' ? '#00ff00' : '#ffaa00';
            status.style.color = '#000';
            
            popup.style.borderColor = c.color;
            popup.classList.add('visible');
        }
        
        function hidePopup() {
            document.getElementById('popup').classList.remove('visible');
        }
        
        function animate() {
            requestAnimationFrame(animate);
            
            const time = Date.now() * 0.001;
            
            // Bob characters
            characterMeshes.forEach((g, i) => {
                g.position.y = 0.8 + Math.sin(time * 2 + i) * 0.05;
            });
            
            // Rotate particles
            scene.getObjectByName('particles').rotation.y += 0.001;
            
            // Status blink
            characterMeshes.forEach(g => {
                const status = g.getObjectByName('status');
                if(status) {
                    status.material.opacity = 0.5 + Math.sin(time * 3) * 0.5;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        init();
    </script>
</body>
</html>
"""

def main():
    html = THREE_JS.replace("CHAR_DATA = CHAR_DATA", f"const characters = {CHARACTERS}")
    components.html(html, height=700)

if __name__ == "__main__":
    main()
