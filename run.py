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
            background: url('/static/New York Comic.webp') no-repeat center center;
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

        .victory-panel {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: url('/static/Times%20Square%203.png') no-repeat center center;
            background-size: cover;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1100; /* Higher than win cutscene */
            cursor: pointer; /* Make it clear it's clickable */
        }

        .victory-panel.active {
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

        .spider-man-victory-scene {
            width: 300px;
            height: 300px;
            margin: 20px auto;
            background: url('/static/Spider-man%20victory%20scene%201.png') no-repeat center center;
            background-size: contain;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            border: 4px solid #000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .dr-strange-times-square {
            width: 300px;
            height: 300px;
            margin: 20px auto;
            background: url('/static/Dr.%20Strange%20Times%20Square.png') no-repeat center center;
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

        .spider-run-logo {
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 8px rgba(0, 191, 255, 0.5));
            animation: logoGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes logoGlow {
            0% { filter: drop-shadow(0 4px 8px rgba(0, 191, 255, 0.5)); }
            100% { filter: drop-shadow(0 8px 16px rgba(0, 191, 255, 0.8)); }
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
        

        
        .button-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            margin-top: 20px;
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
            z-index: -1;
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
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 15px solid #000;
        }
        
        .quip-bubble::after {
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
        
        .cutscene-buttons {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 20px;
            position: relative;
            z-index: 10;
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
            position: relative;
            z-index: 10;
            pointer-events: auto;
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
        
        .cutscene-button.continue {
            background: #28a745;
        }
        
        .cutscene-button.continue:hover {
            background: #218838;
        }
        
        .click-prompt {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }
        
        .click-anywhere-prompt {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            animation: pulse 2s infinite;
            pointer-events: none; /* Ensure clicks pass through to parent */
        }
    </style>
</head>
<body>
    <div class="game-container">
        <!-- Title Screen -->
        <div id="titleScreen" class="comic-panel active">
            <div class="title-screen">
                <div class="spider-run-logo">
                    <img src="/static/spider_run_official_logo.png" alt="SPIDER-RUN" style="width: 600px; height: auto; max-width: 100%;">
                </div>
                
                <!-- Instructions Section -->
                <div class="instructions">
                    <h3>GAME INSTRUCTIONS</h3>
                    <ul>
                        <li>Use ARROW KEYS to move Spider-Man</li>
                        <li>Collect all SPACE DUST to win</li>
                        <li>Avoid ENEMIES or use WEB-SLINGERS</li>
                        <li>You have 5 LIVES per level</li>
                        <li>TAXIS will move you double time</li>
                        <li>WEB SHOOTERS stun villains and give bonus points</li>
                    </ul>
                </div>
                
                <div class="button-container">
                    <button class="menu-button" id="startButton">PRESS ANYWHERE TO BEGIN</button>
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

        <!-- Post-Level 1 Victory Comic Panels -->
        <div id="victoryPanel0" class="victory-panel">
            <div class="panel-content">
                <div class="dr-strange-times-square"></div>
                <div class="speech-bubble">
                    Excellent work, Spider-Man. The East Village is safe — for now.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="victoryPanel1" class="victory-panel">
            <div class="panel-content">
                <div class="spider-man-victory-scene"></div>
                <div class="speech-bubble">
                    Glad I could help. Got any other cosmic chores for me to run while I'm at it?
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="victoryPanel2" class="victory-panel">
            <div class="panel-content">
                <div class="dr-strange-times-square"></div>
                <div class="speech-bubble">
                    The dust has spread to Times Square. You must head there next — before chaos erupts.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="victoryPanel3" class="victory-panel">
            <div class="panel-content">
                <div class="spider-man-victory-scene"></div>
                <div class="speech-bubble">
                    I'll try... but I'm not making any promises about the chaos part.
                </div>
                <div class="click-prompt">Click to continue</div>
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
        
        <!-- Win/Loss Cut Scenes (win cut scene removed) -->
        
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
        let currentVictoryPanel = 0;
        const totalVictoryPanels = 4;
        
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
        
        // Level 2 game variables
        let level2State = 'intro'; // intro, splash, gameplay, win, lose
        let currentLevel = 1; // Track current level
        
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
        
        // Level 2 map data - Times Square layout (27x28) based on design documents
        const level2Map = [
            "##############################",
            "#W...........####...........W#",
            "#.####.###...####...###.####.#",
            "##.#....#.#...##...#.#....#.##",
            "#.....##....######....##.....#",
            "####..###..##....##..###..####",
            "#########..###--###..#########",
            "#########..#VVVVVV#..#########",
            "#########..########..#########",
            "####..###..##..S.##..###..####",
            "#.....##....######....##.....#",
            "##.#....#.#...##...#.#....#.##",
            "#.####.###...####...###.####.#",
            "#W...........####...........W#",
            "##############################"
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
            { name: 'Venom', color: '#000000', speed: 1.1, ability: 'windGust' }
        ];
        
        // Villain state
        let villainAbilities = {
            alleyBlock: { active: false, timer: 0, cooldown: 720 }, // 12 seconds at 60fps
            pumpkinBomb: { active: false, timer: 0, cooldown: 720 },
            windGust: { active: false, timer: 0, cooldown: 720 },
            darkTendrils: { active: false, timer: 0, cooldown: 720 } // Venom
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
            'Venom': null
        };
        let villainSpritesLoaded = 0;
        
        // Load building images
        function loadBuildingImages() {
            // Choose building paths based on current level
            let buildingPaths;
            if (currentLevel === 1) {
                buildingPaths = [
                    '/static/Building_1.png',
                    '/static/Building_2.png',
                    '/static/Building_3.png',
                    '/static/Building_4.png',
                    '/static/Building_5.png',
                    '/static/Building_6.png'
                ];
            } else {
                // Level 2: Use Times Building images
                buildingPaths = [
                    '/static/Times_Building_1.png',
                    '/static/Times_Building_2.png',
                    '/static/Times_Building_3.png',
                    '/static/Times_Building_4.png',
                    '/static/Times_Building_5.png',
                    '/static/Times_Building_6.png',
                    '/static/Times_Building_7.png',
                    '/static/Times_Building_8.png'
                ];
            }
            
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
            // Choose street path based on current level
            let streetPath;
            if (currentLevel === 1) {
                streetPath = '/static/Street_6.png';
            } else {
                // Level 2: Use New Street image
                streetPath = '/static/New_Street.png';
            }
            
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
                'Venom': '/static/Venom.png' // Now using actual Venom sprite
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
            
            // Create 4 villains for Level 1
            for (let i = 0; i < 4; i++) {
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
            
            if (villain.type === 'Green Goblin') {
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
                // All other villains (Doc Ock, Vulture, Venom) can go anywhere
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
                setNewTarget(villain);
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
        
        // Initialize level 2 data
        function initLevel2() {
            console.log('=== initLevel2() called ===');
            // Process the maze with flood-fill to close off enclosed spaces
            const processedMap = processMazeWithFloodFill(level2Map);
            
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
                        // In Level 2, T represents Dimensional Fragments, not taxi stops
                        // For now, treat them as collectible items like dust
                        dustPositions.push({x, y});
                    }
                }
            }
            totalDust = dustPositions.length;
            console.log('Level 2 initialized with', totalDust, 'collectible items');
            
            // Load building images
            loadBuildingImages();
            loadStreetImage();
            loadTaxiImage();
            loadWebImage();
            loadTaxiSpiderManSprite();
            loadSwingSpiderManSprites();
            loadVillainSprites();
            
            // Initialize villains (will be added later)
            // initVillains();
            
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
            console.log('=== showPanel() called with panelNumber:', panelNumber, '===');
            // Hide all panels including title screen
            document.querySelectorAll('.comic-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
            });

            // Show new panel immediately without page flip effect
            if (panelNumber === 0) {
                const panel0 = document.getElementById('comicPanel0');
                console.log('Showing comicPanel0:', panel0);
                panel0.classList.add('active');
            } else {
                const panel = document.getElementById(`comicPanel${panelNumber}`);
                console.log('Showing comicPanel' + panelNumber + ':', panel);
                panel.classList.add('active');
            }
            console.log('=== showPanel() completed ===');
        }

        // Game flow functions
        function startGame() {
            console.log('=== startGame() function called ===');
            console.log('Current state before:', currentState);
            playClickSound();
            currentState = 'comic';
            currentPanel = 0;
            console.log('Current state after:', currentState);
            console.log('Current panel:', currentPanel);
            showPanel(0);
            console.log('=== startGame() function completed ===');
        }
        
        function skipToVictoryComic() {
            console.log('=== skipToVictoryComic() function called ===');
            console.log('Current state before:', currentState);
            playClickSound();
            
            // Hide title screen explicitly
            const titleScreen = document.getElementById('titleScreen');
            console.log('Hiding title screen:', titleScreen);
            titleScreen.classList.remove('active');
            
            // Hide all comic panels
            document.querySelectorAll('.comic-panel, .victory-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            
            currentState = 'victoryComic';
            currentVictoryPanel = 0;
            console.log('Current state after:', currentState);
            console.log('Current victory panel:', currentVictoryPanel);
            showVictoryPanel(0);
            console.log('=== skipToVictoryComic() function completed ===');
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
        
        function showVictoryPanel(panelNumber) {
            console.log('🔥🔥🔥 === showVictoryPanel() called with panel:', panelNumber, '=== 🔥🔥🔥');
            console.log('🔥 Current state:', currentState);
            console.log('🔥 Current victory panel:', currentVictoryPanel);
            
            // Hide all panels including title screen
            console.log('🔥 Hiding all panels...');
            const allPanels = document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen');
            console.log('🔥 Found panels to hide:', allPanels.length);
            allPanels.forEach((panel, index) => {
                console.log(`🔥 Hiding panel ${index}:`, panel.id || panel.className);
                panel.classList.remove('active');
            });

            // Show new victory panel
            const targetPanel = document.getElementById(`victoryPanel${panelNumber}`);
            console.log('🔥 Target victory panel element:', targetPanel);
            console.log('🔥 Target panel ID:', `victoryPanel${panelNumber}`);
            
            if (targetPanel) {
                console.log('🔥 Adding active class to victory panel...');
                targetPanel.classList.add('active');
                console.log('🔥 Victory panel now has active class:', targetPanel.classList.contains('active'));
                
                // FORCE show the victory panel with explicit styles
                targetPanel.style.display = 'flex';
                targetPanel.style.zIndex = '9999';
                targetPanel.style.position = 'fixed';
                targetPanel.style.top = '0';
                targetPanel.style.left = '0';
                targetPanel.style.width = '100vw';
                targetPanel.style.height = '100vh';
                targetPanel.style.visibility = 'visible';
                targetPanel.style.opacity = '1';
                
                console.log('🔥 Victory panel styles FORCE-applied with maximum priority');
                console.log('🔥 Panel display after force:', getComputedStyle(targetPanel).display);
                console.log('🔥 Panel visibility after force:', getComputedStyle(targetPanel).visibility);
                console.log('🔥 Panel z-index after force:', getComputedStyle(targetPanel).zIndex);
                
                // Add click event listener to this victory panel
                console.log('🔥 Adding click event listener to victory panel...');
                targetPanel.addEventListener('click', function(e) {
                    console.log('🔥🔥🔥 Victory panel clicked!');
                    e.preventDefault();
                    e.stopPropagation();
                    nextVictoryPanel();
                });
                
                // Double-check that title screen is still hidden
                const titleScreen = document.getElementById('titleScreen');
                if (titleScreen && (titleScreen.classList.contains('active') || getComputedStyle(titleScreen).display !== 'none')) {
                    console.error('🔥 WARNING: Title screen is still visible! Force hiding it again...');
                    titleScreen.classList.remove('active');
                    titleScreen.style.display = 'none';
                }
            } else {
                console.error('🔥 ERROR: Target victory panel not found!');
                alert(`ERROR: Victory panel victoryPanel${panelNumber} not found!`);
            }
        }
        
        function nextVictoryPanel() {
            console.log('🔥🔥🔥 === nextVictoryPanel() called === 🔥🔥🔥');
            console.log('🔥 Current state:', currentState);
            console.log('🔥 Current victory panel:', currentVictoryPanel);
            console.log('🔥 Total victory panels:', totalVictoryPanels);
            console.log('🔥 Current level:', currentLevel);
            console.log('🔥 Condition check: currentVictoryPanel >= totalVictoryPanels - 1:', currentVictoryPanel >= totalVictoryPanels - 1);
            
            // Check if we're on the last panel (panel 3 of 4)
            if (currentState === 'victoryComic' && currentVictoryPanel < totalVictoryPanels - 1) {
                console.log('🔥🔥🔥 Advancing to next victory panel...');
                currentVictoryPanel++;
                showVictoryPanel(currentVictoryPanel);
            } else if (currentState === 'victoryComic' && currentVictoryPanel >= totalVictoryPanels - 1) {
                console.log('🔥🔥🔥 Last victory panel reached, showing Level 2 splash...');
                console.log('🔥🔥🔥 Panel check: currentVictoryPanel =', currentVictoryPanel, 'totalVictoryPanels =', totalVictoryPanels);
                // End of victory comic, show Level 2 splash screen without resetting anything
                showLevel2Splash();
            } else {
                console.log('🔥🔥🔥 No condition met - currentVictoryPanel:', currentVictoryPanel, 'totalVictoryPanels:', totalVictoryPanels);
                console.log('🔥🔥🔥 State check failed - currentState:', currentState, 'expected: victoryComic');
                // Force advance to Level 2 splash as fallback
                console.log('🔥🔥🔥 FORCE ADVANCING to Level 2 splash as fallback...');
                showLevel2Splash();
            }
        }
        
        function showLevel2Splash() {
            console.log('=== showLevel2Splash() called ===');
            console.log('Current level before splash:', currentLevel);
            
            // Hide all victory panels
            document.querySelectorAll('.victory-panel').forEach(panel => panel.classList.remove('active'));
            
            // Set up for Level 2 but don't reset anything
            currentLevel = 2;
            currentState = 'level2Splash';
            
            // Show Level 2 splash screen on canvas
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas style for comic book look
            canvas.style.display = 'block';
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
            ctx.strokeText('LEVEL 2', canvas.width/2, canvas.height/2 - 50);
            ctx.fillText('LEVEL 2', canvas.width/2, canvas.height/2 - 50);
            
            ctx.font = 'bold 24px Comic Sans MS';
            ctx.strokeText('TIMES SQUARE', canvas.width/2, canvas.height/2);
            ctx.fillText('TIMES SQUARE', canvas.width/2, canvas.height/2);
            
            ctx.font = '16px Comic Sans MS';
            ctx.fillStyle = '#ffffff';
            ctx.fillText('Press SPACE to start', canvas.width/2, canvas.height/2 + 50);
            
            console.log('Level 2 splash screen displayed - NO RESET CALLED');
            
            // Add keyboard listener for starting level 2 gameplay
            document.addEventListener('keydown', function level2Start(event) {
                if (event.code === 'Space' && currentState === 'level2Splash') {
                    document.removeEventListener('keydown', level2Start);
                    startLevel2Gameplay();
                }
            });
        }
        
        function startLevel2Gameplay() {
            console.log('=== startLevel2Gameplay() called ===');
            console.log('Starting Level 2 gameplay...');
            
            // Use the proper Level 2 start function
            startLevel2();
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
        function initLevel1() {
            console.log('=== initLevel1() called ===');
            
            // Reset game state for Level 1
            dustCollected = 0;
            totalDust = 0;
            lives = 3;
            score = 0;
            webShooterActive = false;
            webShooterTimer = 0;
            isRidingTaxi = false;
            winLock = false;
            
            // Reset player position to Level 1 spawn point
            playerX = 13; // Level 1 spawn X
            playerY = 12; // Level 1 spawn Y (just below villain pen)
            
            // Clear all arrays
            dustPositions = [];
            webShooterPositions = [];
            villainPositions = [];
            taxiStopPositions = [];
            villains = []; // Clear villains array
            
            // Initialize Level 1 map elements
            const currentMap = level1Map;
            const processedMap = processMazeWithFloodFill(currentMap);
            
            // Count total dust and place dust pellets
            for (let y = 0; y < processedMap.length; y++) {
                for (let x = 0; x < processedMap[y].length; x++) {
                    const tile = processedMap[y][x];
                    if (tile === '.') {
                        dustPositions.push({x: x, y: y});
                        totalDust++;
                    } else if (tile === 'W') {
                        webShooterPositions.push({x: x, y: y});
                    } else if (tile === 'T') {
                        // In Level 1, T represents Taxi Stops
                        taxiStopPositions.push({x: x, y: y});
                    } else if (tile === 'V') {
                        villainPositions.push({x: x, y: y, type: 'villain'});
                    }
                }
            }
            
            console.log('Level 1 initialized:');
            console.log('- Total dust:', totalDust);
            console.log('- Web shooters:', webShooterPositions.length);
            console.log('- Taxi stops:', taxiStopPositions.length);
            console.log('- Villains:', villainPositions.length);
            console.log('- Player spawn:', playerX, playerY);
            
            // Reload building images for Level 1 (East Village Buildings)
            buildingImages = [];
            buildingImagesLoaded = 0;
            loadBuildingImages();
            
            // Reload street image for Level 1
            streetImageLoaded = false;
            streetImage = null;
            loadStreetImage();
            
            // Load all sprites and images for Level 1
            loadTaxiImage();
            loadWebImage();
            loadTaxiSpiderManSprite();
            loadSwingSpiderManSprites();
            loadVillainSprites();
            
            // Initialize villains for Level 1
            initVillains();
            
            // Initialize background music
            initBackgroundMusic();
        }
        
        function startLevel1() {
            level1State = 'splash';
            currentLevel = 1;
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
        
        function startLevel2() {
            console.log('=== startLevel2() called ===');
            level2State = 'splash';
            currentLevel = 2;
            currentState = 'gameplay'; // Set currentState to gameplay
            console.log('Level 2 state set - level2State:', level2State, 'currentLevel:', currentLevel, 'currentState:', currentState);
            
            // Initialize Level 2 specific settings
            initLevel2();
            
            // Show Level 2 splash screen
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
            
            const title = 'LEVEL 2: TIMES SQUARE';
            ctx.strokeText(title, canvas.width/2, 100);
            ctx.fillText(title, canvas.width/2, 100);
            
            // Draw Times Square background
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
            bgImage.src = '/static/Times Square Pixel.png';
            
            setTimeout(() => {
                console.log('Level 2 splash timeout - starting gameplay');
                level2State = 'gameplay';
                currentState = 'gameplay'; // Make sure currentState is set to gameplay
                initGameplay();
            }, 2000);
        }
        
        function initLevel2() {
            console.log('=== initLevel2() called ===');
            
            // Reset game state for Level 2
            dustCollected = 0;
            totalDust = 0;
            lives = 3;
            score = 0;
            webShooterActive = false;
            webShooterTimer = 0;
            isRidingTaxi = false;
            winLock = false;
            
            // Reset player position to Level 2 spawn point
            playerX = 15; // Level 2 spawn X (center of map)
            playerY = 9; // Level 2 spawn Y (center of map)
            
            // Clear all arrays
            dustPositions = [];
            webShooterPositions = [];
            villainPositions = [];
            taxiStopPositions = [];
            villains = []; // Clear villains array
            
            // Initialize Level 2 map elements
            const currentMap = level2Map;
            const processedMap = processMazeWithFloodFill(currentMap);
            
            // Count total dust and place dust pellets
            for (let y = 0; y < processedMap.length; y++) {
                for (let x = 0; x < processedMap[y].length; x++) {
                    const tile = processedMap[y][x];
                    if (tile === '.') {
                        dustPositions.push({x: x, y: y});
                        totalDust++;
                    } else if (tile === 'W') {
                        webShooterPositions.push({x: x, y: y});
                    } else if (tile === 'T') {
                        // In Level 2, T represents Dimensional Fragments (not taxi stops)
                        dustPositions.push({x: x, y: y});
                        totalDust++;
                    } else if (tile === 'V') {
                        villainPositions.push({x: x, y: y, type: 'villain'});
                    }
                }
            }
            
            console.log('Level 2 initialized:');
            console.log('- Total dust/fragments:', totalDust);
            console.log('- Web shooters:', webShooterPositions.length);
            console.log('- Villains:', villainPositions.length);
            console.log('- Player spawn:', playerX, playerY);
            
            // Reload building images for Level 2 (Times Buildings)
            buildingImages = [];
            buildingImagesLoaded = 0;
            loadBuildingImages();
            
            // Reload street image for Level 2
            streetImageLoaded = false;
            streetImage = null;
            loadStreetImage();
        }
        
        function initGameplay() {
            console.log('=== initGameplay() called ===');
            console.log('Current level:', currentLevel);
            console.log('Current state:', currentState);
            canvas = document.getElementById('gameCanvas');
            ctx = canvas.getContext('2d');
            
            // Show canvas
            canvas.style.display = 'block';
            
            // Get current level map
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            
            // Calculate optimal tile size to fit screen horizontally
            const maxWidth = window.innerWidth * 0.98; // 98% of screen width for maximum horizontal coverage
            const maxHeight = window.innerHeight * 0.85; // 85% of screen height
            
            const tileSizeX = Math.floor(maxWidth / currentMap[0].length);
            const tileSizeY = Math.floor(maxHeight / currentMap.length);
            const tileSize = Math.min(tileSizeX, tileSizeY, 45); // Cap at 45px, minimum of 20px for better fit
            
            // Set canvas size to fit the map with space above for HUD
            canvas.width = currentMap[0].length * tileSize;
            canvas.height = currentMap.length * tileSize + 80; // Add 80px for HUD above
            
            // Store tile size globally for rendering
            window.gameTileSize = tileSize;
            
            // Start game loop
            gameLoop = setInterval(updateGame, 1000/60); // 60 FPS
            
            // Add keyboard controls
            document.addEventListener('keydown', handleKeyPress);
            
            // Ensure canvas doesn't interfere with UI overlays
            if (canvas) {
                canvas.style.pointerEvents = 'none';
            }
            
            // Start background music
            startBackgroundMusic();
        }
        
        function updateGame() {
            if (currentState !== 'gameplay') return;
            const currentLevelState = currentLevel === 1 ? level1State : level2State;
            if (currentLevelState !== 'gameplay') return;
            
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
                console.log('🔥🔥🔥 WIN CONDITION TRIGGERED! 🔥🔥🔥');
                console.log('🔥 Dust collected:', dustCollected);
                console.log('🔥 Total dust:', totalDust);
                console.log('🔥 Lives remaining:', lives);
                console.log('🔥 Calling continueToNextLevel() directly (skip win screen)...');
                if (currentLevel === 1) {
                    level1State = 'win';
                } else {
                    level2State = 'win';
                }
                clearInterval(gameLoop);
                continueToNextLevel();
                return;
            }
            
            // Check lose condition
            if (lives <= 0) {
                console.log('🔥🔥🔥 LOSE CONDITION TRIGGERED! 🔥🔥🔥');
                console.log('🔥 Lives:', lives);
                console.log('🔥 Dust collected:', dustCollected);
                console.log('🔥 Total dust:', totalDust);
                console.log('🔥 Calling showGameOverScreen()...');
                if (currentLevel === 1) {
                    level1State = 'lose';
                } else {
                    level2State = 'lose';
                }
                clearInterval(gameLoop);
                showGameOverScreen(); // Use game over screen when all lives are lost
                return;
            }
            
            renderGame();
        }
        
        function renderGame() {
            if (!ctx) return;
            
            // Don't render game when win/lose screens are active
            if (currentState === 'win' || currentState === 'lose' || currentState === 'gameOver') {
                return;
            }
            
            const tileSize = window.gameTileSize || 30;
            
            // Clear canvas
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw HUD above the game board
            drawHUD();
            
            // Draw background based on current level
            if (!window.backgroundImage) {
                window.backgroundImage = new Image();
                window.backgroundImage.onload = function() {
                    // Background is loaded, but we'll draw it in drawMapElements
                };
                if (currentLevel === 1) {
                    window.backgroundImage.src = '/static/East_Village_Pixel_Scape.png';
                } else {
                    window.backgroundImage.src = '/static/Times Square Pixel.png';
                }
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
            
            // Get processed map based on current level
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            const processedMap = processMazeWithFloodFill(currentMap);
            
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
                        const requiredImages = currentLevel === 1 ? 6 : 8;
                        if (buildingImagesLoaded >= requiredImages) {
                            // Select building image based on position for variety
                            const buildingIndex = (x + y * 3) % requiredImages;
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
                        if (currentLevel === 1) {
                            // Level 1: Draw taxi stop with image (only if not riding and taxi still exists)
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
                        } else {
                            // Level 2: Draw Dimensional Fragment (rainbow crystal shard)
                            const fragmentExists = dustPositions.some(dust => dust.x === x && dust.y === y);
                            if (fragmentExists) {
                                // Draw rainbow crystal shard effect
                                ctx.fillStyle = '#ff00ff'; // Magenta base
                                ctx.beginPath();
                                ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 6, 0, 2 * Math.PI);
                                ctx.fill();
                                ctx.strokeStyle = '#00ffff'; // Cyan outline
                                ctx.lineWidth = 2;
                                ctx.stroke();
                                // Add rainbow glow effect
                                ctx.shadowColor = '#ff00ff';
                                ctx.shadowBlur = 8;
                                ctx.beginPath();
                                ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 4, 0, 2 * Math.PI);
                                ctx.fill();
                                ctx.shadowBlur = 0;
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
                
                // Add fade effect when web shooter is active
                if (webShooterActive) {
                    // Create a pulsing fade effect (fade in and out)
                    const fadeValue = 0.3 + 0.7 * Math.abs(Math.sin(Date.now() * 0.01)); // Pulsing between 0.3 and 1.0
                    ctx.globalAlpha = fadeValue;
                }
                
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
                }
                
                if (villainSprite && villainSpritesLoaded >= 4) {
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
                        // Check if villain is using special power for bonus points
                        let isVillainUsingSpecialPower = false;
                        
                        if (villain.type === 'Doc Ock' && villainAbilities.alleyBlock.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Green Goblin' && villainAbilities.pumpkinBomb.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Vulture' && villainAbilities.windGust.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Venom' && villainAbilities.darkTendrils.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Hobgoblin' && villainAbilities.razorBats.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Prowler' && villainAbilities.clawsOfDarkness.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Mysterio' && villainAbilities.illusionGas.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Sandman' && villainAbilities.tailWhip.active) {
                            isVillainUsingSpecialPower = true;
                        }
                        
                        // Stun villain
                        villain.stunned = true;
                        villain.stunnedTimer = 180; // 3 seconds
                        
                        // Award bonus points for defeating powered-up villains
                        if (isVillainUsingSpecialPower) {
                            score += 300; // Triple points for defeating powered-up villain
                        } else {
                            score += 100; // Normal points for defeating regular villain
                        }
                    } else {
                        // Check if villain is using special power
                        let isVillainUsingSpecialPower = false;
                        
                        if (villain.type === 'Doc Ock' && villainAbilities.alleyBlock.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Green Goblin' && villainAbilities.pumpkinBomb.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Vulture' && villainAbilities.windGust.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Venom' && villainAbilities.darkTendrils.active) {
                            isVillainUsingSpecialPower = true;
                        }
                        
                        // Player loses life (2 if villain is using special power, 1 otherwise)
                        if (isVillainUsingSpecialPower) {
                            lives -= 2;
                        } else {
                            lives--;
                        }
                        
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
            if (webShooterActive) {
                ctx.fillStyle = '#00bfff';
                ctx.fillText('Web Shooter Active!', canvas.width/2, statusY + 60);
            }
        }
        
        function handleKeyPress(event) {
            const currentLevelState = currentLevel === 1 ? level1State : level2State;
            if (currentLevelState !== 'gameplay') return;
            
            // Don't allow movement while riding taxi
            if (isRidingTaxi) return;
            
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            const processedMap = processMazeWithFloodFill(currentMap);
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
                webShooterTimer = 480; // 8 seconds at 60 FPS (6 + 2 more seconds)
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
            console.log('🔥🔥🔥 === showWinScreen() called (win cutscene removed) === 🔥🔥🔥');
            // Skip win cutscene entirely and go straight to victory comic
            continueToNextLevel();
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
            console.log('🔥🔥🔥 === showGameOverScreen() called === 🔥🔥🔥');
            console.log('🔥 Current state before:', currentState);
            console.log('🔥 Win/Loss state before:', winLossState);
            
            currentState = 'gameOver';
            winLossState = 'gameOver';
            currentQuip = lossQuips[Math.floor(Math.random() * lossQuips.length)];
            quipTimer = 0;
            
            console.log('🔥 State set to:', currentState);
            console.log('🔥 Win/Loss state set to:', winLossState);
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide all panels and show game over cutscene
            console.log('🔥 Hiding all comic panels...');
            document.querySelectorAll('.comic-panel').forEach(panel => panel.classList.remove('active'));
            
            console.log('🔥 SHOWING GAME OVER CUTSCENE...');
            const winElement = document.getElementById('winCutscene');
            const loseElement = document.getElementById('loseCutscene');
            const gameOverElement = document.getElementById('gameOverCutscene');
            
            // Make sure other cutscenes are hidden
            if (winElement) {
                winElement.classList.remove('active');
                console.log('🔥 Win cutscene hidden');
            }
            if (loseElement) {
                loseElement.classList.remove('active');
                console.log('🔥 Lose cutscene hidden');
            }
            
            if (gameOverElement) {
                gameOverElement.classList.add('active');
                console.log('🔥 Game over cutscene shown');
            }
            
            document.getElementById('gameOverQuip').textContent = currentQuip;
            console.log('🔥 Game over quip set to:', currentQuip);
        }
        
        // Cut scene button functions
        function returnToTitle() {
            console.log('returnToTitle called!');
            // Reset the entire game state
            resetGame();
            
            // Hide all cutscenes
            document.querySelectorAll('.win-loss-cutscene').forEach(cutscene => cutscene.classList.remove('active'));
            // Hide all comic panels
            document.querySelectorAll('.comic-panel, .victory-panel').forEach(panel => panel.classList.remove('active'));
            // Show title screen
            document.getElementById('titleScreen').classList.add('active');
            
            // Stop any running game loop
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
            }
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide canvas if it exists
            if (canvas) {
                canvas.style.display = 'none';
            }
            
            console.log('returnToTitle completed!');
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
        
        function continueToNextLevel() {
            console.log('🔥🔥🔥 === continueToNextLevel() called === 🔥🔥🔥');
            console.log('🔥 Current state before:', currentState);
            console.log('🔥 Current victory panel:', currentVictoryPanel);
            console.log('🔥 Win cutscene element:', document.getElementById('winCutscene'));
            console.log('🔥 VictoryPanel0 element:', document.getElementById('victoryPanel0'));
            
            // CRITICAL: Hide ALL screens first
            console.log('🔥 HIDING ALL SCREENS FIRST...');
            
            // Hide title screen explicitly
            const titleScreen = document.getElementById('titleScreen');
            if (titleScreen) {
                titleScreen.classList.remove('active');
                titleScreen.style.display = 'none';
                console.log('🔥 Title screen hidden');
            }
            
            // Hide all cutscenes
            document.querySelectorAll('.win-loss-cutscene').forEach(cutscene => {
                cutscene.classList.remove('active');
                cutscene.style.display = 'none';
                console.log('🔥 Cutscene hidden:', cutscene.id);
            });
            
            // Hide all comic panels
            document.querySelectorAll('.comic-panel').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
                console.log('🔥 Comic panel hidden:', panel.id);
            });
            
            // Hide canvas
            const canvas = document.getElementById('gameCanvas');
            if (canvas) {
                canvas.style.display = 'none';
                console.log('🔥 Canvas hidden');
            }
            
            // Show victory comic panels
            console.log('🔥 Setting state to victoryComic...');
            currentState = 'victoryComic';
            currentVictoryPanel = 0;
            console.log('🔥 State changed to:', currentState);
            console.log('🔥 Victory panel set to:', currentVictoryPanel);
            
            console.log('🔥 Calling showVictoryPanel(0)...');
            showVictoryPanel(0);
            console.log('🔥🔥🔥 === continueToNextLevel() completed === 🔥🔥🔥');
        }
        
        function resetLevel() {
            console.log('=== resetLevel() called ===');
            // Reset level-specific variables
            playerX = 13;
            playerY = 12;
            score = 0;
            lives = 5; // Reset lives when retrying the same level
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
            
            // Reset level data (will be re-initialized when level starts)
            dustPositions = [];
            webShooterPositions = [];
            taxiStopPositions = [];
            totalDust = 0;
            
            // Reset villains
            villains = [];
            
            console.log('Level completely reset');
        }
        
        function startNewLevel() {
            console.log('=== startNewLevel() called ===');
            console.log('Current level before reset:', currentLevel);
            // Start a new level without resetting lives
            playerX = 13;
            playerY = 12;
            score = 0;
            // lives = 5; // Don't reset lives when starting a new level
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
            
            // Don't reset currentLevel - it should persist for level progression
            console.log('Current level after reset:', currentLevel);
        }
        
        function resetGame() {
            console.log('=== resetGame() called ===');
            // Reset all game variables
            resetLevel();
            
            // Reset level 2 state
            level2State = 'intro';
            currentLevel = 1;
            
            // Reset victory comic state
            currentVictoryPanel = 0;
            
            // Reset game state
            currentState = 'title';
            currentPanel = 0;
            
            // Reset villain abilities
            Object.keys(villainAbilities).forEach(ability => {
                villainAbilities[ability].active = false;
                villainAbilities[ability].timer = 0;
            });
            
            // Reset player effects
            playerSlowed = false;
            playerSlowTimer = 0;
            
            console.log('Game completely reset to initial state');
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
            } else if (currentState === 'victoryComic') {
                nextVictoryPanel();
            } else if (currentState === 'gameplay') {
                // Skip splash screen on click
                const currentLevelState = currentLevel === 1 ? level1State : level2State;
                if (currentLevelState === 'splash') {
                    if (currentLevel === 1) {
                        level1State = 'gameplay';
                    } else {
                        level2State = 'gameplay';
                    }
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
                if (currentState === 'title') {
                    startGame();
                } else if (currentState === 'comic') {
                    nextPanel();
                } else if (currentState === 'victoryComic') {
                    nextVictoryPanel();
                } else if (currentState === 'gameplay') {
                    const currentLevelState = currentLevel === 1 ? level1State : level2State;
                    if (currentLevelState === 'splash') {
                        // Skip splash screen
                        if (currentLevel === 1) {
                            level1State = 'gameplay';
                        } else {
                            level2State = 'gameplay';
                        }
                        initGameplay();
                    }
                }
            }
        });

        // Initialize
        console.log('Spider-Run game loaded!');
        console.log('Click to advance through comic panels');
        
        // TEMPORARY DEBUG: Force win screen for testing
        function debugForceWin() {
            console.log('=== DEBUG: Forcing win screen ===');
            
            // Stop any running game loop that might interfere
            if (gameLoop) {
                clearInterval(gameLoop);
                gameLoop = null;
                console.log('Game loop stopped');
            }
            
            // Set states
            currentState = 'win';
            winLossState = 'win';
            level1State = 'win';
            currentQuip = winQuips['level1'];
            quipTimer = 0;
            
            // Stop background music
            stopBackgroundMusic();
            
            // Hide all other elements
            document.querySelectorAll('.comic-panel, .victory-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById('titleScreen').classList.remove('active');
            
            // Show win cutscene
            const winCutscene = document.getElementById('winCutscene');
            console.log('🔥 SHOWING WIN CUTSCENE (FORCE WIN)...');
            winCutscene.classList.add('active');
            console.log('🔥 Win cutscene active class added (force):', winCutscene.classList.contains('active'));
            document.getElementById('winQuip').textContent = currentQuip;
            
            console.log('Win screen forced - currentState:', currentState);
            console.log('Win cutscene active:', winCutscene.classList.contains('active'));
            console.log('Win screen should now be visible and persistent');
        }
        
        // Add debug functions to window for console access
        window.debugForceWin = debugForceWin;
        
        // Debug function to check current screen state
        function debugCheckCurrentScreen() {
            console.log('🔥🔥🔥 === CURRENT SCREEN DEBUG === 🔥🔥🔥');
            console.log('🔥 Current state:', currentState);
            console.log('🔥 Win/Loss state:', winLossState);
            console.log('🔥 Current level:', currentLevel);
            console.log('🔥 Lives:', lives);
            console.log('🔥 Dust collected:', dustCollected);
            console.log('🔥 Total dust:', totalDust);
            
            const winElement = document.getElementById('winCutscene');
            const loseElement = document.getElementById('loseCutscene');
            const gameOverElement = document.getElementById('gameOverCutscene');
            
            console.log('🔥 --- CUTSCENE ELEMENTS ---');
            console.log('🔥 Win cutscene exists:', !!winElement);
            console.log('🔥 Win cutscene active:', winElement?.classList.contains('active'));
            console.log('🔥 Win cutscene visible:', winElement ? getComputedStyle(winElement).display !== 'none' : false);
            
            console.log('🔥 Lose cutscene exists:', !!loseElement);
            console.log('🔥 Lose cutscene active:', loseElement?.classList.contains('active'));
            console.log('🔥 Lose cutscene visible:', loseElement ? getComputedStyle(loseElement).display !== 'none' : false);
            
            console.log('🔥 Game over cutscene exists:', !!gameOverElement);
            console.log('🔥 Game over cutscene active:', gameOverElement?.classList.contains('active'));
            console.log('🔥 Game over cutscene visible:', gameOverElement ? getComputedStyle(gameOverElement).display !== 'none' : false);
            
            console.log('🔥 --- BUTTON CHECK ---');
            const buttons = document.querySelectorAll('.cutscene-button');
            buttons.forEach((button, index) => {
                if (button.offsetParent !== null) { // Check if button is visible
                    console.log(`🔥 Visible button ${index}:`, button.textContent, 'onclick:', button.getAttribute('onclick'));
                }
            });
            console.log('🔥🔥🔥 === END SCREEN DEBUG === 🔥🔥🔥');
        }
        
        window.debugCheckCurrentScreen = debugCheckCurrentScreen;
        
        // TEMPORARY DEBUG: Test continue function
        function testContinue() {
            console.log('=== TEST: testContinue() called ===');
            alert('Continue function is accessible!');
            continueToNextLevel();
        }
        window.testContinue = testContinue;
        
        // TEMPORARY DEBUG: Check what's currently visible
        function debugCheckVisible() {
            console.log('=== DEBUG: Checking visible elements ===');
            console.log('Title screen active:', document.getElementById('titleScreen').classList.contains('active'));
            console.log('Win cutscene active:', document.getElementById('winCutscene').classList.contains('active'));
            console.log('Lose cutscene active:', document.getElementById('loseCutscene').classList.contains('active'));
            console.log('Game over cutscene active:', document.getElementById('gameOverCutscene').classList.contains('active'));
            console.log('Current state:', currentState);
            console.log('Level 1 state:', level1State);
            console.log('Win/Loss state:', winLossState);
        }
        window.debugCheckVisible = debugCheckVisible;
        
        // CHEAT CODE: Jump directly to Times Square victory sequence
        function cheatToTimesSquare() {
            console.log('🔥🔥🔥 CHEAT CODE ACTIVATED: Jumping to Times Square victory sequence! 🔥🔥🔥');
            
            // Hide everything first
            document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            
            // Hide game canvas
            const canvas = document.getElementById('gameCanvas');
            if (canvas) canvas.style.display = 'none';
            
            // Set up victory comic state
            currentState = 'victoryComic';
            currentVictoryPanel = 0;
            currentLevel = 1; // Ensure we're in Level 1 context
            
            console.log('🔥 Cheat: State set to victoryComic, panel 0');
            
            // Show the first victory panel (Times Square sequence)
            showVictoryPanel(0);
            
            console.log('🔥🔥🔥 CHEAT COMPLETE: You should now see the first Times Square victory panel! 🔥🔥🔥');
            console.log('🔥 Click on the panel to advance through the sequence');
        }
        window.cheatToTimesSquare = cheatToTimesSquare;
        
        // CHEAT CODE: Jump directly to Level 2 splash screen
        function cheatToLevel2Splash() {
            console.log('🔥🔥🔥 CHEAT CODE ACTIVATED: Jumping directly to Level 2 splash! 🔥🔥🔥');
            
            // Hide everything first
            document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            
            // Hide game canvas
            const canvas = document.getElementById('gameCanvas');
            if (canvas) canvas.style.display = 'none';
            
            // Set up Level 2 splash state
            currentLevel = 2;
            currentState = 'level2Splash';
            
            console.log('🔥 Cheat: State set to level2Splash, level 2');
            
            // Show the Level 2 splash screen
            showLevel2Splash();
            
            console.log('🔥🔥🔥 CHEAT COMPLETE: You should now see the Level 2 splash screen! 🔥🔥🔥');
            console.log('🔥 Press SPACE to start Level 2 gameplay');
        }
        window.cheatToLevel2Splash = cheatToLevel2Splash;
        
        // CHEAT CODE: Test the victory panel transition
        function testVictoryPanelTransition() {
            console.log('🔥🔥🔥 TESTING VICTORY PANEL TRANSITION 🔥🔥🔥');
            console.log('Current victory panel:', currentVictoryPanel);
            console.log('Total victory panels:', totalVictoryPanels);
            console.log('Current state:', currentState);
            
            // Simulate being on the last panel
            currentVictoryPanel = 3;
            currentState = 'victoryComic';
            
            console.log('🔥🔥🔥 Simulated last panel - calling nextVictoryPanel()...');
            nextVictoryPanel();
        }
        
        window.testVictoryPanelTransition = testVictoryPanelTransition;
        
        // CHEAT CODE: Jump directly to Level 2 gameplay
        function cheatToLevel2() {
            console.log('🔥🔥🔥 CHEAT CODE ACTIVATED: Jumping directly to Level 2 gameplay! 🔥🔥🔥');
            
            // Hide all screens first
            document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            
            // Hide game canvas if it exists
            const canvas = document.getElementById('gameCanvas');
            if (canvas) canvas.style.display = 'none';
            
            // Set up Level 2 state
            currentLevel = 2;
            currentState = 'gameplay';
            level2State = 'gameplay';
            
            console.log('🔥 Cheat: Setting up Level 2...');
            console.log('🔥 Current level:', currentLevel);
            console.log('🔥 Current state:', currentState);
            console.log('🔥 Level 2 state:', level2State);
            
            // Initialize Level 2
            initLevel2();
            
            // Start Level 2 gameplay directly (skip splash screen)
            startLevel2Gameplay();
            
            console.log('🔥🔥🔥 CHEAT COMPLETE: You are now in Level 2 gameplay! 🔥🔥🔥');
        }
        
        window.cheatToLevel2 = cheatToLevel2;
        
        // Add event listener for start button
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up buttons...');
            
            // Start button
            const startButton = document.getElementById('startButton');
            console.log('Looking for start button...', startButton);
            if (startButton) {
                console.log('Start button found, adding click listener...');
                startButton.addEventListener('click', function(e) {
                    console.log('Start button clicked!');
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Start button clicked via event listener');
                    startGame();
                });
                console.log('Start button event listener added successfully');
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
