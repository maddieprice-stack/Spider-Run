#!/usr/bin/env python3
"""
Spider-Run Game Server
A Pac-Man-inspired, Spider-Man-themed maze game with comic book cut-scenes
"""

from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Main game HTML template
GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spider-Run</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #000;
            overflow: hidden;
            cursor: pointer;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }

        #gameCanvas {
            display: block;
            margin: 0 auto;
            background: #000;
        }

        .game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .comic-panel {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #fff;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }

        .comic-panel.active {
            display: flex;
        }

        .panel-content {
            text-align: center;
            max-width: 80%;
            padding: 20px;
        }

        .character-image {
            width: 200px;
            height: 200px;
            margin: 20px auto;
            border: 4px solid #000;
            background: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
        }

        .speech-bubble {
            background: #fff;
            border: 3px solid #000;
            border-radius: 20px;
            padding: 20px;
            margin: 20px;
            position: relative;
            max-width: 400px;
            font-size: 18px;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.4;
        }

        .speech-bubble::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-top: 15px solid #000;
        }

        .speech-bubble::before {
            content: '';
            position: absolute;
            bottom: -12px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-top: 12px solid #fff;
        }

        .title-screen {
            background: #000;
            color: #fff;
            text-align: center;
            padding: 40px;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 4px solid #00bfff;
            box-shadow: inset 0 0 20px rgba(0, 191, 255, 0.3);
            position: fixed;
            top: 0;
            left: 0;
            margin: 0;
        }

        .title-screen h1 {
            font-size: 5em;
            font-weight: bold;
            color: #00bfff;
            text-shadow: 3px 3px 0px #ff0000;
            margin-bottom: 40px;
            text-transform: uppercase;
            font-family: 'Courier New', monospace;
            letter-spacing: 4px;
        }

        .title-screen .subtitle {
            font-size: 1.2em;
            margin-bottom: 60px;
            color: #fff;
            font-family: 'Courier New', monospace;
        }

        .spider-man-sprite {
            width: 120px;
            height: 120px;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* Pixel art Spider-Man sprite - Running pose */
        .spider-man-sprite .pixel-sprite {
            width: 100px;
            height: 100px;
            background: 
                /* Head - Red with white eyes */
                linear-gradient(to right, transparent 15%, #ff0000 15%, #ff0000 85%, transparent 85%),
                linear-gradient(to bottom, transparent 5%, #ff0000 5%, #ff0000 35%, transparent 35%),
                /* White eyes */
                linear-gradient(to right, transparent 25%, #ffffff 25%, #ffffff 35%, transparent 35%),
                linear-gradient(to right, transparent 65%, #ffffff 65%, #ffffff 75%, transparent 75%),
                linear-gradient(to bottom, transparent 10%, #ffffff 10%, #ffffff 25%, transparent 25%),
                /* Black eye outlines */
                linear-gradient(to right, transparent 20%, #000000 20%, #000000 40%, transparent 40%),
                linear-gradient(to right, transparent 60%, #000000 60%, #000000 80%, transparent 80%),
                linear-gradient(to bottom, transparent 5%, #000000 5%, #000000 30%, transparent 30%),
                /* Torso - Red with blue center V-shape */
                linear-gradient(to right, transparent 10%, #ff0000 10%, #ff0000 90%, transparent 90%),
                linear-gradient(to bottom, transparent 35%, #ff0000 35%, #ff0000 75%, transparent 75%),
                /* Blue center section */
                linear-gradient(to right, transparent 35%, #0000ff 35%, #0000ff 65%, transparent 65%),
                linear-gradient(to bottom, transparent 45%, #0000ff 45%, #0000ff 65%, transparent 65%),
                /* Right arm - bent forward */
                linear-gradient(to right, transparent 5%, #ff0000 5%, #ff0000 25%, transparent 25%),
                linear-gradient(to bottom, transparent 25%, #ff0000 25%, #ff0000 45%, transparent 45%),
                linear-gradient(to right, transparent 10%, #0000ff 10%, #0000ff 20%, transparent 20%),
                linear-gradient(to bottom, transparent 30%, #0000ff 30%, #0000ff 40%, transparent 40%),
                /* Left arm - extended backward */
                linear-gradient(to right, transparent 75%, #ff0000 75%, #ff0000 95%, transparent 95%),
                linear-gradient(to bottom, transparent 20%, #ff0000 20%, #ff0000 50%, transparent 50%),
                linear-gradient(to right, transparent 80%, #0000ff 80%, #0000ff 90%, transparent 90%),
                linear-gradient(to bottom, transparent 25%, #0000ff 25%, #0000ff 45%, transparent 45%),
                /* Right leg - bent forward */
                linear-gradient(to right, transparent 20%, #ff0000 20%, #ff0000 40%, transparent 40%),
                linear-gradient(to bottom, transparent 75%, #ff0000 75%, #ff0000 95%, transparent 95%),
                linear-gradient(to right, transparent 25%, #0000ff 25%, #0000ff 35%, transparent 35%),
                linear-gradient(to bottom, transparent 80%, #0000ff 80%, #0000ff 90%, transparent 90%),
                /* Left leg - extended backward */
                linear-gradient(to right, transparent 60%, #ff0000 60%, #ff0000 80%, transparent 80%),
                linear-gradient(to bottom, transparent 70%, #ff0000 70%, #ff0000 95%, transparent 95%),
                linear-gradient(to right, transparent 65%, #0000ff 65%, #0000ff 75%, transparent 75%),
                linear-gradient(to bottom, transparent 75%, #0000ff 75%, #0000ff 90%, transparent 90%),
                /* Web patterns on red areas */
                linear-gradient(45deg, transparent 30%, #000000 30%, #000000 35%, transparent 35%),
                linear-gradient(-45deg, transparent 30%, #000000 30%, #000000 35%, transparent 35%),
                linear-gradient(45deg, transparent 70%, #000000 70%, #000000 75%, transparent 75%),
                linear-gradient(-45deg, transparent 70%, #000000 70%, #000000 75%, transparent 75%);
            background-size: 100% 100%;
            image-rendering: pixelated;
            animation: pixelGlow 3s ease-in-out infinite;
        }

        @keyframes pixelGlow {
            0%, 100% { 
                filter: brightness(1) contrast(1);
                transform: translate(-50%, -50%) scale(1);
            }
            50% { 
                filter: brightness(1.2) contrast(1.1);
                transform: translate(-50%, -50%) scale(1.05);
            }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        .instructions {
            background: #000;
            border: 2px solid #ffff00;
            padding: 20px;
            margin: 30px 0;
            max-width: 600px;
            color: #fff;
            font-family: 'Courier New', monospace;
        }

        .instructions h3 {
            color: #ffff00;
            margin-bottom: 15px;
            text-align: center;
        }

        .instructions ul {
            text-align: left;
            list-style: none;
            padding: 0;
        }

        .instructions li {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }

        .instructions li::before {
            content: '•';
            color: #ffff00;
            position: absolute;
            left: 0;
        }

        .menu-button {
            background: #000;
            color: #00bfff;
            border: 3px solid #00bfff;
            padding: 15px 30px;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            font-family: 'Courier New', monospace;
            transition: all 0.3s ease;
        }

        .menu-button:hover {
            background: #00bfff;
            color: #000;
            transform: scale(1.05);
        }

        .page-flip {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000;
            z-index: 20;
            display: none;
            animation: pageFlip 0.5s ease-in-out;
        }

        @keyframes pageFlip {
            0% { transform: rotateY(0deg); }
            50% { transform: rotateY(90deg); }
            100% { transform: rotateY(180deg); }
        }

        .halftone-bg {
            background-image: radial-gradient(circle, #000 1px, transparent 1px);
            background-size: 10px 10px;
        }

        .comic-border {
            border: 5px solid #000;
            box-shadow: 5px 5px 0px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="game-container">
        <!-- Title Screen -->
        <div id="titleScreen" class="comic-panel active">
            <div class="title-screen">
                <h1>SPIDER-RUN</h1>
                <div class="subtitle">A Pac-Man-Inspired Adventure</div>
                
                <!-- Spider-Man Sprite (replacing Pac-Man ghosts) -->
                <div class="spider-man-sprite">
                    <div class="pixel-sprite"></div>
                </div>
                
                <!-- Instructions Section -->
                <div class="instructions">
                    <h3>GAME INSTRUCTIONS</h3>
                    <ul>
                        <li>Use ARROW KEYS to move Spider-Man</li>
                        <li>Collect all SPACE DUST to win</li>
                        <li>Avoid ENEMIES or use POWER-UPS</li>
                        <li>You have 3 LIVES per level</li>
                        <li>Press ESC to pause the game</li>
                    </ul>
                </div>
                
                <div>
                    <button class="menu-button" onclick="startGame()">START GAME</button>
                </div>
            </div>
        </div>

        <!-- Comic Intro Panels -->
        <div id="comicPanel0" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Spider-Man
                </div>
                <div class="speech-bubble">
                    Hi Dr. Strange!
                </div>
            </div>
        </div>

        <div id="comicPanel1" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Dr. Strange
                </div>
                <div class="speech-bubble">
                    Spider-Man! I need your help — I've spilled space dust all over New York City!
                </div>
            </div>
        </div>

        <div id="comicPanel2" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Spider-Man
                </div>
                <div class="speech-bubble">
                    What's a little more dust on the streets? We've seen worse.
                </div>
            </div>
        </div>

        <div id="comicPanel3" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Dr. Strange
                </div>
                <div class="speech-bubble">
                    This dust isn't ordinary, Spider-Man. If left unchecked... it could END THE WORLD!
                </div>
            </div>
        </div>

        <div id="comicPanel4" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Spider-Man
                </div>
                <div class="speech-bubble">
                    ...Okay, okay. Guess I'll grab a broom.
                </div>
            </div>
        </div>

        <div id="comicPanel5" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Dr. Strange
                </div>
                <div class="speech-bubble">
                    The dust is scattered across the East Village — start there before it spreads any further!
                </div>
            </div>
        </div>

        <div id="comicPanel6" class="comic-panel">
            <div class="panel-content">
                <div class="character-image halftone-bg comic-border">
                    Dr. Strange
                </div>
                <div class="speech-bubble">
                    Be careful, Spider-Man. Some of your enemies are out tonight.
                </div>
            </div>
        </div>

        <!-- Game Canvas -->
        <canvas id="gameCanvas" width="800" height="600"></canvas>

        <!-- Page Flip Effect -->
        <div id="pageFlip" class="page-flip"></div>
    </div>

    <script>
        // Game state management
        let currentState = 'title';
        let currentPanel = 0;
        const totalPanels = 7;

        // Audio effects (placeholder)
        function playPageFlipSound() {
            // Placeholder for page flip sound
            console.log('Page flip sound played');
        }

        function playClickSound() {
            // Placeholder for click sound
            console.log('Click sound played');
        }

        // Panel navigation
        function showPanel(panelNumber) {
            // Hide all panels
            document.querySelectorAll('.comic-panel').forEach(panel => {
                panel.classList.remove('active');
            });

            // Show page flip effect
            const pageFlip = document.getElementById('pageFlip');
            pageFlip.style.display = 'block';
            playPageFlipSound();

            // After animation, show new panel
            setTimeout(() => {
                pageFlip.style.display = 'none';
                if (panelNumber === 0) {
                    document.getElementById('titleScreen').classList.add('active');
                } else {
                    document.getElementById(`comicPanel${panelNumber}`).classList.add('active');
                }
            }, 250);
        }

        // Game flow functions
        function startGame() {
            playClickSound();
            currentState = 'comic';
            currentPanel = 0;
            showPanel(0);
        }

        function showInstructions() {
            // Instructions are now displayed directly on the title screen
            playClickSound();
            // Could add additional instructions here if needed
        }

        function nextPanel() {
            if (currentState === 'comic' && currentPanel < totalPanels - 1) {
                currentPanel++;
                showPanel(currentPanel);
            } else if (currentState === 'comic' && currentPanel === totalPanels - 1) {
                // End of comic, start gameplay
                startGameplay();
            }
        }

        function startGameplay() {
            currentState = 'gameplay';
            document.querySelectorAll('.comic-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            
            // Initialize game canvas
            initGame();
        }

        // Game canvas setup
        function initGame() {
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas style for comic book look
            canvas.style.border = '5px solid #000';
            canvas.style.boxShadow = '5px 5px 0px rgba(0,0,0,0.3)';
            
            // Draw placeholder game screen
            ctx.fillStyle = '#1a1a2e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw comic-style title
            ctx.fillStyle = '#fff';
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 3;
            ctx.font = 'bold 48px Comic Sans MS';
            ctx.textAlign = 'center';
            
            const title = 'LEVEL 1: EAST VILLAGE';
            ctx.strokeText(title, canvas.width/2, 100);
            ctx.fillText(title, canvas.width/2, 100);
            
            // Draw placeholder game elements
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(350, 250, 100, 100); // Placeholder for Spider-Man
            
            ctx.fillStyle = '#ffff00';
            ctx.fillRect(100, 100, 20, 20); // Placeholder for dust
            
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(700, 500, 20, 20); // Placeholder for power-up
            
            // Draw instruction
            ctx.fillStyle = '#fff';
            ctx.font = '24px Comic Sans MS';
            ctx.fillText('Gameplay coming soon!', canvas.width/2, 400);
            ctx.fillText('Click anywhere to return to title', canvas.width/2, 450);
        }

        // Event listeners
        document.addEventListener('click', function(e) {
            if (currentState === 'comic') {
                nextPanel();
            } else if (currentState === 'gameplay') {
                // Return to title for now
                currentState = 'title';
                currentPanel = 0;
                showPanel(0);
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (currentState === 'comic') {
                    nextPanel();
                } else if (currentState === 'title') {
                    startGame();
                }
            }
        });

        // Initialize
        console.log('Spider-Run game loaded!');
        console.log('Click to advance through comic panels');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template_string(GAME_HTML)

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (for future assets)"""
    return send_from_directory('static', filename)

if __name__ == "__main__":
    print("🕷️ Spider-Run Game Server Starting...")
    print("🎮 Your game will be available at http://localhost:8081")
    print("📖 Comic book style intro sequence ready!")
    print("🎯 Click to advance through Dr. Strange and Spider-Man dialogue")
    app.run(debug=True, host='0.0.0.0', port=8081)
