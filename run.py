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
            margin: 20px auto;
            background: #000;
            border: 3px solid #00bfff;
            box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
            max-width: 95vw;
            max-height: 85vh;
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
            margin-bottom: 30px;
            color: #fff;
            font-family: 'Courier New', monospace;
        }

        .spider-man-sprite {
            width: 120px;
            height: 120px;
            margin: 30px auto;
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

        .spider-man-sprite-above-instructions {
            text-align: center;
            margin: 5px auto;
            padding: 5px;
        }
        
        .spider-man-sprite-above-instructions img {
            border-radius: 10px;
            transition: transform 0.3s ease;
        }
        
        .spider-man-sprite-above-instructions img:hover {
            transform: scale(1.1);
        }

        .instructions {
            background: #000;
            border: 2px solid #ffff00;
            padding: 20px;
            margin: 10px auto;
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
            background: transparent;
            z-index: 20;
            display: none;
        }

        .halftone-bg {
            background-image: radial-gradient(circle, #000 1px, transparent 1px);
            background-size: 10px 10px;
        }

        .comic-border {
            border: 5px solid #000;
            box-shadow: 5px 5px 0px rgba(0,0,0,0.3);
        }
        
        /* Win/Loss Cut Scene Styles */
        .win-loss-cutscene {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }
        
        .win-loss-cutscene.active {
            opacity: 1;
        }
        
        .cutscene-panel {
            background: #fff;
            border: 4px solid #000;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            max-width: 600px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .cutscene-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 2px,
                rgba(0, 0, 0, 0.1) 2px,
                rgba(0, 0, 0, 0.1) 4px
            );
            pointer-events: none;
        }
        
        .game-over-text {
            font-family: 'Courier New', monospace;
            font-size: 48px;
            font-weight: bold;
            color: #ff0000;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
            animation: gameOverGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes gameOverGlow {
            0% { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); }
            100% { text-shadow: 2px 2px 20px rgba(255, 0, 0, 0.8); }
        }
        
        .win-text {
            font-family: 'Courier New', monospace;
            font-size: 36px;
            font-weight: bold;
            color: #00ff00;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
            animation: winGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes winGlow {
            0% { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); }
            100% { text-shadow: 2px 2px 20px rgba(0, 255, 0, 0.8); }
        }
        
        .spider-man-defeated {
            width: 200px;
            height: 200px;
            margin: 20px auto;
            background: url('/static/Spider-man sprite.png') no-repeat center center;
            background-size: contain;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            opacity: 0.7;
            transform: scale(0.8);
            animation: defeatedBounce 3s ease-in-out infinite;
        }
        
        @keyframes defeatedBounce {
            0%, 100% { transform: scale(0.8) translateY(0px); }
            50% { transform: scale(0.8) translateY(-10px); }
        }
        
        .spider-man-victory {
            width: 200px;
            height: 200px;
            margin: 20px auto;
            background: url('/static/Spider-man sprite.png') no-repeat center center;
            background-size: contain;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            animation: victoryBounce 2s ease-in-out infinite;
        }
        
        @keyframes victoryBounce {
            0%, 100% { transform: scale(1) translateY(0px); }
            50% { transform: scale(1.1) translateY(-15px); }
        }
        
        .quip-bubble {
            background: #fff;
            border: 3px solid #000;
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
            position: relative;
            font-family: 'Comic Sans MS', cursive;
            font-size: 18px;
            line-height: 1.4;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            opacity: 0;
            transform: scale(0.8);
            animation: quipAppear 1s ease-out 1s forwards;
        }
        
        @keyframes quipAppear {
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .quip-bubble::before {
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
        
        .quip-bubble::after {
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
        
        .cutscene-buttons {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        
        .cutscene-button {
            background: #00bfff;
            color: #fff;
            border: 3px solid #000;
            border-radius: 10px;
            padding: 15px 30px;
            font-family: 'Courier New', monospace;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        .cutscene-button:hover {
            background: #0099cc;
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        }
        
        .cutscene-button.retry {
            background: #ff6b35;
        }
        
        .cutscene-button.retry:hover {
            background: #e55a2b;
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
                
                <!-- Additional Spider-Man Sprite above instructions -->
                <div class="spider-man-sprite-above-instructions">
                    <img src="/static/Spider-man-sprite.png" alt="Spider-Man" style="width: 80px; height: 80px;">
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
                    <button class="menu-button" id="startButton">START GAME</button>
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
        
        <!-- Background Music -->
        <audio id="backgroundMusic" loop>
            <source src="/static/background_music.mp3" type="audio/mpeg">
        </audio>

        <!-- Page Flip Effect -->
        <div id="pageFlip" class="page-flip"></div>
        
        <!-- Win/Loss Cut Scenes -->
        <div id="winCutscene" class="win-loss-cutscene">
            <div class="cutscene-panel">
                <div class="win-text">LEVEL COMPLETE!</div>
                <div class="spider-man-victory"></div>
                <div class="quip-bubble" id="winQuip"></div>
                <div class="cutscene-buttons">
                    <button class="cutscene-button" onclick="returnToTitle()">EXIT</button>
                </div>
            </div>
        </div>
        
        <div id="loseCutscene" class="win-loss-cutscene">
            <div class="cutscene-panel">
                <div class="game-over-text">GAME OVER</div>
                <div class="spider-man-defeated"></div>
                <div class="quip-bubble" id="loseQuip"></div>
                <div class="cutscene-buttons">
                    <button class="cutscene-button retry" onclick="retryLevel()">RETRY</button>
                    <button class="cutscene-button" onclick="returnToTitle()">EXIT</button>
                </div>
            </div>
        </div>
        
        <div id="gameOverCutscene" class="win-loss-cutscene">
            <div class="cutscene-panel">
                <div class="game-over-text">GAME OVER</div>
                <div class="spider-man-defeated"></div>
                <div class="quip-bubble" id="gameOverQuip"></div>
                <div class="cutscene-buttons">
                    <button class="cutscene-button retry" onclick="retryGame()">RETRY</button>
                    <button class="cutscene-button" onclick="returnToTitle()">EXIT</button>
                </div>
            </div>
        </div>
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
        let lives = 5;
        let dustCollected = 0;
        let totalDust = 0;
        let webShooterActive = false;
        let webShooterTimer = 0;
        let gameLoop;
        let canvas, ctx;
        
        // Taxi riding system
        let isRidingTaxi = false;
        let taxiX = 0;
        let taxiY = 0;
        let taxiDirection = 'right';
        let taxiSpeed = 0.3; // Speed multiplier for taxi movement
        let taxiMoveTimer = 0;
        
        // Swing animation system
        let swingAnimationCounter = 0;
        let lastPlayerX = 13;
        let lastPlayerY = 12;
        
        // Level 1 map data based on classic Pac-Man layout (25x15)
        const level1Map = [
            "#########################",
            "#W........###...........W#",
            " .####.#.###.###.#.####.#",
            "# #  #.#..... .....#  #T#",
            "#.#  #.#####-#####.#  #.#",
            "#.#  #.#   V V   #.#  #.#",
            "#.#  #.#  V   V  #.#  #.#",
            "#.#  #.#   V V   #.#  #.#",
            "#.#  #.#####-#####.#  #.#",
            "#T#  #.#..... .....#  # #",
            "#.####.#.###.###.#.####.#",
            "#W........###...........#",
            "#########  S  ###########",
            "...............T.........",
            "#########################"
        ];
        
        // Function to process ASCII maze with flood-fill
        function processMazeWithFloodFill(asciiMaze) {
            // Convert ASCII to 2D grid
            const grid = asciiMaze.map(row => row.split(''));
            
            // Find all walkable tiles on the border and player spawn
            const reachable = new Set();
            const queue = [];
            
            // Add border walkable tiles to queue
            for (let y = 0; y < grid.length; y++) {
                for (let x = 0; x < grid[y].length; x++) {
                    // Check if it's a border tile
                    const isBorder = (y === 0 || y === grid.length - 1 || x === 0 || x === grid[y].length - 1);
                    
                    if (isBorder && isWalkable(grid[y][x])) {
                        const key = `${y},${x}`;
                        queue.push([y, x]);
                        reachable.add(key);
                    }
                }
            }
            
            // Add player spawn point to queue (if not already added)
            const spawnKey = `${12},${13}`; // Player spawn position
            if (!reachable.has(spawnKey) && isWalkable(grid[12][13])) {
                queue.push([12, 13]);
                reachable.add(spawnKey);
            }
            
            // Flood-fill from border and spawn
            while (queue.length > 0) {
                const [y, x] = queue.shift();
                
                // Check all 4 directions
                const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
                for (let [dy, dx] of directions) {
                    const ny = y + dy;
                    const nx = x + dx;
                    
                    if (ny >= 0 && ny < grid.length && nx >= 0 && nx < grid[ny].length) {
                        const key = `${ny},${nx}`;
                        if (!reachable.has(key) && isWalkable(grid[ny][nx])) {
                            reachable.add(key);
                            queue.push([ny, nx]);
                        }
                    }
                }
            }
            
            // Convert unreached walkable tiles to black voids
            for (let y = 0; y < grid.length; y++) {
                for (let x = 0; x < grid[y].length; x++) {
                    if (isWalkable(grid[y][x]) && !reachable.has(`${y},${x}`)) {
                        grid[y][x] = '#'; // Convert to black void (wall)
                    }
                }
            }
            
            // Convert back to ASCII
            return grid.map(row => row.join(''));
        }
        
        function isWalkable(char) {
            return char === '.' || char === ' ' || char === 'W' || char === 'T' || 
                   char === 'V' || char === '-' || char === 'S';
        }
        
        function isPassable(char) {
            return char === '.' || char === ' ' || char === 'W' || char === 'T' || 
                   char === 'V' || char === '-' || char === 'S';
        }
        
        // Dust positions (calculated from map)
        let dustPositions = [];
        let webShooterPositions = [];
        let taxiStopPositions = [];
        
        // Villain system
        let villains = [];
        let villainPen = { x: 13, y: 6 }; // Center of villain pen
        let villainSpawns = [
            { x: 12, y: 5 }, { x: 14, y: 5 },
            { x: 11, y: 6 }, { x: 15, y: 6 },
            { x: 12, y: 7 }, { x: 14, y: 7 },
            { x: 13, y: 5 }, { x: 13, y: 7 }, // Additional spawns for more villains
            { x: 11, y: 5 }, { x: 15, y: 5 },
            { x: 12, y: 6 }, { x: 14, y: 6 }, // More spawns for 9 villains
            { x: 11, y: 7 }, { x: 15, y: 7 }
        ];
        
        // Villain types for Level 1
        const villainTypes = [
            { name: 'Doc Ock', color: '#228B22', speed: 0.9, ability: 'alleyBlock' },
            { name: 'Green Goblin', color: '#32CD32', speed: 1.0, ability: 'pumpkinBomb' },
            { name: 'Vulture', color: '#006400', speed: 1.1, ability: 'windGust' },
            { name: 'Venom', color: '#000000', speed: 1.1, ability: 'windGust' },
            { name: 'Lizard', color: '#228B22', speed: 1.1, ability: 'windGust' },
            { name: 'Mysterio', color: '#4B0082', speed: 1.1, ability: 'windGust' },
            { name: 'Hobgoblin', color: '#FF4500', speed: 1.1, ability: 'windGust' },
            { name: 'Prowler', color: '#800080', speed: 1.1, ability: 'windGust' },
            { name: 'Sandman', color: '#D2B48C', speed: 1.1, ability: 'windGust' }
        ];
        
        // Villain state
        let villainAbilities = {
            alleyBlock: { active: false, timer: 0, cooldown: 720 }, // 12 seconds at 60fps
            pumpkinBomb: { active: false, timer: 0, cooldown: 720 },
            windGust: { active: false, timer: 0, cooldown: 720 },
            darkTendrils: { active: false, timer: 0, cooldown: 720 }, // Venom
            razorBats: { active: false, timer: 0, cooldown: 720 }, // Hobgoblin
            clawsOfDarkness: { active: false, timer: 0, cooldown: 720 }, // Prowler
            illusionGas: { active: false, timer: 0, cooldown: 720 }, // Mysterio
            tailWhip: { active: false, timer: 0, cooldown: 720 } // Lizard
        };
        
        let playerSlowed = false;
        let playerSlowTimer = 0;
        
        // Building images
        let buildingImages = [];
        let buildingImagesLoaded = 0;
        
        // Street image
        let streetImage = null;
        let streetImageLoaded = false;
        
        // Villain sprites
        let villainSprites = {
            'Doc Ock': null,
            'Green Goblin': null,
            'Vulture': null,
            'Venom': null,
            'Lizard': null,
            'Mysterio': null,
            'Hobgoblin': null,
            'Prowler': null,
            'Sandman': null
        };
        let villainSpritesLoaded = 0;
        
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
        
        // Load street image
        function loadStreetImage() {
            const streetPath = '/static/Street_6.png';
            const img = new Image();
            img.onload = function() {
                streetImageLoaded = true;
            };
            img.src = streetPath;
            streetImage = img;
        }
        
        // Load taxi image
        let taxiImage = null;
        let taxiImageLoaded = false;
        
        function loadTaxiImage() {
            const taxiPath = '/static/taxi.png';
            const img = new Image();
            img.onload = function() {
                taxiImageLoaded = true;
            };
            img.src = taxiPath;
            taxiImage = img;
        }
        
        // Load web image
        let webImage = null;
        let webImageLoaded = false;
        
        function loadWebImage() {
            const webPath = '/static/webs.png';
            const img = new Image();
            img.onload = function() {
                webImageLoaded = true;
            };
            img.src = webPath;
            webImage = img;
        }
        
        // Load taxi Spider-Man sprite
        let taxiSpiderManSprite = null;
        let taxiSpiderManLoaded = false;
        
        function loadTaxiSpiderManSprite() {
            const taxiSpiderManPath = '/static/spider_man_taxi.png';
            const img = new Image();
            img.onload = function() {
                taxiSpiderManLoaded = true;
            };
            img.src = taxiSpiderManPath;
            taxiSpiderManSprite = img;
        }
        
        // Load swing Spider-Man sprites
        let swingSpiderManSprite1 = null;
        let swingSpiderManSprite2 = null;
        let swingSpiderManLoaded = false;
        
        function loadSwingSpiderManSprites() {
            const swingPath1 = '/static/spider_man_swing.png';
            const swingPath2 = '/static/spider_man_swing_2.png';
            
            const img1 = new Image();
            img1.onload = function() {
                swingSpiderManLoaded = true;
            };
            img1.src = swingPath1;
            swingSpiderManSprite1 = img1;
            
            const img2 = new Image();
            img2.onload = function() {
                swingSpiderManLoaded = true;
            };
            img2.src = swingPath2;
            swingSpiderManSprite2 = img2;
        }
        
        // Load villain sprites
        function loadVillainSprites() {
            const villainPaths = {
                'Doc Ock': '/static/Doc_Oc.png',
                'Green Goblin': '/static/Green_Goblin.png',
                'Vulture': '/static/Vulture.png',
                'Venom': '/static/Venom.png', // Now using actual Venom sprite
                'Lizard': '/static/Lizard.png',
                'Mysterio': '/static/Mysterio.png',
                'Hobgoblin': '/static/Hobgoblin.png',
                'Prowler': '/static/Prowler.png',
                'Sandman': '/static/Sandman.png'
            };
            
            Object.keys(villainPaths).forEach(villainName => {
                const img = new Image();
                img.onload = function() {
                    villainSpritesLoaded++;
                };
                img.src = villainPaths[villainName];
                villainSprites[villainName] = img;
            });
        }
        
        // Initialize villains
        function initVillains() {
            villains = [];
            
            // Create 9 villains for Level 1
            for (let i = 0; i < 9; i++) {
                const spawn = villainSpawns[i];
                const villainType = villainTypes[i];
                
                villains.push({
                    x: spawn.x,
                    y: spawn.y,
                    type: villainType.name,
                    color: villainType.color,
                    speed: villainType.speed,
                    ability: villainType.ability,
                    direction: 'right',
                    moveTimer: 0,
                    abilityTimer: 0,
                    stunned: false,
                    stunnedTimer: 0,
                    targetX: spawn.x,
                    targetY: spawn.y
                });
            }
        }
        
        // Villain AI movement
        function updateVillains() {
            villains.forEach(villain => {
                if (villain.stunned) {
                    villain.stunnedTimer--;
                    if (villain.stunnedTimer <= 0) {
                        villain.stunned = false;
                        // Return to pen
                        villain.x = villainPen.x;
                        villain.y = villainPen.y;
                    }
                    return;
                }
                
                // Move towards target
                villain.moveTimer++;
                if (villain.moveTimer >= Math.floor(60 / villain.speed)) {
                    villain.moveTimer = 0;
                    
                    // Check if reached target
                    if (villain.x === villain.targetX && villain.y === villain.targetY) {
                        setNewTarget(villain);
                    } else {
                        moveTowardsTarget(villain);
                    }
                }
                
                // Update abilities
                villain.abilityTimer++;
                if (villain.abilityTimer >= 720) { // 12 seconds
                    villain.abilityTimer = 0;
                    useVillainAbility(villain);
                }
            });
        }
        
        function setNewTarget(villain) {
            const processedMap = processMazeWithFloodFill(level1Map);
            
            // All villains can move freely - just pick random valid positions
            // Different villains have slight preferences but can go anywhere
            
            if (villain.type === 'Doc Ock') {
                // Doc Ock prefers center area but can go anywhere
                const centerX = Math.floor(processedMap[0].length / 2);
                const centerY = Math.floor(processedMap.length / 2);
                
                if (Math.random() < 0.7) { // 70% chance to target center area
                    villain.targetX = centerX + (Math.random() - 0.5) * 8;
                    villain.targetY = centerY + (Math.random() - 0.5) * 8;
                } else { // 30% chance to go anywhere
                    villain.targetX = Math.floor(Math.random() * processedMap[0].length);
                    villain.targetY = Math.floor(Math.random() * processedMap.length);
                }
            } else if (villain.type === 'Green Goblin') {
                // Green Goblin prefers outer areas but can go anywhere
                if (Math.random() < 0.6) { // 60% chance to target edges
                    const edges = [
                        { x: 1, y: 1 }, { x: processedMap[0].length - 2, y: 1 },
                        { x: 1, y: processedMap.length - 2 }, { x: processedMap[0].length - 2, y: processedMap.length - 2 }
                    ];
                    const target = edges[Math.floor(Math.random() * edges.length)];
                    villain.targetX = target.x;
                    villain.targetY = target.y;
                } else { // 40% chance to go anywhere
                    villain.targetX = Math.floor(Math.random() * processedMap[0].length);
                    villain.targetY = Math.floor(Math.random() * processedMap.length);
                }
            } else {
                // All other villains (Vulture, Venom, Lizard, Mysterio) can go anywhere
                villain.targetX = Math.floor(Math.random() * processedMap[0].length);
                villain.targetY = Math.floor(Math.random() * processedMap.length);
            }
            
            // Ensure target is within bounds and not a wall
            villain.targetX = Math.max(0, Math.min(processedMap[0].length - 1, villain.targetX));
            villain.targetY = Math.max(0, Math.min(processedMap.length - 1, villain.targetY));
            
            // If target is a wall, find a valid position nearby
            if (processedMap[villain.targetY][villain.targetX] === '#') {
                // Search for nearest valid position
                let found = false;
                let searchRadius = 1;
                
                while (!found && searchRadius < Math.max(processedMap.length, processedMap[0].length)) {
                    for (let dy = -searchRadius; dy <= searchRadius; dy++) {
                        for (let dx = -searchRadius; dx <= searchRadius; dx++) {
                            const newX = villain.targetX + dx;
                            const newY = villain.targetY + dy;
                            
                            if (newX >= 0 && newX < processedMap[0].length && 
                                newY >= 0 && newY < processedMap.length && 
                                processedMap[newY][newX] !== '#') {
                                villain.targetX = newX;
                                villain.targetY = newY;
                                found = true;
                                break;
                            }
                        }
                        if (found) break;
                    }
                    searchRadius++;
                }
                
                // If still no valid position found, pick a random valid position
                if (!found) {
                    const validPositions = [];
                    for (let y = 0; y < processedMap.length; y++) {
                        for (let x = 0; x < processedMap[y].length; x++) {
                            if (processedMap[y][x] !== '#') {
                                validPositions.push({x, y});
                            }
                        }
                    }
                    
                    if (validPositions.length > 0) {
                        const randomPos = validPositions[Math.floor(Math.random() * validPositions.length)];
                        villain.targetX = randomPos.x;
                        villain.targetY = randomPos.y;
                    }
                }
            }
        }
        
        function moveTowardsTarget(villain) {
            const processedMap = processMazeWithFloodFill(level1Map);
            
            // Find the best path to target using A* pathfinding
            const path = findPathToTarget(villain.x, villain.y, villain.targetX, villain.targetY, processedMap);
            
            if (path && path.length > 1) {
                // Move to the next step in the path
                const nextStep = path[1]; // path[0] is current position
                
                // Update direction based on movement
                if (nextStep.x < villain.x) {
                    villain.direction = 'left';
                } else if (nextStep.x > villain.x) {
                    villain.direction = 'right';
                }
                
                villain.x = nextStep.x;
                villain.y = nextStep.y;
            } else {
                // No path found or already at target, set new target
                // For Doc Ock, try a simpler fallback movement
                if (villain.type === 'Doc Ock') {
                    // Try simple movement in any valid direction
                    const directions = [[0, -1], [0, 1], [-1, 0], [1, 0]];
                    let moved = false;
                    
                    for (let [dx, dy] of directions) {
                        const newX = villain.x + dx;
                        const newY = villain.y + dy;
                        
                        if (newX >= 0 && newX < processedMap[0].length && 
                            newY >= 0 && newY < processedMap.length && 
                            processedMap[newY][newX] !== '#') {
                            
                            // Update direction based on movement
                            if (dx < 0) {
                                villain.direction = 'left';
                            } else if (dx > 0) {
                                villain.direction = 'right';
                            }
                            
                            villain.x = newX;
                            villain.y = newY;
                            moved = true;
                            break;
                        }
                    }
                    
                    if (!moved) {
                        setNewTarget(villain);
                    }
                } else {
                    setNewTarget(villain);
                }
            }
        }
        
        // A* pathfinding algorithm
        function findPathToTarget(startX, startY, targetX, targetY, map) {
            const openSet = [];
            const closedSet = new Set();
            const cameFrom = new Map();
            const gScore = new Map();
            const fScore = new Map();
            
            const startKey = `${startX},${startY}`;
            const targetKey = `${targetX},${targetY}`;
            
            openSet.push({x: startX, y: startY});
            gScore.set(startKey, 0);
            fScore.set(startKey, heuristic(startX, startY, targetX, targetY));
            
            while (openSet.length > 0) {
                // Find node with lowest fScore
                let currentIndex = 0;
                for (let i = 1; i < openSet.length; i++) {
                    const currentKey = `${openSet[currentIndex].x},${openSet[currentIndex].y}`;
                    const nextKey = `${openSet[i].x},${openSet[i].y}`;
                    if (fScore.get(nextKey) < fScore.get(currentKey)) {
                        currentIndex = i;
                    }
                }
                
                const current = openSet.splice(currentIndex, 1)[0];
                const currentKey = `${current.x},${current.y}`;
                
                if (currentKey === targetKey) {
                    // Path found, reconstruct it
                    return reconstructPath(cameFrom, current);
                }
                
                closedSet.add(currentKey);
                
                // Check all 4 neighbors
                const directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]; // up, down, left, right
                for (let [dx, dy] of directions) {
                    const neighborX = current.x + dx;
                    const neighborY = current.y + dy;
                    const neighborKey = `${neighborX},${neighborY}`;
                    
                    // Check bounds and if it's a wall
                    if (neighborX < 0 || neighborX >= map[0].length || 
                        neighborY < 0 || neighborY >= map.length || 
                        map[neighborY][neighborX] === '#' || 
                        closedSet.has(neighborKey)) {
                        continue;
                    }
                    
                    const tentativeGScore = gScore.get(currentKey) + 1;
                    
                    if (!openSet.some(node => node.x === neighborX && node.y === neighborY)) {
                        openSet.push({x: neighborX, y: neighborY});
                    } else if (tentativeGScore >= gScore.get(neighborKey)) {
                        continue;
                    }
                    
                    cameFrom.set(neighborKey, current);
                    gScore.set(neighborKey, tentativeGScore);
                    fScore.set(neighborKey, tentativeGScore + heuristic(neighborX, neighborY, targetX, targetY));
                }
            }
            
            // No path found
            return null;
        }
        
        function heuristic(x1, y1, x2, y2) {
            // Manhattan distance
            return Math.abs(x1 - x2) + Math.abs(y1 - y2);
        }
        
        function reconstructPath(cameFrom, current) {
            const path = [current];
            let currentKey = `${current.x},${current.y}`;
            
            while (cameFrom.has(currentKey)) {
                current = cameFrom.get(currentKey);
                path.unshift(current);
                currentKey = `${current.x},${current.y}`;
            }
            
            return path;
        }
        
        function useVillainAbility(villain) {
            if (villain.ability === 'alleyBlock') {
                // Doc Ock blocks nearest alley
                villainAbilities.alleyBlock.active = true;
                villainAbilities.alleyBlock.timer = 180; // 3 seconds
            } else if (villain.ability === 'pumpkinBomb') {
                // Green Goblin drops bomb at random intersection
                villainAbilities.pumpkinBomb.active = true;
                villainAbilities.pumpkinBomb.timer = 240; // 4 seconds
            } else if (villain.ability === 'windGust') {
                // Vulture creates wind gust
                villainAbilities.windGust.active = true;
                villainAbilities.windGust.timer = 180; // 3 seconds
                playerSlowed = true;
                playerSlowTimer = 180; // 3 seconds
            }
        }
        
        // Initialize level 1 data
        function initLevel1() {
            // Process the maze with flood-fill to close off enclosed spaces
            const processedMap = processMazeWithFloodFill(level1Map);
            
            dustPositions = [];
            webShooterPositions = [];
            taxiStopPositions = [];
            
            for (let y = 0; y < processedMap.length; y++) {
                for (let x = 0; x < processedMap[y].length; x++) {
                    const tile = processedMap[y][x];
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
            loadStreetImage();
            loadTaxiImage();
            loadWebImage();
            loadTaxiSpiderManSprite();
            loadSwingSpiderManSprites();
            loadVillainSprites();
            
            // Initialize villains
            initVillains();
            
            // Initialize background music
            initBackgroundMusic();
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
        
        // Background music functions
        function initBackgroundMusic() {
            const bgMusic = document.getElementById('backgroundMusic');
            if (bgMusic) {
                bgMusic.volume = 0.3; // Set volume to 30%
                bgMusic.loop = true;
            }
        }
        
        function startBackgroundMusic() {
            const bgMusic = document.getElementById('backgroundMusic');
            if (bgMusic) {
                bgMusic.play().catch(error => {
                    console.log('Background music autoplay blocked:', error);
                });
            }
        }
        
        function stopBackgroundMusic() {
            const bgMusic = document.getElementById('backgroundMusic');
            if (bgMusic) {
                bgMusic.pause();
                bgMusic.currentTime = 0;
            }
        }

        // Panel navigation
        function showPanel(panelNumber) {
            // Hide all panels including title screen
            document.querySelectorAll('.comic-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
            });

            // Show new panel immediately without page flip effect
            if (panelNumber === 0) {
                document.getElementById('comicPanel0').classList.add('active');
            } else {
                document.getElementById(`comicPanel${panelNumber}`).classList.add('active');
            }
        }

        // Game flow functions
        function startGame() {
            console.log('Start game clicked!');
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
            
            // Calculate optimal tile size to fit screen horizontally
            const maxWidth = window.innerWidth * 0.98; // 98% of screen width for maximum horizontal coverage
            const maxHeight = window.innerHeight * 0.85; // 85% of screen height
            
            const tileSizeX = Math.floor(maxWidth / level1Map[0].length);
            const tileSizeY = Math.floor(maxHeight / level1Map.length);
            const tileSize = Math.min(tileSizeX, tileSizeY, 45); // Cap at 45px, minimum of 20px for better fit
            
            // Set canvas size to fit the map with space above for HUD
            canvas.width = level1Map[0].length * tileSize;
            canvas.height = level1Map.length * tileSize + 80; // Add 80px for HUD above
            
            // Store tile size globally for rendering
            window.gameTileSize = tileSize;
            
            // Start game loop
            gameLoop = setInterval(updateGame, 1000/60); // 60 FPS
            
            // Add keyboard controls
            document.addEventListener('keydown', handleKeyPress);
            
            // Start background music
            startBackgroundMusic();
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
            
            // Update villain abilities
            Object.keys(villainAbilities).forEach(ability => {
                if (villainAbilities[ability].active) {
                    villainAbilities[ability].timer--;
                    if (villainAbilities[ability].timer <= 0) {
                        villainAbilities[ability].active = false;
                    }
                }
            });
            
            // Update player slow effect
            if (playerSlowed) {
                playerSlowTimer--;
                if (playerSlowTimer <= 0) {
                    playerSlowed = false;
                }
            }
            
            // Update villains
            updateVillains();
            
            // Update taxi ride
            updateTaxiRide();
            
            // Check villain collision
            checkVillainCollision();
            
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
                showGameOverScreen(); // Use game over screen when all lives are lost
                return;
            }
            
            renderGame();
        }
        
        function renderGame() {
            if (!ctx) return;
            
            const tileSize = window.gameTileSize || 30;
            
            // Clear canvas
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw HUD above the game board
            drawHUD();
            
            // Draw background (East Village pixel art) - only once
            if (!window.backgroundImage) {
                window.backgroundImage = new Image();
                window.backgroundImage.onload = function() {
                    // Background is loaded, but we'll draw it in drawMapElements
                };
                window.backgroundImage.src = '/static/East_Village_Pixel_Scape.png';
            }
            
            // Draw map elements (which will handle background drawing)
            drawMapElements();
        }
        
        function drawMapElements() {
            const tileSize = window.gameTileSize || 30;
            const hudHeight = 80; // Height of HUD area
            
            // Draw background first (only if loaded) - offset by HUD height
            if (window.backgroundImage && window.backgroundImage.complete) {
                ctx.drawImage(window.backgroundImage, 0, hudHeight, canvas.width, canvas.height - hudHeight);
            }
            
            // Get processed map
            const processedMap = processMazeWithFloodFill(level1Map);
            
            // Draw map elements
            for (let y = 0; y < processedMap.length; y++) {
                for (let x = 0; x < processedMap[y].length; x++) {
                    const tile = processedMap[y][x];
                    const drawX = x * tileSize;
                    const drawY = y * tileSize + hudHeight; // Offset by HUD height
                    
                    // Draw street background for all non-building tiles
                    if (tile !== '#') {
                        if (streetImageLoaded && streetImage) {
                            ctx.drawImage(streetImage, drawX, drawY, tileSize, tileSize);
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
                        // Draw web shooter with image
                        const webShooterExists = webShooterPositions.some(ws => ws.x === x && ws.y === y);
                        if (webShooterExists) {
                            if (webImageLoaded && webImage) {
                                ctx.drawImage(webImage, drawX, drawY, tileSize, tileSize);
                            } else {
                                // Fallback to blue circle while image loads
                                ctx.fillStyle = '#00bfff';
                                ctx.beginPath();
                                ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 8, 0, 2 * Math.PI);
                                ctx.fill();
                                ctx.strokeStyle = '#ffffff';
                                ctx.lineWidth = 2;
                                ctx.stroke();
                            }
                        }
                    } else if (tile === 'T') {
                        // Draw taxi stop with image (only if not riding and taxi still exists)
                        if (!isRidingTaxi) {
                            // Check if this taxi position still exists in taxiStopPositions
                            const taxiExists = taxiStopPositions.some(taxi => taxi.x === x && taxi.y === y);
                            if (taxiExists) {
                                if (taxiImageLoaded && taxiImage) {
                                    ctx.drawImage(taxiImage, drawX, drawY, tileSize, tileSize);
                                } else {
                                    // Fallback to yellow square while image loads
                                    ctx.fillStyle = '#ffff00';
                                    ctx.fillRect(drawX + 2, drawY + 2, tileSize - 4, tileSize - 4);
                                    ctx.strokeStyle = '#000';
                                    ctx.lineWidth = 1;
                                    ctx.strokeRect(drawX + 2, drawY + 2, tileSize - 4, tileSize - 4);
                                }
                            }
                        }
                    }
                }
            }
            
            // Draw villains
            drawVillains();
            
            // Draw taxi if riding
            if (isRidingTaxi && taxiImageLoaded && taxiImage) {
                const drawTaxiX = taxiX * tileSize;
                const drawTaxiY = taxiY * tileSize + hudHeight;
                ctx.drawImage(taxiImage, drawTaxiX, drawTaxiY, tileSize, tileSize);
            }
            
            // Draw player (Spider-Man sprite) - use cached image
            if (!window.playerSprite) {
                window.playerSprite = new Image();
                window.playerSprite.onload = function() {
                    // Image loaded, will be drawn next frame
                };
                window.playerSprite.src = '/static/Spider-man_Running_Sprite.png';
            }
            
            // Choose which Spider-Man sprite to use
            let currentPlayerSprite = window.playerSprite;
            if (isRidingTaxi && taxiSpiderManLoaded && taxiSpiderManSprite) {
                currentPlayerSprite = taxiSpiderManSprite;
            } else if (webShooterActive && swingSpiderManLoaded && swingSpiderManSprite1 && swingSpiderManSprite2) {
                // Check if player moved to a new square
                if (playerX !== lastPlayerX || playerY !== lastPlayerY) {
                    swingAnimationCounter++;
                    lastPlayerX = playerX;
                    lastPlayerY = playerY;
                }
                
                // Alternate between swing sprites based on movement
                if (swingAnimationCounter % 2 === 0) {
                    currentPlayerSprite = swingSpiderManSprite1;
                } else {
                    currentPlayerSprite = swingSpiderManSprite2;
                }
            }
            
            if (currentPlayerSprite && currentPlayerSprite.complete) {
                ctx.save();
                if (playerDirection === 'left') {
                    // Flip horizontally when moving left
                    ctx.scale(-1, 1);
                    ctx.drawImage(currentPlayerSprite, -(playerX * tileSize + 1 + tileSize - 2), playerY * tileSize + 1 + hudHeight, tileSize - 2, tileSize - 2);
                } else {
                    // Normal drawing for other directions
                    ctx.drawImage(currentPlayerSprite, playerX * tileSize + 1, playerY * tileSize + 1 + hudHeight, tileSize - 2, tileSize - 2);
                }
                ctx.restore();
                
                // Draw floating "YOU" text above Spider-Man
                const textX = playerX * tileSize + tileSize / 2;
                const textY = playerY * tileSize - 10 + hudHeight;
                
                // Glow effect
                ctx.shadowColor = '#00bfff';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 0;
                
                // Main text
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 16px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('YOU', textX, textY);
                
                // Reset shadow
                ctx.shadowBlur = 0;
            }
        }
        
        function drawVillains() {
            const tileSize = window.gameTileSize || 30;
            const hudHeight = 80; // Height of HUD area
            

            
            villains.forEach(villain => {
                // Get the villain sprite
                const villainSprite = villainSprites[villain.type];
                
                // Check if villain is using special power and set glow color
                let glowColor = null;
                if (villain.type === 'Doc Ock' && villainAbilities.alleyBlock.active) {
                    glowColor = '#ff0000'; // Red glow for Doc Ock
                } else if (villain.type === 'Green Goblin' && villainAbilities.pumpkinBomb.active) {
                    glowColor = '#ff8800'; // Orange glow for Green Goblin
                } else if (villain.type === 'Vulture' && villainAbilities.windGust.active) {
                    glowColor = '#00ffff'; // Cyan glow for Vulture
                } else if (villain.type === 'Venom' && villainAbilities.darkTendrils.active) {
                    glowColor = '#800080'; // Purple glow for Venom
                } else if (villain.type === 'Hobgoblin' && villainAbilities.razorBats.active) {
                    glowColor = '#ff6600'; // Dark orange glow for Hobgoblin
                } else if (villain.type === 'Prowler' && villainAbilities.clawsOfDarkness.active) {
                    glowColor = '#000080'; // Dark blue glow for Prowler
                } else if (villain.type === 'Mysterio' && villainAbilities.illusionGas.active) {
                    glowColor = '#00ff00'; // Green glow for Mysterio
                } else if (villain.type === 'Sandman' && villainAbilities.tailWhip.active) {
                    glowColor = '#008000'; // Dark green glow for Lizard
                }
                
                if (villainSprite && villainSpritesLoaded >= 9) {
                    // Draw villain sprite
                    if (villain.stunned) {
                        // Draw stunned villain (flashing)
                        if (Math.floor(Date.now() / 100) % 2 === 0) {
                            ctx.globalAlpha = 0.5; // Make it semi-transparent when stunned
                        } else {
                            ctx.globalAlpha = 1.0;
                        }
                    } else {
                        ctx.globalAlpha = 1.0;
                    }
                    
                    ctx.save();
                    
                    // Add glow effect if villain is using special power
                    if (glowColor) {
                        ctx.shadowColor = glowColor;
                        ctx.shadowBlur = 15;
                        ctx.shadowOffsetX = 0;
                        ctx.shadowOffsetY = 0;
                    }
                    
                    if (villain.direction === 'left') {
                        // Flip horizontally when moving left
                        ctx.scale(-1, 1);
                        ctx.drawImage(villainSprite, -(villain.x * tileSize + 0.5 + tileSize - 1), villain.y * tileSize + 0.5 + hudHeight, tileSize - 1, tileSize - 1);
                    } else {
                        // Normal drawing for other directions
                        ctx.drawImage(villainSprite, villain.x * tileSize + 0.5, villain.y * tileSize + 0.5 + hudHeight, tileSize - 1, tileSize - 1);
                    }
                    ctx.restore();
                    ctx.globalAlpha = 1.0; // Reset alpha
                } else {
                    // Fallback to colored block if sprite not loaded
                    ctx.save();
                    
                    // Add glow effect if villain is using special power
                    if (glowColor) {
                        ctx.shadowColor = glowColor;
                        ctx.shadowBlur = 15;
                        ctx.shadowOffsetX = 0;
                        ctx.shadowOffsetY = 0;
                    }
                    
                    if (villain.stunned) {
                        // Draw stunned villain (flashing)
                        if (Math.floor(Date.now() / 100) % 2 === 0) {
                            ctx.fillStyle = '#ffffff';
                        } else {
                            ctx.fillStyle = villain.color;
                        }
                    } else {
                        ctx.fillStyle = villain.color;
                    }
                    
                    ctx.fillRect(villain.x * tileSize + 0.5, villain.y * tileSize + 0.5 + hudHeight, tileSize - 1, tileSize - 1);
                    ctx.restore();
                }
                
                // Draw villain name
                ctx.fillStyle = '#ffffff';
                ctx.font = `${Math.max(8, tileSize * 0.3)}px Courier New`;
                ctx.textAlign = 'center';
                ctx.fillText(villain.type, villain.x * tileSize + tileSize/2, villain.y * tileSize - 5 + hudHeight);
            });
        }
        
        function checkVillainCollision() {
            // Spider-Man is immune to villains when riding a taxi
            if (isRidingTaxi) return;
            
            villains.forEach(villain => {
                if (villain.x === playerX && villain.y === playerY) {
                    if (webShooterActive) {
                        // Stun villain
                        villain.stunned = true;
                        villain.stunnedTimer = 180; // 3 seconds
                        score += 100;
                    } else {
                        // Player loses life
                        lives--;
                        playerX = 13; // Reset to spawn
                        playerY = 12;
                    }
                }
            });
        }
        
        function drawHUD() {
            const tileSize = window.gameTileSize || 30;
            const hudY = 35; // Increased position to prevent cutoff
            const fontSize = Math.min(20, Math.max(14, tileSize * 0.4)); // Capped font size
            
            // Lives
            ctx.fillStyle = '#ffffff';
            ctx.font = `${fontSize}px Courier New`;
            ctx.fillText(`Lives: ${lives}`, tileSize * 1.5, hudY);
            
            // Score
            ctx.fillText(`Score: ${score}`, canvas.width/2 - tileSize * 2.5, hudY);
            
            // Level
            ctx.fillText('Level 1: East Village', canvas.width - tileSize * 10, hudY);
            
            // Villain ability status
            const statusY = hudY + fontSize + 8;
            ctx.font = `${Math.min(16, Math.max(10, tileSize * 0.3))}px Courier New`;
            
            if (villainAbilities.alleyBlock.active) {
                ctx.fillStyle = '#ff0000';
                ctx.fillText('Doc Ock: Alley Blocked!', tileSize * 0.5, statusY);
            }
            if (villainAbilities.pumpkinBomb.active) {
                ctx.fillStyle = '#ff8800';
                ctx.fillText('Green Goblin: Pumpkin Bomb!', canvas.width/2 - tileSize * 2.5, statusY);
            }
            if (villainAbilities.windGust.active || playerSlowed) {
                ctx.fillStyle = '#00ffff';
                ctx.fillText('Vulture: Wind Gust!', canvas.width - tileSize * 10, statusY);
            }
            if (villainAbilities.darkTendrils.active) {
                ctx.fillStyle = '#800080';
                ctx.fillText('Venom: Dark Tendrils!', tileSize * 0.5, statusY + 20);
            }
            if (villainAbilities.razorBats.active) {
                ctx.fillStyle = '#ff6600';
                ctx.fillText('Hobgoblin: Razor Bats!', canvas.width/2 - tileSize * 2.5, statusY + 20);
            }
            if (villainAbilities.clawsOfDarkness.active) {
                ctx.fillStyle = '#000080';
                ctx.fillText('Prowler: Claws of Darkness!', canvas.width - tileSize * 10, statusY + 20);
            }
            if (villainAbilities.illusionGas.active) {
                ctx.fillStyle = '#00ff00';
                ctx.fillText('Mysterio: Illusion Gas!', tileSize * 0.5, statusY + 40);
            }
            if (villainAbilities.tailWhip.active) {
                ctx.fillStyle = '#008000';
                ctx.fillText('Lizard: Tail Whip!', canvas.width/2 - tileSize * 2.5, statusY + 40);
            }
            if (webShooterActive) {
                ctx.fillStyle = '#00bfff';
                ctx.fillText('Web Shooter Active!', canvas.width/2, statusY + 60);
            }
        }
        
        function handleKeyPress(event) {
            if (level1State !== 'gameplay') return;
            
            // Don't allow movement while riding taxi
            if (isRidingTaxi) return;
            
            const processedMap = processMazeWithFloodFill(level1Map);
            const newX = playerX;
            const newY = playerY;
            
            switch(event.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (newY > 0 && processedMap[newY - 1][newX] !== '#') {
                        playerY = newY - 1;
                        playerDirection = 'up';
                    }
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    if (newY < processedMap.length - 1 && processedMap[newY + 1][newX] !== '#') {
                        playerY = newY + 1;
                        playerDirection = 'down';
                    }
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (newX > 0 && processedMap[newY][newX - 1] !== '#') {
                        playerX = newX - 1;
                        playerDirection = 'left';
                    } else if (newX === 0 && newY === 13) {
                        // Wrap-around tunnel: left edge to right edge at row 14
                        playerX = processedMap[0].length - 1;
                        playerDirection = 'left';
                    } else if (newX === 0 && newY === 2) {
                        // Wrap-around tunnel: left edge row 3 to right edge row 2
                        playerX = processedMap[0].length - 1;
                        playerY = 1;
                        playerDirection = 'left';
                    }
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (newX < processedMap[0].length - 1 && processedMap[newY][newX + 1] !== '#') {
                        playerX = newX + 1;
                        playerDirection = 'right';
                    } else if (newX === processedMap[0].length - 1 && newY === 13) {
                        // Wrap-around tunnel: right edge to left edge at row 14
                        playerX = 0;
                        playerDirection = 'right';
                    } else if (newX === processedMap[0].length - 1 && newY === 1) {
                        // Wrap-around tunnel: right edge row 2 to left edge row 3
                        playerX = 0;
                        playerY = 2;
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
            if (taxiIndex !== -1 && !isRidingTaxi && !webShooterActive) {
                // Start taxi ride (only if web shooter is not active)
                isRidingTaxi = true;
                taxiX = playerX;
                taxiY = playerY;
                taxiDirection = playerDirection;
                taxiMoveTimer = 0;
                score += 25;
                
                // Remove taxi from collection list
                taxiStopPositions.splice(taxiIndex, 1);
            }
        }
        
        function updateTaxiRide() {
            if (!isRidingTaxi) return;
            
            taxiMoveTimer += taxiSpeed;
            
            if (taxiMoveTimer >= 1) {
                taxiMoveTimer = 0;
                
                const processedMap = processMazeWithFloodFill(level1Map);
                let newTaxiX = taxiX;
                let newTaxiY = taxiY;
                
                // Move taxi in its direction
                switch (taxiDirection) {
                    case 'up':
                        newTaxiY = taxiY - 1;
                        break;
                    case 'down':
                        newTaxiY = taxiY + 1;
                        break;
                    case 'left':
                        newTaxiX = taxiX - 1;
                        break;
                    case 'right':
                        newTaxiX = taxiX + 1;
                        break;
                }
                
                // Check if taxi can move
                if (newTaxiX >= 0 && newTaxiX < processedMap[0].length &&
                    newTaxiY >= 0 && newTaxiY < processedMap.length &&
                    processedMap[newTaxiY][newTaxiX] !== '#') {
                    
                    // Check if taxi would hit column 1 or 25 (stop at edges)
                    if (newTaxiX === 0 || newTaxiX === processedMap[0].length - 1) {
                        // Taxi hit column 1 or 25, end the ride
                        isRidingTaxi = false;
                        return;
                    }
                    
                    // Update taxi position
                    taxiX = newTaxiX;
                    taxiY = newTaxiY;
                    
                    // Move player with taxi
                    playerX = taxiX;
                    playerY = taxiY;
                    
                    // Check for dust collection while riding taxi
                    checkDustCollection();
                    checkWebShooterCollection();
                } else {
                    // Taxi hit a wall or edge, end the ride
                    isRidingTaxi = false;
                }
            }
        }
        
        // Win/Loss Cut Scene System
        let winLossState = 'none'; // none, win, lose, gameOver
        let currentQuip = '';
        let quipTimer = 0;
        
        // Win quips for different levels
        const winQuips = {
            'level1': "Guess sweeping the streets really is my job…",
            'level2': "Bright lights, cleaner streets — you're welcome, New York!"
        };
        
        // Loss quips (randomized)
        const lossQuips = [
            "Man… I really dropped the ball this time.",
            "Note to self: dodging villains is harder than it looks.",
            "Remind me to never tell Strange I messed this up…",
            "Even heroes have bad days."
        ];
        
        function showWinScreen() {
            currentState = 'win';
            winLossState = 'win';
            currentQuip = winQuips['level1']; // For now, hardcoded to level 1
            quipTimer = 0;
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide all panels and show win cutscene
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('winCutscene').classList.add('active');
            document.getElementById('winQuip').textContent = currentQuip;
        }
        
        function showLoseScreen() {
            currentState = 'lose';
            winLossState = 'lose';
            currentQuip = lossQuips[Math.floor(Math.random() * lossQuips.length)];
            quipTimer = 0;
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide all panels and show lose cutscene
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('loseCutscene').classList.add('active');
            document.getElementById('loseQuip').textContent = currentQuip;
        }
        
        function showGameOverScreen() {
            currentState = 'gameOver';
            winLossState = 'gameOver';
            currentQuip = lossQuips[Math.floor(Math.random() * lossQuips.length)];
            quipTimer = 0;
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide all panels and show game over cutscene
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('gameOverCutscene').classList.add('active');
            document.getElementById('gameOverQuip').textContent = currentQuip;
        }
        
        // Cut scene button functions
        function returnToTitle() {
            // Hide all cutscenes
            document.querySelectorAll('.win-loss-cutscene').forEach(cutscene => cutscene.classList.remove('active'));
            // Hide all comic panels
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            // Show title screen
            document.getElementById('titleScreen').classList.add('active');
            currentState = 'title';
            currentPanel = 0;
        }
        
        function retryLevel() {
            // Hide lose cutscene
            document.getElementById('loseCutscene').classList.remove('active');
            // Reset level and restart
            resetLevel();
            currentState = 'gameplay';
            startLevel1();
        }
        
        function retryGame() {
            // Hide game over cutscene
            document.getElementById('gameOverCutscene').classList.remove('active');
            // Reset everything and restart from level 1
            resetGame();
            currentState = 'gameplay';
            startLevel1();
        }
        
        function resetLevel() {
            // Reset level-specific variables
            playerX = 13;
            playerY = 12;
            score = 0;
            lives = 5;
            dustCollected = 0;
            webShooterActive = false;
            webShooterTimer = 0;
            level1State = 'intro';
            
            // Reset taxi riding variables
            isRidingTaxi = false;
            taxiX = 0;
            taxiY = 0;
            taxiDirection = 'right';
            taxiMoveTimer = 0;
            
            // Reset swing animation
            swingAnimationCounter = 0;
            lastPlayerX = 13;
            lastPlayerY = 12;
        }
        
        function resetGame() {
            // Reset all game variables
            resetLevel();
            currentState = 'title';
            currentPanel = 0;
        }

        // Handle window resize
        window.addEventListener('resize', function() {
            if (level1State === 'gameplay' && canvas) {
                // Recalculate tile size and canvas dimensions
                const maxWidth = window.innerWidth * 0.98;
                const maxHeight = window.innerHeight * 0.85;
                
                const tileSizeX = Math.floor(maxWidth / level1Map[0].length);
                const tileSizeY = Math.floor(maxHeight / level1Map.length);
                const tileSize = Math.min(tileSizeX, tileSizeY, 45);
                
                canvas.width = level1Map[0].length * tileSize;
                canvas.height = level1Map.length * tileSize;
                window.gameTileSize = tileSize;
            }
        });

        // Event listeners
        document.addEventListener('click', function(e) {
            // Don't handle clicks on buttons - let button event listeners handle them
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                return;
            }
            
            console.log('Click detected, currentState:', currentState);
            if (currentState === 'title') {
                startGame();
            } else if (currentState === 'comic') {
                nextPanel();
            } else if (currentState === 'gameplay') {
                // Skip splash screen on click
                if (level1State === 'splash') {
                    level1State = 'gameplay';
                    initGameplay();
                }
            } else if (currentState === 'win' || currentState === 'lose' || currentState === 'gameOver') {
                // Don't handle clicks for cut scenes - let buttons handle them
                return;
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
        
        // Add event listener for start button
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up start button...');
            const startButton = document.getElementById('startButton');
            if (startButton) {
                console.log('Start button found, adding click listener...');
                startButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Start button clicked via event listener');
                    startGame();
                });
            } else {
                console.error('Start button not found!');
            }
        });
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
