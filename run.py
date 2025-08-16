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
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background: #000;
            overflow: hidden;
            cursor: pointer;
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
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
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
            background: linear-gradient(135deg, #ff0000 0%, #0000ff 100%);
            color: #fff;
            text-align: center;
            padding: 50px;
        }

        .title-screen h1 {
            font-size: 4em;
            text-shadow: 4px 4px 0px #000;
            margin-bottom: 30px;
            text-transform: uppercase;
        }

        .title-screen .subtitle {
            font-size: 1.5em;
            margin-bottom: 50px;
            text-shadow: 2px 2px 0px #000;
        }

        .menu-button {
            background: #fff;
            color: #000;
            border: 3px solid #000;
            padding: 15px 30px;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }

        .menu-button:hover {
            background: #000;
            color: #fff;
            transform: scale(1.05);
        }

        .page-flip {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
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
            <div class="title-screen comic-border">
                <h1>🕷️ Spider-Run 🕷️</h1>
                <div class="subtitle">A Pac-Man-Inspired Adventure</div>
                <div>
                    <button class="menu-button" onclick="startGame()">Start Game</button>
                    <button class="menu-button" onclick="showInstructions()">Instructions</button>
                </div>
            </div>
        </div>

        <!-- Comic Intro Panels -->
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
        const totalPanels = 6;

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
            currentPanel = 1;
            showPanel(1);
        }

        function showInstructions() {
            playClickSound();
            alert('Spider-Run Instructions:\\n\\n- Click to advance through comic panels\\n- Collect all space dust to win\\n- Avoid enemies or use power-ups\\n- Use arrow keys to move Spider-Man\\n- Press ESC to pause');
        }

        function nextPanel() {
            if (currentState === 'comic' && currentPanel < totalPanels) {
                currentPanel++;
                showPanel(currentPanel);
            } else if (currentState === 'comic' && currentPanel === totalPanels) {
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
