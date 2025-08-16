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
            background: url('/static/New_York_5.webp') no-repeat center center;
            background-size: cover;
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
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            border: 3px solid #000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
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

        .dr-strange-image {
            width: 300px;
            height: 300px;
            margin: 20px auto;
            background: url('/static/Dr_Strange_Comic.png') no-repeat center center;
            background-size: contain;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            border: 4px solid #000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .dr-strange-webp-image {
            width: 300px;
            height: 300px;
            margin: 20px auto;
            background: url('/static/Dr_Strange_Comic.webp') no-repeat center center;
            background-size: contain;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            border: 4px solid #000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
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
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .speech-bubble::after {
            content: '';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 15px solid #000;
        }

        .speech-bubble::before {
            content: '';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-bottom: 12px solid #fff;
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
            margin: 60px auto;
            background: url('/static/Spider-man sprite.png') no-repeat center center;
            background-size: 100% 100%;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            animation: pixelGlow 3s ease-in-out infinite;
            display: block;
            border: 2px solid #00bfff;
            background-color: rgba(255, 255, 255, 0.1);
        }

        @keyframes pixelGlow {
            0%, 100% { 
                filter: brightness(1) contrast(1);
                transform: scale(1);
            }
            50% { 
                filter: brightness(1.2) contrast(1.1);
                transform: scale(1.05);
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
            margin: 60px auto;
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
                <div class="spider-man-sprite" title="Spider-Man"></div>
                
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
                <div class="dr-strange-image"></div>
                <div class="speech-bubble">
                    Hi Dr. Strange!
                </div>
            </div>
        </div>

        <div id="comicPanel1" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="speech-bubble">
                    Spider-Man! I need your help — I've spilled space dust all over New York City!
                </div>
            </div>
        </div>

        <div id="comicPanel2" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-image"></div>
                <div class="speech-bubble">
                    What's a little more dust on the streets? We've seen worse.
                </div>
            </div>
        </div>

        <div id="comicPanel3" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="speech-bubble">
                    This dust isn't ordinary, Spider-Man. If left unchecked... it could END THE WORLD!
                </div>
            </div>
        </div>

        <div id="comicPanel4" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-image"></div>
                <div class="speech-bubble">
                    ...Okay, okay. Guess I'll grab a broom.
                </div>
            </div>
        </div>

        <div id="comicPanel5" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="speech-bubble">
                    The dust is scattered across the East Village — start there before it spreads any further!
                </div>
            </div>
        </div>

        <div id="comicPanel6" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
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
        
        // Level 1 game variables
        let level1State = 'intro'; // intro, splash, gameplay, win, lose
        let playerX = 13;
        let playerY = 12;
        let playerDirection = 'right';
        let score = 0;
        let lives = 3;
        let dustCollected = 0;
        let totalDust = 0;
        let webShooterActive = false;
        let webShooterTimer = 0;
        let gameLoop;
        let canvas, ctx;
        
        // Level 1 map data (27x29 grid)
        const level1Map = [
            "###########################",
            "#W........###...........W#",
            "#.####.#.###.###.#.####.#",
            "#T#  #.#..... .....#. #T#",
            "#.#  #.#####-#####.#  #.#",
            "#.#  #.#   V V   #.#  #.#",
            "#.#  #.#  V   V  #.#  #.#",
            "#.#  #.#   V V   #.#  #.#",
            "#.#  #.#####-#####.#  #.#",
            "#T#  #.#..... .....#. #T#",
            "#.####.#.###.###.#.####.#",
            "#W........###...........#",
            "#########  S  ###########",
            "#...............T........#",
            "#.####.#####.#####.####.#",
            "#.#  #.#   #.#   #.#  #.#",
            "#.#  #.# W #.# W #.#  #.#",
            "#.#  #.#####.#####.#  #.#",
            "#.#  #.............#  #.#",
            "#.####.###.#.#.###.####.#",
            "#.....T...#.#.#...T.....#",
            "###.#####.#.#.#.#####.###",
            "#...#   #.......#   #...#",
            "#.#.# W ####### W #.#.#.#",
            "#.#.#   #.....#   #.#.#.#",
            "#.#.#####.#.#.#####.#.#.#",
            "#T.......T.#.#.T.......T#",
            "###########################"
        ];
        
        // Dust positions (calculated from map)
        let dustPositions = [];
        let webShooterPositions = [];
        let taxiStopPositions = [];
        
        // Building images
        let buildingImages = [];
        let buildingImagesLoaded = 0;
        
        // Street images
        let streetImages = [];
        let streetImagesLoaded = 0;
        
        // Load building images
        function loadBuildingImages() {
            const buildingPaths = [
                '/static/Building_1.png',
                '/static/Building_2.png',
                '/static/Building_3.png',
                '/static/Building_4.png',
                '/static/Building_5.png',
                '/static/Building_6.png'
            ];
            
            buildingPaths.forEach((path, index) => {
                const img = new Image();
                img.onload = function() {
                    buildingImagesLoaded++;
                };
                img.src = path;
                buildingImages[index] = img;
            });
        }
        
        // Load street images
        function loadStreetImages() {
            const streetPaths = [
                '/static/Street_1.png',
                '/static/Street_2.png',
                '/static/Street_3.png',
                '/static/Street_4.png'
            ];
            
            streetPaths.forEach((path, index) => {
                const img = new Image();
                img.onload = function() {
                    streetImagesLoaded++;
                };
                img.src = path;
                streetImages[index] = img;
            });
        }
        
        // Initialize level 1 data
        function initLevel1() {
            dustPositions = [];
            webShooterPositions = [];
            taxiStopPositions = [];
            
            for (let y = 0; y < level1Map.length; y++) {
                for (let x = 0; x < level1Map[y].length; x++) {
                    const tile = level1Map[y][x];
                    if (tile === '.') {
                        dustPositions.push({x, y});
                    } else if (tile === 'W') {
                        webShooterPositions.push({x, y});
                    } else if (tile === 'T') {
                        taxiStopPositions.push({x, y});
                    }
                }
            }
            totalDust = dustPositions.length;
            
            // Load building images
            loadBuildingImages();
            loadStreetImages();
        }

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
            
            // Start Level 1
            startLevel1();
        }

        // Level 1 functions
        function startLevel1() {
            level1State = 'splash';
            initLevel1();
            
            // Show Level 1 splash screen
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas style for comic book look
            canvas.style.border = '5px solid #000';
            canvas.style.boxShadow = '5px 5px 0px rgba(0,0,0,0.3)';
            
            // Draw splash screen
            ctx.fillStyle = '#1a1a2e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw comic-style title
            ctx.fillStyle = '#ffff00';
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 3;
            ctx.font = 'bold 48px Comic Sans MS';
            ctx.textAlign = 'center';
            
            const title = 'LEVEL 1: EAST VILLAGE';
            ctx.strokeText(title, canvas.width/2, 100);
            ctx.fillText(title, canvas.width/2, 100);
            
            // Draw East Village background
            const bgImage = new Image();
            bgImage.onload = function() {
                ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
                // Redraw title over background
                ctx.fillStyle = '#ffff00';
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 3;
                ctx.font = 'bold 48px Comic Sans MS';
                ctx.textAlign = 'center';
                ctx.strokeText(title, canvas.width/2, 100);
                ctx.fillText(title, canvas.width/2, 100);
            };
            bgImage.src = '/static/East_Village_Pixel_Scape.png';
            
            setTimeout(() => {
                level1State = 'gameplay';
                initGameplay();
            }, 2000);
        }
        
        function initGameplay() {
            canvas = document.getElementById('gameCanvas');
            ctx = canvas.getContext('2d');
            
            // Set canvas size to fit the map
            const tileSize = 20;
            canvas.width = level1Map[0].length * tileSize;
            canvas.height = level1Map.length * tileSize;
            
            // Start game loop
            gameLoop = setInterval(updateGame, 1000/60); // 60 FPS
            
            // Add keyboard controls
            document.addEventListener('keydown', handleKeyPress);
        }
        
        function updateGame() {
            if (level1State !== 'gameplay') return;
            
            // Update web shooter timer
            if (webShooterActive) {
                webShooterTimer--;
                if (webShooterTimer <= 0) {
                    webShooterActive = false;
                }
            }
            
            // Check win condition
            if (dustCollected >= totalDust) {
                level1State = 'win';
                clearInterval(gameLoop);
                showWinScreen();
                return;
            }
            
            // Check lose condition
            if (lives <= 0) {
                level1State = 'lose';
                clearInterval(gameLoop);
                showLoseScreen();
                return;
            }
            
            renderGame();
        }
        
        function renderGame() {
            if (!ctx) return;
            
            const tileSize = 20;
            
            // Clear canvas
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw background (East Village pixel art)
            const bgImage = new Image();
            bgImage.onload = function() {
                ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
                drawMapElements();
            };
            bgImage.src = '/static/East_Village_Pixel_Scape.png';
        }
        
        function drawMapElements() {
            const tileSize = 20;
            
            // Draw map elements
            for (let y = 0; y < level1Map.length; y++) {
                for (let x = 0; x < level1Map[y].length; x++) {
                    const tile = level1Map[y][x];
                    const drawX = x * tileSize;
                    const drawY = y * tileSize;
                    
                    // Draw street background for all non-building tiles
                    if (tile !== '#') {
                        if (streetImagesLoaded >= 4) {
                            // Select street image based on position for variety
                            const streetIndex = (x + y * 2) % 4;
                            const streetImg = streetImages[streetIndex];
                            if (streetImg) {
                                ctx.drawImage(streetImg, drawX, drawY, tileSize, tileSize);
                            }
                        }
                    }
                    
                    if (tile === '#') {
                        // Draw building with image
                        if (buildingImagesLoaded >= 6) {
                            // Select building image based on position for variety
                            const buildingIndex = (x + y * 3) % 6;
                            const buildingImg = buildingImages[buildingIndex];
                            if (buildingImg) {
                                ctx.drawImage(buildingImg, drawX, drawY, tileSize, tileSize);
                            }
                        } else {
                            // Fallback to simple square while images load
                            ctx.fillStyle = '#1a1a2e';
                            ctx.fillRect(drawX, drawY, tileSize, tileSize);
                            ctx.strokeStyle = '#00bfff';
                            ctx.lineWidth = 2;
                            ctx.strokeRect(drawX, drawY, tileSize, tileSize);
                        }
                    } else if (tile === '.') {
                        // Check if dust is still there
                        const dustExists = dustPositions.some(dust => dust.x === x && dust.y === y);
                        if (dustExists) {
                            // Draw space dust
                            ctx.fillStyle = '#ffffff';
                            ctx.beginPath();
                            ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 3, 0, 2 * Math.PI);
                            ctx.fill();
                        }
                    } else if (tile === 'W') {
                        // Draw web shooter
                        const webShooterExists = webShooterPositions.some(ws => ws.x === x && ws.y === y);
                        if (webShooterExists) {
                            ctx.fillStyle = '#00bfff';
                            ctx.beginPath();
                            ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 8, 0, 2 * Math.PI);
                            ctx.fill();
                            ctx.strokeStyle = '#ffffff';
                            ctx.lineWidth = 2;
                            ctx.stroke();
                        }
                    } else if (tile === 'T') {
                        // Draw taxi stop
                        ctx.fillStyle = '#ffff00';
                        ctx.fillRect(drawX + 2, drawY + 2, tileSize - 4, tileSize - 4);
                        ctx.strokeStyle = '#000';
                        ctx.lineWidth = 1;
                        ctx.strokeRect(drawX + 2, drawY + 2, tileSize - 4, tileSize - 4);
                    }
                }
            }
            
            // Draw player
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(playerX * tileSize + 2, playerY * tileSize + 2, tileSize - 4, tileSize - 4);
            
            // Draw HUD
            drawHUD();
        }
        
        function drawHUD() {
            const hudY = 25;
            
            // Lives
            ctx.fillStyle = '#ffffff';
            ctx.font = '16px Courier New';
            ctx.fillText(`Lives: ${lives}`, 10, hudY);
            
            // Score
            ctx.fillText(`Score: ${score}`, canvas.width/2 - 50, hudY);
            
            // Level
            ctx.fillText('Level 1: East Village', canvas.width - 200, hudY);
        }
        
        function handleKeyPress(event) {
            if (level1State !== 'gameplay') return;
            
            const newX = playerX;
            const newY = playerY;
            
            switch(event.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (newY > 0 && level1Map[newY - 1][newX] !== '#') {
                        playerY = newY - 1;
                        playerDirection = 'up';
                    }
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    if (newY < level1Map.length - 1 && level1Map[newY + 1][newX] !== '#') {
                        playerY = newY + 1;
                        playerDirection = 'down';
                    }
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (newX > 0 && level1Map[newY][newX - 1] !== '#') {
                        playerX = newX - 1;
                        playerDirection = 'left';
                    }
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (newX < level1Map[0].length - 1 && level1Map[newY][newX + 1] !== '#') {
                        playerX = newX + 1;
                        playerDirection = 'right';
                    }
                    break;
            }
            
            // Check for dust collection
            checkDustCollection();
            checkWebShooterCollection();
            checkTaxiStopCollection();
        }
        
        function checkDustCollection() {
            const dustIndex = dustPositions.findIndex(dust => dust.x === playerX && dust.y === playerY);
            if (dustIndex !== -1) {
                dustPositions.splice(dustIndex, 1);
                dustCollected++;
                score += 10;
            }
        }
        
        function checkWebShooterCollection() {
            const webShooterIndex = webShooterPositions.findIndex(ws => ws.x === playerX && ws.y === playerY);
            if (webShooterIndex !== -1) {
                webShooterPositions.splice(webShooterIndex, 1);
                webShooterActive = true;
                webShooterTimer = 360; // 6 seconds at 60 FPS
                score += 50;
            }
        }
        
        function checkTaxiStopCollection() {
            const taxiIndex = taxiStopPositions.findIndex(taxi => taxi.x === playerX && taxi.y === playerY);
            if (taxiIndex !== -1) {
                // Taxi ride effect (simplified for now)
                score += 25;
            }
        }
        
        function showWinScreen() {
            currentState = 'win';
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('titleScreen').classList.add('active');
        }
        
        function showLoseScreen() {
            currentState = 'lose';
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('titleScreen').classList.add('active');
        }

        // Event listeners
        document.addEventListener('click', function(e) {
            if (currentState === 'comic') {
                nextPanel();
            } else if (currentState === 'gameplay') {
                // Skip splash screen on click
                if (level1State === 'splash') {
                    level1State = 'gameplay';
                    initGameplay();
                }
            } else if (currentState === 'win' || currentState === 'lose') {
                // Return to title
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
                } else if (currentState === 'gameplay' && level1State === 'splash') {
                    // Skip splash screen
                    level1State = 'gameplay';
                    initGameplay();
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
