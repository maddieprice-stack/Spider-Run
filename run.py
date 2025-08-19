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
        
        /* --- Level 3 Intro: light animated effects --- */
        .portal-sparks {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 140px;
            height: 140px;
            margin-left: -70px;
            margin-top: -70px;
            border-radius: 50%;
            box-shadow:
                0 0 8px 2px rgba(255, 215, 0, 0.8),
                inset 0 0 20px 2px rgba(255, 140, 0, 0.5);
            border: 2px dashed rgba(255, 215, 0, 0.6);
            animation: spin 4s linear infinite;
            pointer-events: none;
        }
        
        .magic-orb {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 120px;
            height: 120px;
            margin-left: -60px;
            margin-top: -60px;
            border-radius: 50%;
            background: radial-gradient(circle at 40% 40%, rgba(0,191,255,0.9), rgba(0,0,0,0.1));
            box-shadow: 0 0 25px rgba(0,191,255,0.8), inset 0 0 20px rgba(255,255,255,0.2);
            animation: pulseGlow 2.2s ease-in-out infinite;
            pointer-events: none;
        }
        
        .sunrise-clock {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid #FFD700;
            box-shadow: 0 0 10px rgba(255,215,0,0.7);
            animation: clockPulse 1.4s ease-in-out infinite;
            pointer-events: none;
        }
        .sunrise-clock::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 2px;
            height: 22px;
            background: #FFD700;
            transform-origin: bottom center;
            transform: translate(-50%, -100%) rotate(20deg);
        }
        .sunrise-clock::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 2px;
            height: 16px;
            background: #FFD700;
            transform-origin: bottom center;
            transform: translate(-50%, -100%) rotate(120deg);
            opacity: 0.8;
        }
        
        .villain-silhouettes {
            position: absolute;
            bottom: 18%;
            left: 10%;
            right: 10%;
            height: 120px;
            pointer-events: none;
        }
        .villain-silhouettes .silhouette {
            position: absolute;
            width: 80px;
            height: 80px;
            background-size: contain;
            background-repeat: no-repeat;
            filter: brightness(0) contrast(200%);
            opacity: 0.7;
            animation: floatUp 3.5s ease-in-out infinite alternate;
        }
        .villain-silhouettes .s1 { left: 5%; background-image: url('/static/Doc_Oc.png'); animation-delay: 0s; }
        .villain-silhouettes .s2 { left: 28%; background-image: url('/static/Green_Goblin.png'); animation-delay: .3s; }
        .villain-silhouettes .s3 { left: 51%; background-image: url('/static/Vulture.png'); animation-delay: .6s; }
        .villain-silhouettes .s4 { left: 74%; background-image: url('/static/Venom.png'); animation-delay: .9s; }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulseGlow {
            0%, 100% { transform: scale(1); box-shadow: 0 0 18px rgba(0,191,255,0.6), inset 0 0 12px rgba(255,255,255,0.15); }
            50% { transform: scale(1.06); box-shadow: 0 0 30px rgba(0,191,255,0.95), inset 0 0 24px rgba(255,255,255,0.25); }
        }
        @keyframes clockPulse {
            0%, 100% { box-shadow: 0 0 8px rgba(255,215,0,0.6); transform: scale(1); }
            50% { box-shadow: 0 0 18px rgba(255,215,0,0.9); transform: scale(1.06); }
        }
        @keyframes floatUp {
            0% { transform: translateY(0); opacity: 0.65; }
            100% { transform: translateY(-18px); opacity: 0.85; }
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

        /* Comic overlay character selector */
        .character-select-overlay {
            position: fixed;
            top: 20px;
            right: 20px;
            display: none;
            flex-direction: column;
            gap: 8px;
            z-index: 10000;
            background: rgba(0,0,0,0.6);
            border: 3px solid #000;
            box-shadow: 5px 5px 0 rgba(0,0,0,0.35);
            padding: 12px;
            border-radius: 8px;
        }
        .character-select-overlay .title {
            color: #fff;
            font: bold 16px "Comic Sans MS", sans-serif;
            text-align: center;
        }
        .character-select-overlay .menu-button {
            min-width: 160px;
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

        <!-- Character Select Panel -->
        <div id="characterSelect" class="comic-panel">
            <div class="panel-content">
                <div class="speech-bubble">Choose Your Spider</div>
                <div style="display:flex; gap:24px; margin-top:16px; justify-content:center;">
                    <button class="menu-button" id="chooseSpiderManBtn" onclick="chooseSpider('spiderman')">Spider-Man</button>
                    <button class="menu-button" id="chooseMilesBtn" onclick="chooseSpider('miles')">Miles Morales</button>
                </div>
                <div style="display:flex; gap:24px; margin-top:12px; align-items:center; justify-content:center;">
                    <div style="width:140px; height:140px; background:url('/static/Spider-man%20sprite.png') center/contain no-repeat;"></div>
                    <div style="width:140px; height:140px; background:url('/static/Miles%20Morales%20Sprite.png') center/contain no-repeat;"></div>
                </div>
                <div style="display:flex; gap:24px; margin-top:24px; justify-content:center;">
                    <button class="menu-button" id="startIntroBtn" onclick="goToIntroComic()">Start Intro</button>
                </div>
            </div>
        </div>

        <!-- Comic Intro Panels -->
        <div id="comicPanelStart" class="comic-panel">
            <div class="panel-content">
                <div class="speech-bubble">
                    Spider-man: Space Dust Chaos
                </div>
            </div>
        </div>

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
                <div class="dr-strange-webp-image" style="background-image: url('/static/Dr%20Strange%203.png');"></div>
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
                <div class="dr-strange-webp-image" style="background-image: url('/static/Dr%20Strange%203.png');"></div>
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
                <div class="dr-strange-webp-image" style="background-image: url('/static/Dr%20Strange%203.png');"></div>
                <div class="speech-bubble">
                    The dust is scattered across the East Village — start there before it spreads any further!
                </div>
            </div>
        </div>

        <div id="comicPanel6" class="comic-panel">
            <div class="panel-content">
                <div class="dr-strange-webp-image" style="background-image: url('/static/Dr%20Strange%203.png');"></div>
                <div class="speech-bubble">
                    Be careful, Spider-Man. Some of your enemies are out tonight.
                </div>
            </div>
        </div>

        <!-- Comic character choice overlay (appears on intro comic until chosen) -->
        <div id="comicCharacterSelect" class="character-select-overlay">
            <div class="title">Choose Your Spider</div>
            <button class="menu-button" id="chooseSpiderFromComicBtn" onclick="setSelectedSpider('spiderman')">Spider-Man</button>
            <button class="menu-button" id="chooseMilesFromComicBtn" onclick="setSelectedSpider('miles')">Miles Morales</button>
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

        <!-- Level 3 Intro Cutscene Panels (post-Level 2 win) -->
        <div id="level3IntroPanel0" class="victory-panel" style="background: url('/static/New%20York%203%20Updated.png') no-repeat center center; background-size: cover;">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="portal-sparks"></div>
                <div class="speech-bubble">
                    Well done, Spider-Man. You cleared the space dust — but it's not over yet.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="level3IntroPanel1" class="victory-panel" style="background: url('/static/New%20York%203%20Updated.png') no-repeat center center; background-size: cover;">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="magic-orb"></div>
                <div class="speech-bubble">
                    The dust has spread… to the Empire State Building. And it's climbing fast.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="level3IntroPanel2" class="victory-panel" style="background: url('/static/New%20York%203%20Updated.png') no-repeat center center; background-size: cover;">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="sunrise-clock"></div>
                <div class="speech-bubble">
                    You have until sunrise to clean it up. If even one speck remains, the world ends.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <div id="level3IntroPanel3" class="victory-panel" style="background: url('/static/New%20York%203%20Updated.png') no-repeat center center; background-size: cover;">
            <div class="panel-content">
                <div class="dr-strange-webp-image"></div>
                <div class="villain-silhouettes">
                    <div class="silhouette s1"></div>
                    <div class="silhouette s2"></div>
                    <div class="silhouette s3"></div>
                    <div class="silhouette s4"></div>
                    </div>
                <div class="speech-bubble">
                    But beware… you're not the only one racing to the top.
                </div>
                <div class="click-prompt">Click to continue</div>
            </div>
        </div>

        <!-- Spider-Man quip panel -->
        <div id="level3IntroPanel4" class="victory-panel" style="background: url('/static/New%20York%203%20Updated.png') no-repeat center center; background-size: cover;">
            <div class="panel-content">
                <div class="spider-man-victory-scene" style="background-image: url('/static/Spider-man%20Comic%203.png');"></div>
                <div class="speech-bubble">
                    Note to self: race to the top, avoid villains, save the world before breakfast. Easy.
                    </div>
                <div class="click-prompt">Click to start Level 3</div>
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

        <div id="victoryPanel4" class="victory-panel">
            <div class="panel-content">
                <div class="dr-strange-times-square"></div>
                <div class="speech-bubble">
                    Beware, Spider-Man! Mysterio and Electro are also there, and they know how to use Times Square to their advantage.
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
        const totalPanels = 8;
        let currentVictoryPanel = 0;
        const totalVictoryPanels = 5;
        
        // Character selection state
        let selectedSpider = 'spiderman'; // 'spiderman' | 'miles'
        let characterChosen = false;
        
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
        
        // Waka waka sound system (disabled)
        // let wakaWakaAudio = null;
        // let isWakaWakaPlaying = false;
        // let wakaWakaTimeout = null;
        
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
        
        // Level 2 map data - New Times Square layout with wraparound mechanics
        const level2Map = [
            "##############################",
            "#W..........T####...........W#",
            "R.####.###...####...###.####.R",
            "#..#....#.#...##...#.#....#..#",
            "#.....##....#.##.#....##.....#",
            "####..###..##....##..###..####",
            "#########..###EE###..#########",
            "#########..#VVVVVV#..#########",
            "#########..########..#########",
            "####..###..##..S.##.T###..####",
            "#.....##....#.##.#....##.....#",
            "#..#....#.#...##...#.#....#..#",
            "R.####.###...####...###.####.R",
            "#W...........####...........W#",
            "##############################"
        ];
        
        // Level 3 map data - Empire State Building vertical maze (design-only)
        const level3Map = [
            "##############################",
            "#.......###.......#.....#...G#",
            "#.#####.###.#####.#.###.###.##",
            "#.#...#.###.....#...#.....#.##",
            "#.#.#.#.#######.#####.#####.##",
            "#...#.#.........#...#.....#..#",
            "#####.###########.#.#####.#.##",
            "#.....#.........#.#.#...#.#..#",
            "#.#####.#######.#.#.#.#.#.#.##",
            "#.#.....###.....#.#.#.#...#..#",
            "#.###.#####.#####.#.#.#####.##",
            "#.....#...#.....#.#.......#..#",
            "#######.#.#####.#.#########.##",
            "#.......#.......#............#",
            "S.############################",
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
            const spawnKey = `${9},${15}`; // Player spawn position (row 9, column 15)
            if (!reachable.has(spawnKey) && isWalkable(grid[9][15])) {
                queue.push([9, 15]);
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
                   char === 'V' || char === '-' || char === 'S' || char === 'E' || char === 'R';
        }
        
        function isPassable(char) {
            return char === '.' || char === ' ' || char === 'W' || char === 'T' || 
                   char === 'V' || char === '-' || char === 'S' || char === 'E' || char === 'R';
        }
        
        function hasBomb(x, y) {
            return bombPositions.some(bomb => bomb.x === x && bomb.y === y);
        }
        
        function hasCrash(x, y) {
            return crashPositions.some(crash => crash.x === x && crash.y === y);
        }
        
        // Dust positions (calculated from map)
        let dustPositions = [];
        let webShooterPositions = [];
        let taxiStopPositions = [];
        
        // Level 2 camera collectible
        let cameraImage = null;
        let cameraImageLoaded = false;
        let cameraPosition = null; // {x, y}
        // Selfie flash overlay
        let selfieImage = null;
        let selfieLoaded = false;
        let selfieTimer = 0; // frames remaining
        // Level 2 subway signs
        let subwayImage = null;
        let subwayImageLoaded = false;
        let subwayPositions = []; // [{x,y}, {x,y}]
        let subwayTeleportCooldown = 0;
        
        // Villain system
        let villains = [];
        let villainPen = { x: 13, y: 6 }; // Center of villain pen
        // Villain spawn positions - these will be set dynamically based on V positions in the map
        let villainSpawns = [];
        
        // Global frame counter and last-ability timestamps to avoid simultaneous triggers
        let globalFrameCounter = 0;
        let lastDocOckAbilityFrame = -99999;
        let lastGoblinAbilityFrame = -99999;
        let lastMysterioAbilityFrame = -99999;
        let lastElectroAbilityFrame = -99999;
        
        // Villain types for both levels
        const villainTypes = [
            { name: 'Doc Ock', color: '#228B22', speed: 0.9, ability: 'alleyBlock' },
            { name: 'Green Goblin', color: '#32CD32', speed: 1.0, ability: 'pumpkinBomb' },
            { name: 'Vulture', color: '#006400', speed: 1.1, ability: 'windGust' },
            { name: 'Venom', color: '#000000', speed: 1.1, ability: 'windGust' },
            { name: 'Mysterio', color: '#4B0082', speed: 0.8, ability: 'illusion' },
            { name: 'Electro', color: '#FFD700', speed: 1.2, ability: 'lightning' }
        ];
        
        // Villain state
        let villainAbilities = {
            alleyBlock: { active: false, timer: 0, cooldown: 720 }, // 12 seconds at 60fps
            pumpkinBomb: { active: false, timer: 0, cooldown: 720 },
            windGust: { active: false, timer: 0, cooldown: 720 },
            darkTendrils: { active: false, timer: 0, cooldown: 720 }, // Venom
            illusion: { active: false, timer: 0, cooldown: 1800 }, // Mysterio - 30 seconds (much less frequent)
            lightning: { active: false, timer: 0, cooldown: 1200 } // Electro - 20 seconds (less frequent)
        };
        
        let playerSlowed = false;
        let playerSlowTimer = 0;
        
        // Electro lightning flash effect
        let electroFlashActive = false;
        let electroFlashTimer = 0;
        let electroFlashX = 0;
        let electroFlashY = 0;
        
        // Mysterio illusion flash effect
        let mysterioFlashActive = false;
        let mysterioFlashTimer = 0;
        let mysterioFlashX = 0;
        let mysterioFlashY = 0;
        
        // Green Goblin bomb system
        let bombPositions = [];
        let bombImage = null;
        let bombImageLoaded = false;
        
        // Doc Ock crash system
        let crashPositions = [];
        let crashImage = null;
        let crashImageLoaded = false;
        
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
            'Mysterio': null,
            'Electro': null
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
            const taxiPath = '/static/Taxi.png';
            console.log('Loading taxi image from:', taxiPath);
            const img = new Image();
            img.onload = function() {
                taxiImageLoaded = true;
                taxiImage = img;
                console.log('Taxi image loaded successfully! taxiImageLoaded:', taxiImageLoaded, 'taxiImage:', !!taxiImage);
            };
            img.onerror = function() {
                console.error('Failed to load taxi image from:', taxiPath);
            };
            img.src = taxiPath;
        }
        
        // Load web image
        let webImage = null;
        let webImageLoaded = false;
        
        function loadWebImage() {
            const webPath = '/static/Web.png';
            console.log('Loading web image from:', webPath);
            const img = new Image();
            img.onload = function() {
                webImageLoaded = true;
                webImage = img;
                console.log('Web image loaded successfully! webImageLoaded:', webImageLoaded, 'webImage:', !!webImage);
            };
            img.onerror = function() {
                console.error('Failed to load web image from:', webPath);
                // Try fallback to webs.png
                console.log('Trying fallback to webs.png...');
                const fallbackImg = new Image();
                fallbackImg.onload = function() {
                    webImageLoaded = true;
                    webImage = fallbackImg;
                    console.log('Fallback web image loaded successfully!');
                };
                fallbackImg.onerror = function() {
                    console.error('Failed to load fallback web image from /static/webs.png');
                };
                fallbackImg.src = '/static/webs.png';
            };
            img.src = webPath;
        }
        
        // Load taxi Spider-Man sprite
        let taxiSpiderManSprite = null; // will hold Spider-Man taxi by default
        let taxiMilesSprite = null;     // Miles taxi sprite
        let taxiSpiderManLoaded = false;
        let taxiMilesLoaded = false;
        
        function loadTaxiSpiderManSprite() {
            // Load Spider-Man taxi
            const smPath = '/static/spider_man_taxi.png';
            const smImg = new Image();
            smImg.onload = function() { taxiSpiderManLoaded = true; };
            smImg.src = smPath;
            taxiSpiderManSprite = smImg;
            // Load Miles taxi
            const milesPath = '/static/Miles Taxi.png';
            const milesImg = new Image();
            milesImg.onload = function() { taxiMilesLoaded = true; };
            milesImg.src = milesPath;
            taxiMilesSprite = milesImg;
        }
        
        // Load swing sprites (Spider-Man and Miles variants)
        let swingSpiderManSprite1 = null;
        let swingSpiderManSprite2 = null;
        let swingMilesSprite1 = null;
        let swingMilesSprite2 = null;
        let swingSpiderManLoaded = false;
        
        function loadSwingSpiderManSprites() {
            const sm1 = new Image();
            sm1.onload = function() { swingSpiderManLoaded = true; };
            sm1.src = '/static/spider_man_swing.png';
            swingSpiderManSprite1 = sm1;

            const sm2 = new Image();
            sm2.onload = function() { swingSpiderManLoaded = true; };
            sm2.src = '/static/spider_man_swing_2.png';
            swingSpiderManSprite2 = sm2;

            // Miles swing frames
            swingMilesSprite1 = new Image();
            swingMilesSprite1.src = '/static/Miles Morales Swinging.png';
            swingMilesSprite2 = new Image();
            swingMilesSprite2.src = '/static/Miles Morales Swinging 2.png';
        }
        
        // Load villain sprites
        function loadVillainSprites() {
            const villainPaths = {
                'Doc Ock': '/static/Doc_Oc.png',
                'Green Goblin': '/static/Green_Goblin.png',
                'Vulture': '/static/Vulture.png',
                'Venom': '/static/Venom.png',
                'Mysterio': '/static/Mysterio.png',
                'Electro': '/static/Electro.png'
            };
            
            Object.keys(villainPaths).forEach(villainName => {
                const img = new Image();
                img.onload = function() {
                    villainSpritesLoaded++;
                    console.log(`Loaded villain sprite: ${villainName}`);
                };
                img.onerror = function() {
                    console.error(`Failed to load villain sprite: ${villainName}`);
                };
                img.src = villainPaths[villainName];
                villainSprites[villainName] = img;
            });
        }
        
        // Load bomb image
        function loadBombImage() {
            bombImage = new Image();
            bombImage.onload = function() {
                bombImageLoaded = true;
                console.log('✅ Loaded bomb image successfully');
            };
            bombImage.onerror = function() {
                console.error('❌ Failed to load bomb image from:', bombImage.src);
                bombImageLoaded = false;
                
                // Try alternative path without URL encoding
                const fallbackImage = new Image();
                fallbackImage.onload = function() {
                    bombImage = fallbackImage;
                    bombImageLoaded = true;
                    console.log('✅ Loaded bomb image with fallback path');
                };
                fallbackImage.onerror = function() {
                    console.error('❌ Failed to load bomb image with fallback path');
                };
                fallbackImage.src = '/static/Green Goblin Bomb.png';
            };
            bombImage.src = '/static/Green%20Goblin%20Bomb.png';
        }
        
        // Load crash image
        function loadCrashImage() {
            crashImage = new Image();
            crashImage.onload = function() {
                crashImageLoaded = true;
                console.log('Loaded crash image successfully');
            };
            crashImage.onerror = function() {
                console.error('Failed to load crash image');
                crashImageLoaded = false;
            };
            crashImage.src = '/static/Doc%20Oc%20Crash.png';
        }
        
        // Initialize villains
        function initVillains() {
            villains = [];
            
            // Get current map to find V positions
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            
            // Find all V positions in the map
            villainSpawns = [];
            for (let y = 0; y < currentMap.length; y++) {
                for (let x = 0; x < currentMap[y].length; x++) {
                    if (currentMap[y][x] === 'V') {
                        villainSpawns.push({ x: x, y: y });
                    }
                }
            }
            
            console.log(`Found ${villainSpawns.length} villain spawn positions:`, villainSpawns);
            
            // Level-specific villain selection
            let levelVillainTypes;
            if (currentLevel === 1) {
                // Level 1: Only the original 4 villains
                levelVillainTypes = villainTypes.slice(0, 4);
            } else {
                // Level 2: All 6 villains including Electro and Mysterio
                levelVillainTypes = villainTypes;
            }
            
            // Create villains based on level and available spawn positions
            const numVillains = Math.min(levelVillainTypes.length, villainSpawns.length);
            for (let i = 0; i < numVillains; i++) {
                const spawn = villainSpawns[i];
                const villainType = levelVillainTypes[i];
                
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
            
            console.log(`Created ${villains.length} villains for Level ${currentLevel}:`, villains.map(v => v.type));
        }
        
        // Villain AI movement
        function updateVillains() {
            villains.forEach(villain => {
                if (villain.stunned) {
                    villain.stunnedTimer--;
                    if (villain.stunnedTimer <= 0) {
                        villain.stunned = false;
                        // Return to pen - use the first V position from current level
                        if (villainSpawns.length > 0) {
                            villain.x = villainSpawns[0].x;
                            villain.y = villainSpawns[0].y;
                        }
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
                
                // Update abilities with desynchronization to avoid simultaneous triggers
                villain.abilityTimer++;
                const jitter = (villain.type === 'Green Goblin' ? 30 : 0)
                              + (villain.type === 'Doc Ock' ? 60 : 0)
                              + (villain.type === 'Mysterio' ? 45 : 0)
                              + (villain.type === 'Electro' ? 75 : 0);
                const baseCooldown = 720; // 12 seconds
                if (villain.abilityTimer >= baseCooldown + jitter) {
                    // Prevent paired villains from triggering on the same second window
                    if (villain.type === 'Doc Ock' && Math.abs(globalFrameCounter - lastGoblinAbilityFrame) < 60) {
                        // Defer by one second if Goblin just used ability
                        villain.abilityTimer = baseCooldown + jitter - 1;
                    } else if (villain.type === 'Green Goblin' && Math.abs(globalFrameCounter - lastDocOckAbilityFrame) < 60) {
                        villain.abilityTimer = baseCooldown + jitter - 1;
                    } else if (villain.type === 'Mysterio' && Math.abs(globalFrameCounter - lastElectroAbilityFrame) < 60) {
                        villain.abilityTimer = baseCooldown + jitter - 1;
                    } else if (villain.type === 'Electro' && Math.abs(globalFrameCounter - lastMysterioAbilityFrame) < 60) {
                        villain.abilityTimer = baseCooldown + jitter - 1;
                    } else {
                    villain.abilityTimer = 0;
                    useVillainAbility(villain);
                        if (villain.type === 'Doc Ock') lastDocOckAbilityFrame = globalFrameCounter;
                        if (villain.type === 'Green Goblin') lastGoblinAbilityFrame = globalFrameCounter;
                        if (villain.type === 'Mysterio') lastMysterioAbilityFrame = globalFrameCounter;
                        if (villain.type === 'Electro') lastElectroAbilityFrame = globalFrameCounter;
                    }
                }
            });
        }
        
        function setNewTarget(villain) {
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            const processedMap = currentLevel === 1 ? processMazeWithFloodFill(currentMap) : currentMap;
            
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
            } else if (villain.type === 'Electro') {
                // Electro is fast and prefers open areas
                villain.targetX = Math.floor(Math.random() * processedMap[0].length);
                villain.targetY = Math.floor(Math.random() * processedMap.length);
            } else if (villain.type === 'Mysterio') {
                // Mysterio prefers to stay in the center areas
                const centerX = Math.floor(processedMap[0].length / 2);
                const centerY = Math.floor(processedMap.length / 2);
                const radius = Math.min(centerX, centerY) / 2;
                
                villain.targetX = Math.floor(centerX + (Math.random() - 0.5) * radius * 2);
                villain.targetY = Math.floor(centerY + (Math.random() - 0.5) * radius * 2);
                
                console.log(`Mysterio targeting: (${villain.targetX}, ${villain.targetY}) from center (${centerX}, ${centerY})`);
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
            const currentMap = currentLevel === 1 ? level1Map : level2Map;
            const processedMap = currentLevel === 1 ? processMazeWithFloodFill(currentMap) : currentMap;
            
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
                
                if (villain.type === 'Mysterio') {
                    console.log(`Mysterio moved from (${villain.x}, ${villain.y}) to (${nextStep.x}, ${nextStep.y})`);
                }
            } else {
                // No path found or already at target, set new target
                if (villain.type === 'Mysterio') {
                    console.log(`Mysterio no path found, setting new target. Current: (${villain.x}, ${villain.y}), Target: (${villain.targetX}, ${villain.targetY})`);
                }
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
                    
                    // Check bounds and if it's a wall or has a crash
                    if (neighborX < 0 || neighborX >= map[0].length || 
                        neighborY < 0 || neighborY >= map.length || 
                        map[neighborY][neighborX] === '#' || 
                        hasCrash(neighborX, neighborY) ||
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
                // Doc Ock places a temporary blocker at his current position (10 seconds)
                villainAbilities.alleyBlock.active = true;
                villainAbilities.alleyBlock.timer = 600; // 10 seconds at 60fps
                const crash = {
                    x: villain.x,
                    y: villain.y,
                    timer: 600
                };
                crashPositions.push(crash);
                console.log(`Doc Ock placed blocker at (${villain.x}, ${villain.y})`);
            } else if (villain.ability === 'pumpkinBomb') {
                // Green Goblin drops bomb at his current position
                villainAbilities.pumpkinBomb.active = true;
                villainAbilities.pumpkinBomb.timer = 240; // 4 seconds
                const bomb = {
                    x: villain.x,
                    y: villain.y,
                    timer: 600 // 10 seconds (600 frames at 60fps)
                };
                bombPositions.push(bomb);
                console.log(`Green Goblin placed bomb at (${villain.x}, ${villain.y})`);
            } else if (villain.ability === 'windGust') {
                // Vulture creates wind gust
                villainAbilities.windGust.active = true;
                villainAbilities.windGust.timer = 180; // 3 seconds
                playerSlowed = true;
                playerSlowTimer = 180; // 3 seconds
            } else if (villain.ability === 'illusion') {
                // Mysterio creates illusion gas
                villainAbilities.illusion.active = true;
                villainAbilities.illusion.timer = 600; // 10 seconds
                // Trigger massive purple flash effect
                mysterioFlashActive = true;
                mysterioFlashTimer = 600; // 10 seconds total
                mysterioFlashX = villain.x;
                mysterioFlashY = villain.y;
            } else if (villain.ability === 'lightning') {
                // Electro uses lightning power
                villainAbilities.lightning.active = true;
                villainAbilities.lightning.timer = 600; // 10 seconds
                // Trigger massive white flash effect
                electroFlashActive = true;
                electroFlashTimer = 600; // 10 seconds total
                electroFlashX = villain.x;
                electroFlashY = villain.y;
            }
        }
        
        // Initialize level 1 data
        function initLevel1() {
            // Process the maze with flood-fill to close off enclosed spaces
            const processedMap = processMazeWithFloodFill(level1Map);
            
            dustPositions = [];
            webShooterPositions = [];
            taxiStopPositions = [];
            bombPositions = []; // Clear bombs when level starts
            crashPositions = []; // Clear crashes when level starts
            
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
            loadBombImage();
            loadCrashImage();
            
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
        let currentBackgroundMusic = null;
        
        function initBackgroundMusic() {
            // Initialize with Level 1 music by default
            if (!currentBackgroundMusic) {
                currentBackgroundMusic = new Audio('/static/background_music.mp3');
                currentBackgroundMusic.volume = 0.3; // Set volume to 30%
                currentBackgroundMusic.loop = true;
            }
        }
        
        function startBackgroundMusic() {
            if (currentBackgroundMusic) {
                currentBackgroundMusic.play().catch(error => {
                    console.log('Background music autoplay blocked:', error);
                });
            }
        }
        
        function stopBackgroundMusic() {
            if (currentBackgroundMusic) {
                currentBackgroundMusic.pause();
                currentBackgroundMusic.currentTime = 0;
            }
        }
        
        function switchToLevel2Music() {
            // Stop current music
            if (currentBackgroundMusic) {
                currentBackgroundMusic.pause();
                currentBackgroundMusic.currentTime = 0;
            }
            
            // Switch to Level 2 music
            currentBackgroundMusic = new Audio('/static/Spider song 2.mp3');
            currentBackgroundMusic.volume = 0.3; // Set volume to 30%
            currentBackgroundMusic.loop = true;
            
            // Start playing the new music
            currentBackgroundMusic.play().catch(error => {
                console.log('Level 2 background music autoplay blocked:', error);
            });
        }

        function switchToLevel1Music() {
            // Stop current music
            if (currentBackgroundMusic) {
                currentBackgroundMusic.pause();
                currentBackgroundMusic.currentTime = 0;
            }
            // Choose track based on selected Spider
            const track = (typeof selectedSpider !== 'undefined' && selectedSpider === 'miles')
                ? '/static/Miles Song 1.mp3'
                : '/static/background_music.mp3';
            currentBackgroundMusic = new Audio(track);
            currentBackgroundMusic.volume = 0.3;
            currentBackgroundMusic.loop = true;
        }

        function switchToLevel3Music() {
            // Stop current music
            if (currentBackgroundMusic) {
                currentBackgroundMusic.pause();
                currentBackgroundMusic.currentTime = 0;
            }
            // Switch to Level 3 music
            currentBackgroundMusic = new Audio('/static/Spider song 3.mp3');
            currentBackgroundMusic.volume = 0.3; // Set volume to 30%
            currentBackgroundMusic.loop = true;
            currentBackgroundMusic.addEventListener('error', function() {
                console.log('Level 3 music failed to load; falling back to default');
                currentBackgroundMusic = new Audio('/static/background_music.mp3');
                currentBackgroundMusic.volume = 0.3;
                currentBackgroundMusic.loop = true;
                currentBackgroundMusic.play().catch(err => console.log('Fallback music autoplay blocked:', err));
            }, { once: true });
            currentBackgroundMusic.play().catch(error => {
                console.log('Level 3 background music autoplay blocked:', error);
            });
        }
        
        // Waka waka sound functions (disabled)
        /*
        function initWakaWakaSound() {
            wakaWakaAudio = new Audio('/static/Waka Waka (PacMan) - QuickSounds.com.mp3');
            wakaWakaAudio.volume = 0.06; // Set volume to 6% (30% of previous 20%)
            wakaWakaAudio.loop = true;
        }
        
        function startWakaWakaSound() {
            if (wakaWakaAudio && !isWakaWakaPlaying) {
                wakaWakaAudio.play().catch(error => {
                    console.log('Waka waka sound autoplay blocked:', error);
                });
                isWakaWakaPlaying = true;
            }
        }
        
        function stopWakaWakaSound() {
            if (wakaWakaAudio && isWakaWakaPlaying) {
                wakaWakaAudio.pause();
                wakaWakaAudio.currentTime = 0;
                isWakaWakaPlaying = false;
            }
        }
        */

        // Panel navigation
        function showPanel(panelNumber) {
            console.log('=== showPanel() called with panelNumber:', panelNumber, '===');
            // Hide all panels including title screen
            document.querySelectorAll('.comic-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });

            // Show new panel immediately without page flip effect
            if (panelNumber < 0) {
                const p = document.getElementById('comicPanelStart');
                if (p) {
                    p.classList.add('active');
                    p.style.display = 'flex';
                    p.style.position = 'fixed';
                    p.style.top = '0';
                    p.style.left = '0';
                    p.style.width = '100vw';
                    p.style.height = '100vh';
                    p.style.visibility = 'visible';
                    p.style.opacity = '1';
                    p.style.zIndex = '9999';
                }
            } else if (panelNumber === 0) {
                const panel0 = document.getElementById('comicPanel0');
                console.log('Showing comicPanel0:', panel0);
                panel0.classList.add('active');
                panel0.style.display = 'flex';
                panel0.style.position = 'fixed';
                panel0.style.top = '0';
                panel0.style.left = '0';
                panel0.style.width = '100vw';
                panel0.style.height = '100vh';
                panel0.style.visibility = 'visible';
                panel0.style.opacity = '1';
                panel0.style.zIndex = '9999';
            } else {
                const panel = document.getElementById(`comicPanel${panelNumber}`);
                console.log('Showing comicPanel' + panelNumber + ':', panel);
                panel.classList.add('active');
                panel.style.display = 'flex';
                panel.style.position = 'fixed';
                panel.style.top = '0';
                panel.style.left = '0';
                panel.style.width = '100vw';
                panel.style.height = '100vh';
                panel.style.visibility = 'visible';
                panel.style.opacity = '1';
                panel.style.zIndex = '9999';
            }
            console.log('=== showPanel() completed ===');
        }

        // Game flow functions
        function startGame() {
            console.log('=== startGame() function called ===');
            console.log('Current state before:', currentState);
            playClickSound();
            // Go straight to intro comic; choose character on comic overlay
            document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(p => {
                p.classList.remove('active');
                p.style.display = 'none';
            });
            characterChosen = false;
            currentState = 'comic';
            // Start at new title panel before panel 0
            currentPanel = -1;
            showPanel(0);
            const overlay = document.getElementById('comicCharacterSelect');
            if (overlay) {
                overlay.style.display = 'flex';
            }
            console.log('=== startGame() function completed ===');
        }

        function setSelectedSpider(which) {
            selectedSpider = which === 'miles' ? 'miles' : 'spiderman';
            characterChosen = true;
            const overlay = document.getElementById('comicCharacterSelect');
            if (overlay) overlay.style.display = 'none';
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
                // End of comic, start Level 1 explicitly
                beginLevel1FromIntro();
            }
        }

        function beginLevel1FromIntro() {
            // Hide any overlays
            const overlay = document.getElementById('comicCharacterSelect');
            if (overlay) overlay.style.display = 'none';
            // Hide all comic panels
            document.querySelectorAll('.comic-panel').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            // Ensure proper state and music for Level 1
            currentState = 'gameplay';
            currentLevel = 1;
            if (typeof switchToLevel1Music === 'function') {
                switchToLevel1Music();
                startBackgroundMusic();
            }
            // Start Level 1 flow
            startLevel1();
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
            } else if (currentState === 'victoryComic' && currentVictoryPanel === totalVictoryPanels - 1) {
                console.log('🔥🔥🔥 Last victory panel reached, starting Level 2 gameplay...');
                console.log('🔥🔥🔥 Panel check: currentVictoryPanel =', currentVictoryPanel, 'totalVictoryPanels =', totalVictoryPanels);
                // End of victory comic, start Level 2 gameplay directly (like intro comic)
                startLevel2Gameplay();
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
            ctx.strokeText('Level 2: Times Square', canvas.width/2, canvas.height/2 - 25);
            ctx.fillText('Level 2: Times Square', canvas.width/2, canvas.height/2 - 25);
            
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
            
            // Set state to gameplay (like startGameplay does)
            currentState = 'gameplay';
            
            // Hide all victory panels AND comic panels (like startGameplay does)
            document.querySelectorAll('.victory-panel, .comic-panel').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            
            // Hide title screen if it's still visible
            const titleScreen = document.getElementById('titleScreen');
            if (titleScreen) {
                titleScreen.classList.remove('active');
                titleScreen.style.display = 'none';
            }
            
            // Switch to Level 2 music
            switchToLevel2Music();
            
            // Start Level 2 (like startGameplay calls startLevel1)
            startLevel2();
        }

        function startGameplay() {
            currentState = 'gameplay';
            document.querySelectorAll('.comic-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            
            // Ensure Level 1 music is playing (Spider-Man or Miles)
            if (currentLevel === 1) {
                switchToLevel1Music();
                startBackgroundMusic();
            } else {
            initBackgroundMusic();
            startBackgroundMusic();
            }
            
            // Start Level 1
            startLevel1();
        }

        // Level 1 functions
        function initLevel1() {
            console.log('=== initLevel1() called ===');
            
            // Reset game state for Level 1
            dustCollected = 0;
            totalDust = 0;
            lives = 5; // Spider-Man starts with 5 lives on each level
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
            loadBombImage();
            loadCrashImage();
            
            // Initialize villains for Level 1
            initVillains();
            
            // Initialize background music
            initBackgroundMusic();
            
            // Initialize waka waka sound (disabled)
            // initWakaWakaSound();
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
            console.log('🔥🔥🔥 Starting Level 2 splash screen! 🔥🔥🔥');
            level2State = 'splash';
            currentLevel = 2;
            initLevel2();
            
            // Show Level 2 splash screen
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            console.log('🔥🔥🔥 Canvas found:', canvas);
            console.log('🔥🔥🔥 Canvas dimensions:', canvas.width, 'x', canvas.height);
            
            // Make sure canvas is visible
            canvas.style.display = 'block';
            canvas.style.border = '5px solid #000';
            canvas.style.boxShadow = '5px 5px 0px rgba(0,0,0,0.3)';
            
            // Draw splash screen background
            ctx.fillStyle = '#1a1a2e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw comic-style title
            ctx.fillStyle = '#ffff00';
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 3;
            ctx.font = 'bold 48px Comic Sans MS';
            ctx.textAlign = 'center';
            
            const title = 'LEVEL 2: TIMES SQUARE';
            console.log('🔥🔥🔥 Drawing title:', title);
            ctx.strokeText(title, canvas.width/2, 100);
            ctx.fillText(title, canvas.width/2, 100);
            
            // Draw Times Square background
            const bgImage = new Image();
            bgImage.onload = function() {
                console.log('🔥🔥🔥 Times Square background image loaded!');
                ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
                // Redraw title over background
                ctx.fillStyle = '#ffff00';
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 3;
                ctx.font = 'bold 48px Comic Sans MS';
                ctx.textAlign = 'center';
                ctx.strokeText(title, canvas.width/2, 100);
                ctx.fillText(title, canvas.width/2, 100);
                console.log('🔥🔥🔥 Level 2 splash screen complete!');
            };
            bgImage.onerror = function() {
                console.error('🔥🔥🔥 ERROR: Could not load Times Square background image!');
                // Still show the title even if background fails
                ctx.fillStyle = '#ffff00';
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 3;
                ctx.font = 'bold 48px Comic Sans MS';
                ctx.textAlign = 'center';
                ctx.strokeText(title, canvas.width/2, 100);
                ctx.fillText(title, canvas.width/2, 100);
            };
            bgImage.src = '/static/Times Square Pixel.png';
            
            console.log('🔥🔥🔥 Level 2 splash screen will show for 2 seconds...');
            setTimeout(() => {
                console.log('🔥🔥🔥 Level 2 splash screen timeout - starting gameplay...');
                level2State = 'gameplay';
                initGameplay();
            }, 2000);
        }
        
        function initLevel2() {
            console.log('=== initLevel2() called ===');
            
            // Reset game state for Level 2
            dustCollected = 0;
            totalDust = 0;
            lives = 5; // Spider-Man starts with 5 lives on each level
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
            bombPositions = []; // Clear bombs when level starts
            crashPositions = []; // Clear crashes when level starts
            villains = []; // Clear villains array
            
            // Initialize Level 2 map elements
            const currentMap = level2Map;
            const processedMap = currentMap; // Use original map without flood-fill
            
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
                        // In Level 2, T represents Taxi stops (not dimensional fragments)
                        taxiStopPositions.push({x: x, y: y});
                        console.log(`Added taxi stop at (${x}, ${y})`);
                    } else if (tile === 'V') {
                        villainPositions.push({x: x, y: y, type: 'villain'});
                    }
                    // Note: E tiles are walkable but don't spawn pellets
                    // Note: R tiles are walkable and don't spawn pellets (wraparound mechanics)
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
            
            // Load web image and other sprites
            loadWebImage();
            loadTaxiImage();
            loadTaxiSpiderManSprite();
            loadSwingSpiderManSprites();
            loadVillainSprites();
            loadBombImage();
            
            // Load camera image once
            if (!cameraImage) {
                cameraImage = new Image();
                cameraImage.onload = function() { cameraImageLoaded = true; };
                cameraImage.onerror = function() { cameraImageLoaded = false; };
                cameraImage.src = '/static/Camera.png';
            }
            if (!selfieImage) {
                selfieImage = new Image();
                selfieImage.onload = function() { selfieLoaded = true; };
                selfieImage.onerror = function() { selfieLoaded = false; };
                selfieImage.src = '/static/Spider-man Selfie.png';
            }
            if (!subwayImage) {
                subwayImage = new Image();
                subwayImage.onload = function() { subwayImageLoaded = true; };
                subwayImage.onerror = function() { subwayImageLoaded = false; };
                subwayImage.src = '/static/Subway Sign.png';
            }
            
            // Pick a random walkable square for camera (not a wall/blocker)
            cameraPosition = null;
            const attempts = 200;
            for (let i = 0; i < attempts; i++) {
                const rx = Math.floor(Math.random() * processedMap[0].length);
                const ry = Math.floor(Math.random() * processedMap.length);
                const tile = processedMap[ry][rx];
                if (tile !== '#') { // any non-wall is fine
                    cameraPosition = { x: rx, y: ry };
                    break;
                }
            }
            // Pick two random walkable squares for subway signs
            subwayPositions = [];
            let tries = 0;
            while (subwayPositions.length < 2 && tries < 400) {
                tries++;
                const rx = Math.floor(Math.random() * processedMap[0].length);
                const ry = Math.floor(Math.random() * processedMap.length);
                const tile = processedMap[ry][rx];
                if (tile !== '#') {
                    // avoid duplicating camera position
                    if (!cameraPosition || rx !== cameraPosition.x || ry !== cameraPosition.y) {
                        // avoid duplicates between subway spots
                        if (!subwayPositions.some(p => p.x === rx && p.y === ry)) {
                            subwayPositions.push({ x: rx, y: ry });
                        }
                    }
                }
            }
            loadCrashImage();
            
            // Initialize villains for Level 2
            initVillains();
            
            // Initialize background music
            initBackgroundMusic();
            
            // Initialize waka waka sound (disabled)
            // initWakaWakaSound();
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
            
            // Increment global frame counter
            globalFrameCounter++;
            if (subwayTeleportCooldown > 0) subwayTeleportCooldown--;
            
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
            
            // Update bomb timers
            for (let i = bombPositions.length - 1; i >= 0; i--) {
                bombPositions[i].timer--;
                if (bombPositions[i].timer <= 0) {
                    console.log(`Bomb at (${bombPositions[i].x}, ${bombPositions[i].y}) exploded`);
                    bombPositions.splice(i, 1);
                }
            }
            
            // Update crash timers
            for (let i = crashPositions.length - 1; i >= 0; i--) {
                crashPositions[i].timer--;
                if (crashPositions[i].timer <= 0) {
                    console.log(`Crash at (${crashPositions[i].x}, ${crashPositions[i].y}) cleared`);
                    crashPositions.splice(i, 1);
                }
            }
            
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
            
            // Check win condition (but not if we just came from victory comic)
            if (dustCollected >= totalDust && dustCollected > 0) {
                console.log('🔥🔥🔥 WIN CONDITION TRIGGERED! 🔥🔥🔥');
                console.log('🔥 Dust collected:', dustCollected);
                console.log('🔥 Total dust:', totalDust);
                console.log('🔥 Lives remaining:', lives);
                console.log('🔥 Calling continueToNextLevel() directly (skip win screen)...');
                
                // Stop background music when level is completed
                stopBackgroundMusic();
                
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
            
            // Draw Electro lightning flash effect
            if (electroFlashActive && electroFlashTimer > 0) {
                const tileSize = window.gameTileSize || 30;
                const hudHeight = 80;
                
                // Calculate flash area (6 surrounding squares)
                const flashRadius = 3; // 3 tiles in each direction = 6 surrounding squares
                const flashCenterX = electroFlashX * tileSize + tileSize / 2;
                const flashCenterY = electroFlashY * tileSize + hudHeight + tileSize / 2;
                const flashSize = flashRadius * tileSize * 2;
                
                // Calculate opacity based on timer
                let opacity = 1.0;
                if (electroFlashTimer <= 120) { // Last 2 seconds = fade out
                    opacity = electroFlashTimer / 120;
                }
                
                // Create radial gradient for the flash effect
                const gradient = ctx.createRadialGradient(
                    flashCenterX, flashCenterY, 0,
                    flashCenterX, flashCenterY, flashSize
                );
                gradient.addColorStop(0, `rgba(255, 255, 255, ${opacity})`);
                gradient.addColorStop(0.3, `rgba(255, 255, 255, ${opacity * 0.8})`);
                gradient.addColorStop(0.7, `rgba(255, 255, 255, ${opacity * 0.4})`);
                gradient.addColorStop(1, `rgba(255, 255, 255, 0)`);
                
                // Draw the flash effect
                ctx.fillStyle = gradient;
                ctx.fillRect(
                    flashCenterX - flashSize,
                    flashCenterY - flashSize,
                    flashSize * 2,
                    flashSize * 2
                );
                
                // Decrease timer
                electroFlashTimer--;
                if (electroFlashTimer <= 0) {
                    electroFlashActive = false;
                }
            }
            
            // Draw Mysterio illusion flash effect
            if (mysterioFlashActive && mysterioFlashTimer > 0) {
                const tileSize = window.gameTileSize || 30;
                const hudHeight = 80;
                
                // Calculate flash area (6 surrounding squares)
                const flashRadius = 3; // 3 tiles in each direction = 6 surrounding squares
                const flashCenterX = mysterioFlashX * tileSize + tileSize / 2;
                const flashCenterY = mysterioFlashY * tileSize + hudHeight + tileSize / 2;
                const flashSize = flashRadius * tileSize * 2;
                
                // Calculate opacity based on timer
                let opacity = 1.0;
                if (mysterioFlashTimer <= 120) { // Last 2 seconds = fade out
                    opacity = mysterioFlashTimer / 120;
                }
                
                // Create radial gradient for the purple flash effect
                const gradient = ctx.createRadialGradient(
                    flashCenterX, flashCenterY, 0,
                    flashCenterX, flashCenterY, flashSize
                );
                gradient.addColorStop(0, `rgba(75, 0, 130, ${opacity})`); // Purple center
                gradient.addColorStop(0.3, `rgba(75, 0, 130, ${opacity * 0.8})`);
                gradient.addColorStop(0.7, `rgba(75, 0, 130, ${opacity * 0.4})`);
                gradient.addColorStop(1, `rgba(75, 0, 130, 0)`);
                
                // Draw the flash effect
                ctx.fillStyle = gradient;
                ctx.fillRect(
                    flashCenterX - flashSize,
                    flashCenterY - flashSize,
                    flashSize * 2,
                    flashSize * 2
                );
                
                // Decrease timer
                mysterioFlashTimer--;
                if (mysterioFlashTimer <= 0) {
                    mysterioFlashActive = false;
                }
            }
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
            const processedMap = currentLevel === 1 ? processMazeWithFloodFill(currentMap) : currentMap;
            
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
                                // Debug info for successful rendering
                                if (x === 1 && y === 1) {
                                    console.log('Web shooter at (1,1) - RENDERED WITH IMAGE!');
                                }
                            } else {
                                // Fallback to blue circle while image loads
                                ctx.fillStyle = '#00bfff';
                                ctx.beginPath();
                                ctx.arc(drawX + tileSize/2, drawY + tileSize/2, 8, 0, 2 * Math.PI);
                                ctx.fill();
                                ctx.strokeStyle = '#ffffff';
                                ctx.lineWidth = 2;
                                ctx.stroke();
                                // Debug info
                                if (x === 1 && y === 1) {
                                    console.log('Web shooter at (1,1) - FALLBACK RENDERED - webImageLoaded:', webImageLoaded, 'webImage:', !!webImage);
                                }
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
                            // Level 2: Draw Taxi stop (only if not riding and taxi still exists)
                            if (!isRidingTaxi) {
                                // Check if this taxi position still exists in taxiStopPositions
                                const taxiExists = taxiStopPositions.some(taxi => taxi.x === x && taxi.y === y);
                                if (taxiExists) {
                                    console.log(`Drawing taxi at (${x}, ${y}) - taxiImageLoaded: ${taxiImageLoaded}, taxiImage: ${!!taxiImage}, currentLevel: ${currentLevel}`);
                                    if (taxiImageLoaded && taxiImage) {
                                        console.log(`Drawing Taxi.png image at (${drawX}, ${drawY})`);
                                        ctx.drawImage(taxiImage, drawX, drawY, tileSize, tileSize);
                                    } else {
                                        console.log(`Drawing yellow fallback square at (${drawX}, ${drawY})`);
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
            }
            
            // Draw villains
            drawVillains();
            
            // Draw bombs
            drawBombs();
            
            // Draw camera in Level 2 if positioned
            if (currentLevel === 2 && cameraPosition) {
                const drawX = cameraPosition.x * tileSize + 1;
                const drawY = cameraPosition.y * tileSize + 1 + hudHeight;
                const size = tileSize - 2;
                if (cameraImageLoaded && cameraImage) {
                    ctx.drawImage(cameraImage, drawX, drawY, size, size);
                } else {
                    // Fallback small gray square
                    ctx.fillStyle = '#888';
                    ctx.fillRect(drawX, drawY, size, size);
                }
            }
            // Draw subway signs in Level 2
            if (currentLevel === 2 && subwayPositions && subwayPositions.length > 0) {
                subwayPositions.forEach(pos => {
                    const sx = pos.x * tileSize + 1;
                    const sy = pos.y * tileSize + 1 + hudHeight;
                    const ssize = tileSize - 2;
                    if (subwayImageLoaded && subwayImage) {
                        ctx.drawImage(subwayImage, sx, sy, ssize, ssize);
                    } else {
                        ctx.fillStyle = '#0a0';
                        ctx.fillRect(sx, sy, ssize, ssize);
                    }
                });
            }

            // Draw selfie overlay if active
            if (selfieTimer > 0 && selfieLoaded && selfieImage) {
                const total = 120; // 2 seconds at 60fps
                const fadeOut = 20; // last ~0.33s fade
                const alpha = selfieTimer > fadeOut ? 1 : Math.max(0, selfieTimer / fadeOut);
                ctx.save();
                ctx.globalAlpha = alpha;
                // Center overlay covering most of canvas
                const overlayW = Math.floor(canvas.width * 0.6);
                const overlayH = Math.floor((overlayW * selfieImage.naturalHeight) / selfieImage.naturalWidth);
                const ox = Math.floor((canvas.width - overlayW) / 2);
                const oy = Math.floor((canvas.height - overlayH) / 2);
                ctx.drawImage(selfieImage, ox, oy, overlayW, overlayH);
                ctx.restore();
                selfieTimer--;
            }
            
            // Draw crashes
            drawCrashes();
            
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
                window.playerSprite.src = (selectedSpider === 'miles')
                    ? '/static/Miles Morales Sprite.png'
                    : '/static/Spider-man_Running_Sprite.png';
            } else {
                // Keep base sprite consistent with selection if not swinging/taxi
                const desiredBase = (selectedSpider === 'miles')
                    ? '/static/Miles Morales Sprite.png'
                    : '/static/Spider-man_Running_Sprite.png';
                if (!window.playerSprite.src.endsWith(desiredBase)) {
                    window.playerSprite.src = desiredBase;
                }
            }
            
            // Preload additional running frames (normal running animation)
            if (!window.playerRun2) {
                window.playerRun2 = new Image();
                window.playerRun2.onload = function() {};
                window.playerRun2.src = (selectedSpider === 'miles')
                    ? '/static/Miles Running 2.png'
                    : '/static/Spider-man%20run%202.png';
            } else {
                const desiredRun2 = (selectedSpider === 'miles')
                    ? '/static/Miles Running 2.png'
                    : '/static/Spider-man%20run%202.png';
                if (!window.playerRun2.src.endsWith(desiredRun2)) {
                    window.playerRun2.src = desiredRun2;
                }
            }
            if (!window.playerRun3) {
                window.playerRun3 = new Image();
                window.playerRun3.onload = function() {};
                window.playerRun3.src = (selectedSpider === 'miles')
                    ? '/static/Miles Running 3.png'
                    : '/static/Spider-man%20run%203.png';
            } else {
                const desiredRun3 = (selectedSpider === 'miles')
                    ? '/static/Miles Running 3.png'
                    : '/static/Spider-man%20run%203.png';
                if (!window.playerRun3.src.endsWith(desiredRun3)) {
                    window.playerRun3.src = desiredRun3;
                }
            }
            
            // Choose which Spider-Man sprite to use
            let currentPlayerSprite = window.playerSprite;
            if (isRidingTaxi) {
                if (selectedSpider === 'miles' && taxiMilesLoaded && taxiMilesSprite) {
                    currentPlayerSprite = taxiMilesSprite;
                } else if (taxiSpiderManLoaded && taxiSpiderManSprite) {
                currentPlayerSprite = taxiSpiderManSprite;
                }
            } else if (webShooterActive) {
                // Select Miles vs Spider-Man swing frames
                let swing1 = swingSpiderManSprite1;
                let swing2 = swingSpiderManSprite2;
                let swingReady = swingSpiderManLoaded;
                if (selectedSpider === 'miles' && swingMilesSprite1 && swingMilesSprite2) {
                    swing1 = swingMilesSprite1;
                    swing2 = swingMilesSprite2;
                    swingReady = true;
                }
                if (swingReady && swing1 && swing2) {
                if (playerX !== lastPlayerX || playerY !== lastPlayerY) {
                    swingAnimationCounter++;
                    lastPlayerX = playerX;
                    lastPlayerY = playerY;
                }
                    currentPlayerSprite = (swingAnimationCounter % 2 === 0) ? swing1 : swing2;
                }
            } else {
                // Normal running animation (when not swinging or riding)
                if (typeof window.normalRunFrameIndex === 'undefined') {
                    window.normalRunFrameIndex = 0;
                }
                if (typeof window.lastNormalX === 'undefined') {
                    window.lastNormalX = playerX;
                    window.lastNormalY = playerY;
                }
                // Advance frame when moving tile-to-tile
                if (playerX !== window.lastNormalX || playerY !== window.lastNormalY) {
                    window.normalRunFrameIndex = (window.normalRunFrameIndex + 1) % 4; // 0..3
                    window.lastNormalX = playerX;
                    window.lastNormalY = playerY;
                }
                // Frame order (loop): base -> run2 -> run3 -> run2
                switch (window.normalRunFrameIndex) {
                    case 0:
                        currentPlayerSprite = window.playerSprite;
                        break;
                    case 1:
                        if (window.playerRun2 && window.playerRun2.complete) currentPlayerSprite = window.playerRun2;
                        break;
                    case 2:
                        if (window.playerRun3 && window.playerRun3.complete) currentPlayerSprite = window.playerRun3;
                        break;
                    case 3:
                        if (window.playerRun2 && window.playerRun2.complete) currentPlayerSprite = window.playerRun2;
                        break;
                    default:
                        currentPlayerSprite = window.playerSprite;
                        break;
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
                
                // Draw sprite preserving aspect ratio (avoid distortion across frames)
                const imgWidth = currentPlayerSprite.naturalWidth || currentPlayerSprite.width || tileSize;
                const imgHeight = currentPlayerSprite.naturalHeight || currentPlayerSprite.height || tileSize;
                const available = tileSize - 2;
                const scale = Math.min(available / imgWidth, available / imgHeight);
                const drawW = Math.max(1, Math.round(imgWidth * scale));
                const drawH = Math.max(1, Math.round(imgHeight * scale));
                const baseX = playerX * tileSize + 1 + Math.floor((available - drawW) / 2);
                const baseY = playerY * tileSize + 1 + hudHeight + Math.floor((available - drawH) / 2);
                
                if (playerDirection === 'left') {
                    // Flip horizontally when moving left
                    ctx.scale(-1, 1);
                    ctx.drawImage(currentPlayerSprite, -(baseX + drawW), baseY, drawW, drawH);
                } else {
                    // Normal drawing for other directions
                    ctx.drawImage(currentPlayerSprite, baseX, baseY, drawW, drawH);
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
                } else if (villain.type === 'Mysterio' && villainAbilities.illusion.active) {
                    glowColor = '#4B0082'; // Intense purple glow for Mysterio
                } else if (villain.type === 'Electro' && villainAbilities.lightning.active) {
                    glowColor = '#FFD700'; // Intense golden glow for Electro
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
                        // Much more intense glow for Electro and Mysterio
                        if (villain.type === 'Electro' && villainAbilities.lightning.active) {
                            ctx.shadowBlur = 50; // Very intense golden glow
                        } else if (villain.type === 'Mysterio' && villainAbilities.illusion.active) {
                            ctx.shadowBlur = 45; // Very intense purple glow
                        } else {
                            ctx.shadowBlur = 15; // Normal glow for other villains
                        }
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
                        // Much more intense glow for Electro and Mysterio
                        if (villain.type === 'Electro' && villainAbilities.lightning.active) {
                            ctx.shadowBlur = 50; // Very intense golden glow
                        } else if (villain.type === 'Mysterio' && villainAbilities.illusion.active) {
                            ctx.shadowBlur = 45; // Very intense purple glow
                        } else {
                            ctx.shadowBlur = 15; // Normal glow for other villains
                        }
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
        
        function drawBombs() {
            const tileSize = window.gameTileSize || 30;
            const hudHeight = 80; // Height of HUD area
            
            bombPositions.forEach(bomb => {
                const drawX = bomb.x * tileSize;
                const drawY = bomb.y * tileSize + hudHeight;
                
                if (bombImageLoaded && bombImage) {
                    // Draw bomb with image
                    ctx.drawImage(bombImage, drawX, drawY, tileSize, tileSize);
                    console.log('🎯 Drawing bomb image at:', drawX, drawY);
                } else {
                    // Fallback to green circle while image loads
                    ctx.fillStyle = '#00ff00';
                    ctx.beginPath();
                    ctx.arc(drawX + tileSize/2, drawY + tileSize/2, tileSize/3, 0, 2 * Math.PI);
                    ctx.fill();
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    console.log('⚠️ Drawing fallback green circle - bombImageLoaded:', bombImageLoaded, 'bombImage:', !!bombImage);
                }
                
                // Add pulsing effect as bomb gets closer to exploding
                const timeLeft = bomb.timer / 600; // Normalize to 0-1
                const pulseIntensity = 0.3 + 0.7 * (1 - timeLeft); // More intense as timer decreases
                
                ctx.save();
                ctx.globalAlpha = pulseIntensity * 0.5;
                ctx.fillStyle = '#ff0000';
                ctx.beginPath();
                ctx.arc(drawX + tileSize/2, drawY + tileSize/2, tileSize/2, 0, 2 * Math.PI);
                ctx.fill();
                ctx.restore();
            });
        }
        
        function drawCrashes() {
            const tileSize = window.gameTileSize || 30;
            const hudHeight = 80; // Height of HUD area
            
            crashPositions.forEach(crash => {
                const drawX = crash.x * tileSize;
                const drawY = crash.y * tileSize + hudHeight;
                
                if (crashImageLoaded && crashImage) {
                    // Draw crash with image
                    ctx.drawImage(crashImage, drawX, drawY, tileSize, tileSize);
                    console.log('Drawing crash image at:', drawX, drawY);
                } else {
                    // Fallback to orange circle while image loads
                    ctx.fillStyle = '#ff8c00';
                    ctx.beginPath();
                    ctx.arc(drawX + tileSize/2, drawY + tileSize/2, tileSize/3, 0, 2 * Math.PI);
                    ctx.fill();
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    console.log('Drawing fallback orange circle - image not loaded');
                }
                
                // Removed glowing orange overlay for Doc Ock crash blocker
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
                        } else if (villain.type === 'Mysterio' && villainAbilities.illusion.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Electro' && villainAbilities.lightning.active) {
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
                        } else if (villain.type === 'Mysterio' && villainAbilities.illusion.active) {
                            isVillainUsingSpecialPower = true;
                        } else if (villain.type === 'Electro' && villainAbilities.lightning.active) {
                            isVillainUsingSpecialPower = true;
                        }
                        
                        // Player loses life (2 if villain is using special power, 1 otherwise)
                        if (isVillainUsingSpecialPower) {
                            lives -= 2;
                        } else {
                            lives--;
                        }
                        
                        // Reset to spawn based on current level
                        if (currentLevel === 1) {
                            playerX = 13; // Level 1 spawn position
                        playerY = 12;
                        } else {
                            playerX = 15; // Level 2 spawn position (S in ASCII)
                            playerY = 9;
                        }
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
            const levelText = currentLevel === 1 ? 'Level 1: East Village' : 'Level 2: Times Square';
            ctx.fillText(levelText, canvas.width - tileSize * 10, hudY);
            
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
            if (villainAbilities.illusion.active) {
                ctx.fillStyle = '#4B0082';
                ctx.fillText('Mysterio: Illusion Gas!', canvas.width/2 - tileSize * 2.5, statusY + 20);
            }
            if (villainAbilities.lightning.active) {
                ctx.fillStyle = '#FFD700';
                ctx.fillText('Electro: Lights On!', canvas.width - tileSize * 10, statusY + 20);
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
            const processedMap = currentLevel === 1 ? processMazeWithFloodFill(currentMap) : currentMap;
            const newX = playerX;
            const newY = playerY;
            
            switch(event.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (newY > 0 && processedMap[newY - 1][newX] !== '#' && !hasCrash(newX, newY - 1)) {
                        playerY = newY - 1;
                        playerDirection = 'up';
                    }
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    // Subway teleport if on a subway sign (Level 2) and cooldown is ready
                    if (currentLevel === 2 && subwayTeleportCooldown === 0 && subwayPositions && subwayPositions.length === 2) {
                        const hereIdx = subwayPositions.findIndex(p => p.x === playerX && p.y === playerY);
                        if (hereIdx !== -1) {
                            const otherIdx = 1 - hereIdx;
                            playerX = subwayPositions[otherIdx].x;
                            playerY = subwayPositions[otherIdx].y;
                            playerDirection = 'down';
                            subwayTeleportCooldown = 20; // short lockout to prevent bounce
                            break;
                        }
                    }
                    if (newY < processedMap.length - 1 && processedMap[newY + 1][newX] !== '#' && !hasCrash(newX, newY + 1)) {
                        playerY = newY + 1;
                        playerDirection = 'down';
                    }
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (newX > 0 && processedMap[newY][newX - 1] !== '#' && !hasCrash(newX - 1, newY)) {
                        playerX = newX - 1;
                        playerDirection = 'left';
                    } else if (currentLevel === 1) {
                        // Level 1 wraparound logic
                        if (newX === 0 && newY === 13) {
                        // Wrap-around tunnel: left edge to right edge at row 14
                        playerX = processedMap[0].length - 1;
                        playerDirection = 'left';
                    } else if (newX === 0 && newY === 2) {
                        // Wrap-around tunnel: left edge row 3 to right edge row 2
                        playerX = processedMap[0].length - 1;
                        playerY = 1;
                        playerDirection = 'left';
                        }
                    } else if (currentLevel === 2) {
                        // Level 2 wraparound logic for R tiles
                        if (newX === 0 && (newY === 2 || newY === 12)) {
                            // Left R tile wraparound to right R tile
                            playerX = processedMap[0].length - 1;
                            playerDirection = 'left';
                        }
                    }
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (newX < processedMap[0].length - 1 && processedMap[newY][newX + 1] !== '#' && !hasCrash(newX + 1, newY)) {
                        playerX = newX + 1;
                        playerDirection = 'right';
                    } else if (currentLevel === 1) {
                        // Level 1 wraparound logic
                        if (newX === processedMap[0].length - 1 && newY === 13) {
                        // Wrap-around tunnel: right edge to left edge at row 14
                        playerX = 0;
                        playerDirection = 'right';
                    } else if (newX === processedMap[0].length - 1 && newY === 1) {
                        // Wrap-around tunnel: right edge row 2 to left edge row 3
                        playerX = 0;
                        playerY = 2;
                        playerDirection = 'right';
                        }
                    } else if (currentLevel === 2) {
                        // Level 2 wraparound logic for R tiles
                        if (newX === processedMap[0].length - 1 && (newY === 2 || newY === 12)) {
                            // Right R tile wraparound to left R tile
                            playerX = 0;
                            playerDirection = 'right';
                        }
                    }
                    break;
            }
            
            // Check for dust collection
            checkDustCollection();
            checkWebShooterCollection();
            checkTaxiStopCollection();
            checkBombCollision();
        }
        
        function checkDustCollection() {
            const dustIndex = dustPositions.findIndex(dust => dust.x === playerX && dust.y === playerY);
            if (dustIndex !== -1) {
                dustPositions.splice(dustIndex, 1);
                dustCollected++;
                score += 10;
                
                // Start waka waka sound when collecting dust (disabled)
                // startWakaWakaSound();
                
                // Clear any existing timeout (disabled)
                // if (wakaWakaTimeout) {
                //     clearTimeout(wakaWakaTimeout);
                // }
                
                // Stop waka waka sound after 500ms if no more dust is collected (disabled)
                // wakaWakaTimeout = setTimeout(() => {
                //     stopWakaWakaSound();
                // }, 500);
            }
            // Camera collection (Level 2 only)
            if (currentLevel === 2 && cameraPosition && playerX === cameraPosition.x && playerY === cameraPosition.y) {
                cameraPosition = null; // collected
                score += 50;
                console.log('Camera collected! +50');
                // Trigger selfie overlay for 3 seconds
                selfieTimer = 120;
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
                
                // Set specific taxi direction based on level and position
                if (currentLevel === 2 && playerX === 12 && playerY === 1) {
                    // Level 2 left-side taxi (top) - always go left
                    taxiDirection = 'left';
                } else {
                    // All other taxis: Use player direction
                taxiDirection = playerDirection;
                }
                
                taxiMoveTimer = 0;
                score += 25;
                
                // Remove taxi from collection list
                taxiStopPositions.splice(taxiIndex, 1);
            }
        }
        
        function checkBombCollision() {
            // Check if player is on a bomb position
            const bombIndex = bombPositions.findIndex(bomb => bomb.x === playerX && bomb.y === playerY);
            if (bombIndex !== -1) {
                console.log(`Spider-Man hit a bomb at (${playerX}, ${playerY})!`);
                
                // Player loses a life
                lives--;
                
                // Remove the bomb that was hit
                bombPositions.splice(bombIndex, 1);
                
                // Reset player position based on current level
                if (currentLevel === 1) {
                    playerX = 13; // Level 1 spawn position
                    playerY = 12;
                } else {
                    playerX = 15; // Level 2 spawn position (S in ASCII)
                    playerY = 9;
                }
                
                console.log(`Spider-Man respawned at (${playerX}, ${playerY}) with ${lives} lives remaining`);
            }
        }
        
        function updateTaxiRide() {
            if (!isRidingTaxi) return;
            
            taxiMoveTimer += taxiSpeed;
            
            if (taxiMoveTimer >= 1) {
                taxiMoveTimer = 0;
                
                const processedMap = currentLevel === 1 ? processMazeWithFloodFill(level1Map) : level2Map;
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
            // Guard: only valid from cutscenes
            if (currentState !== 'win' && currentState !== 'lose' && currentState !== 'gameOver' && currentState !== 'victoryComic') {
                console.log('returnToTitle ignored: currentState=', currentState);
                return;
            }
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
            
            // Branch by currentLevel: after Level 1 → Times Square victory; after Level 2 → Level 3 Intro cutscene
            if (currentLevel === 1) {
                console.log('🔥 Transition: Level 1 → Level 2 victory comic');
                console.log('🔥 Setting state to victoryComic...');
                currentState = 'victoryComic';
                currentVictoryPanel = 0;
                console.log('🔥 Calling showVictoryPanel(0)...');
                showVictoryPanel(0);
            } else if (currentLevel === 2) {
                console.log('🔥 Transition: Level 2 → Level 3 Intro cutscene');
                // Stop Level 2 music when the round ends
                stopBackgroundMusic();
                startLevel3IntroCutscene();
            } else {
                // Fallback: default to title
                console.log('⚠️ Unknown level transition. Returning to title.');
                const title = document.getElementById('titleScreen');
                if (title) {
                    title.style.display = 'block';
                    title.classList.add('active');
                }
                currentState = 'title';
            }
            
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
            
            // Reset Electro flash effect
            electroFlashActive = false;
            electroFlashTimer = 0;
            
            // Reset Mysterio flash effect
            mysterioFlashActive = false;
            mysterioFlashTimer = 0;
            
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

        // === Level 3 Intro Cutscene Logic ===
        let level3IntroPanelIndex = 0;
        const totalLevel3IntroPanels = 5; // 0..4 (adds Spider-Man quip panel)

        function showLevel3IntroPanel(index) {
            // Hide all level 3 intro panels
            document.querySelectorAll('[id^="level3IntroPanel"]').forEach(p => {
                p.classList.remove('active');
                p.style.display = 'none';
                p.style.visibility = 'hidden';
            });
            const panel = document.getElementById(`level3IntroPanel${index}`);
            if (panel) {
                // Forcefully ensure the panel is visible above everything
                panel.classList.add('active');
                panel.style.display = 'flex';
                panel.style.position = 'fixed';
                panel.style.top = '0';
                panel.style.left = '0';
                panel.style.width = '100vw';
                panel.style.height = '100vh';
                panel.style.visibility = 'visible';
                panel.style.opacity = '1';
                panel.style.zIndex = '9999';

                // Hide the canvas to avoid any overlapping artifacts
                const canvas = document.getElementById('gameCanvas');
                if (canvas) {
                    canvas.style.display = 'none';
                }
            }
        }

        function nextLevel3IntroPanel() {
            if (level3IntroPanelIndex < totalLevel3IntroPanels - 1) {
                level3IntroPanelIndex++;
                showLevel3IntroPanel(level3IntroPanelIndex);
            } else {
                // End of intro → proceed to Level 3 splash
                // Hide intro panels before transitioning
                document.querySelectorAll('[id^="level3IntroPanel"]').forEach(p => {
                    p.classList.remove('active');
                    p.style.display = 'none';
                    p.style.visibility = 'hidden';
                });
                startLevel3Splash();
            }
        }

        function startLevel3IntroCutscene() {
            console.log('=== startLevel3IntroCutscene() ===');
            currentState = 'level3Intro';
            level3IntroPanelIndex = 0;
            // Click anywhere to advance panels (handled in global click/keydown)
            showLevel3IntroPanel(0);
        }

        function startLevel3Splash() {
            console.log('=== startLevel3Splash() ===');
            // Hide any intro panels
            document.querySelectorAll('[id^="level3IntroPanel"]').forEach(p => {
                p.classList.remove('active');
                p.style.display = 'none';
                p.style.visibility = 'hidden';
            });
            // Prepare canvas splash
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            canvas.style.display = 'block';
            currentState = 'level3Splash';
            currentLevel = 3;
            // Ensure Level 3 music starts at splash
            if (typeof switchToLevel3Music === 'function') {
                switchToLevel3Music();
            }
            // Draw simple splash
            // Draw styled splash with building theme
            ctx.fillStyle = '#0b0b16';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            grad.addColorStop(0, '#351a4a');
            grad.addColorStop(0.5, '#0b0b16');
            grad.addColorStop(1, '#000');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.textAlign = 'center';
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 6;
            ctx.fillStyle = '#ff2d2d';
            ctx.font = 'bold 52px Comic Sans MS';
            ctx.strokeText('LEVEL 3: EMPIRE RUSH', canvas.width/2, canvas.height/2 - 40);
            ctx.fillText('LEVEL 3: EMPIRE RUSH', canvas.width/2, canvas.height/2 - 40);
            ctx.fillStyle = '#ffffff';
            ctx.font = '20px Comic Sans MS';
            ctx.fillText('Vertical maze ascent — reach the top!', canvas.width/2, canvas.height/2 + 4);
            ctx.font = '16px Comic Sans MS';
            ctx.fillText('Press SPACE or Click to continue', canvas.width/2, canvas.height/2 + 36);

            // Background image splash with Empire skyline
            const bg = new Image();
            bg.onload = function() {
                const iw = bg.naturalWidth;
                const ih = bg.naturalHeight;
                const scale = Math.max(canvas.width / iw, canvas.height / ih);
                const dw = Math.ceil(iw * scale);
                const dh = Math.ceil(ih * scale);
                const dx = Math.floor((canvas.width - dw) / 2);
                const dy = Math.floor((canvas.height - dh) / 2);
                ctx.drawImage(bg, dx, dy, dw, dh);
                drawSplashText();
            };
            bg.onerror = function() {
                // Fallback gradient
                ctx.fillStyle = '#0b0b16';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
                grad.addColorStop(0, '#351a4a');
                grad.addColorStop(0.5, '#0b0b16');
                grad.addColorStop(1, '#000');
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                drawSplashText();
            };
            bg.src = '/static/Empire%20View.jpg';

            function drawSplashText() {
            ctx.textAlign = 'center';
                ctx.strokeStyle = 'rgba(0,0,0,0.75)';
                ctx.lineWidth = 6;
                ctx.fillStyle = '#ff2d2d';
                ctx.font = 'bold 52px Comic Sans MS';
                ctx.strokeText('LEVEL 3: EMPIRE RUSH', canvas.width/2, canvas.height/2 - 40);
                ctx.fillText('LEVEL 3: EMPIRE RUSH', canvas.width/2, canvas.height/2 - 40);
                ctx.fillStyle = '#ffffff';
                ctx.font = '20px Comic Sans MS';
                ctx.fillText('Vertical maze ascent — reach the top!', canvas.width/2, canvas.height/2 + 4);
                ctx.font = '16px Comic Sans MS';
                ctx.fillText('Press SPACE or Click to continue', canvas.width/2, canvas.height/2 + 36);
            }
        }

        function startLevel3Placeholder() {
            console.log('=== startLevel3Placeholder() ===');
            // Deprecated: replaced by startLevel3DesignOnly
            startLevel3DesignOnly();
        }

        // Level 3 design-only renderer (no characters/villains yet)
        function startLevel3DesignOnly() {
            console.log('=== startLevel3DesignOnly() ===');
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            canvas.style.display = 'block';
            canvas.style.border = 'none';
            currentState = 'gameplay';
            // Switch to Level 3 music on loop
            if (typeof switchToLevel3Music === 'function') {
                switchToLevel3Music();
            }

            // Prepare rotated map: rotate 90° so original LEFT becomes BOTTOM,
            // then force 'S' to bottom-left as requested
            function rotateClockwise(mapArr) {
                const r = mapArr.length;
                const c = mapArr[0].length;
                const out = Array.from({ length: c }, () => Array(r).fill(' '));
                for (let y = 0; y < r; y++) {
                    for (let x = 0; x < c; x++) {
                        out[x][r - 1 - y] = mapArr[y][x];
                    }
                }
                return out.map(row => row.join(''));
            }

            function ensureStartAtBottomLeft(mapArr) {
                const r = mapArr.length;
                const c = mapArr[0].length;
                let sx = -1, sy = -1;
                for (let y = 0; y < r; y++) {
                    const ix = mapArr[y].indexOf('S');
                    if (ix !== -1) { sy = y; sx = ix; break; }
                }
                if (sx !== -1) {
                    // Replace old S with path
                    mapArr[sy] = mapArr[sy].substring(0, sx) + '.' + mapArr[sy].substring(sx + 1);
                }
                // Set bottom-left to 'S' if it's a wall, carve a path
                const by = r - 1, bx = 0;
                const ch = mapArr[by][bx];
                const replacement = 'S';
                mapArr[by] = replacement + mapArr[by].substring(1);
                return mapArr;
            }

            function mirrorVertical(mapArr) {
                return mapArr.map(row => row.split('').reverse().join(''));
            }

            function mirrorHorizontal(mapArr) {
                // Reverse the order of rows
                return mapArr.slice().reverse();
            }

            let mapData = rotateClockwise(level3Map);
            // Flip across horizontal axis (top-bottom)
            mapData = mirrorHorizontal(mapData);
            mapData = ensureStartAtBottomLeft(mapData);

            // Compute tile size for a zoomed-in viewport centered on Spider-Man
            const rows = mapData.length;
            const cols = mapData[0].length;
            const viewTilesX = 11; // visible tiles horizontally
            const viewTilesY = 11; // visible tiles vertically
            const maxWidth = window.innerWidth * 0.98;
            const maxHeight = window.innerHeight * 0.85;
            const tileSize = Math.min(
                Math.floor(maxWidth / viewTilesX),
                Math.floor(maxHeight / viewTilesY),
                64
            );
            canvas.width = viewTilesX * tileSize;
            canvas.height = viewTilesY * tileSize;

            // Offscreen buffer for static map to prevent flicker
            const mapCanvas = document.createElement('canvas');
            mapCanvas.width = cols * tileSize;
            mapCanvas.height = rows * tileSize;
            const mapCtx = mapCanvas.getContext('2d');

            // Cache textures once
            const wallImg = new Image();
            let wallReady = false;
            wallImg.onload = function() { wallReady = true; renderStaticMap(); renderFrame(); };
            wallImg.onerror = function() { wallReady = false; renderStaticMap(); renderFrame(); };
            wallImg.src = '/static/Square.png';

            const walkImg = new Image();
            let walkReady = false;
            walkImg.onload = function() { walkReady = true; renderStaticMap(); renderFrame(); };
            walkImg.onerror = function() { walkReady = false; renderStaticMap(); renderFrame(); };
            walkImg.src = '/static/Walkable%203.png';

            function renderStaticMap() {
                // Draw the static grid to offscreen canvas
                mapCtx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
                for (let y = 0; y < rows; y++) {
                    for (let x = 0; x < cols; x++) {
                        const ch = mapData[y][x];
                        const px = x * tileSize;
                        const py = y * tileSize;
                        if (ch === '#') {
                            if (wallReady) {
                                const iw = wallImg.naturalWidth;
                                const ih = wallImg.naturalHeight;
                                const scale = Math.max(tileSize / iw, tileSize / ih);
                                const dw = Math.ceil(iw * scale);
                                const dh = Math.ceil(ih * scale);
                                const dx = Math.floor(px + (tileSize - dw) / 2);
                                const dy = Math.floor(py + (tileSize - dh) / 2);
                                mapCtx.save();
                                mapCtx.beginPath();
                                mapCtx.rect(px, py, tileSize, tileSize);
                                mapCtx.clip();
                                mapCtx.drawImage(wallImg, dx, dy, dw, dh);
                                mapCtx.restore();
                            } else {
                                mapCtx.fillStyle = '#2a2f3a';
                                mapCtx.fillRect(px, py, tileSize, tileSize);
                                mapCtx.strokeStyle = '#4c5566';
                                mapCtx.strokeRect(px + 0.5, py + 0.5, tileSize - 1, tileSize - 1);
                            }
                        } else if (ch === 'S') {
                            mapCtx.fillStyle = '#14203a';
                            mapCtx.fillRect(px, py, tileSize, tileSize);
                            mapCtx.fillStyle = '#00bfff';
                            mapCtx.font = `${Math.floor(tileSize * 0.6)}px Comic Sans MS`;
                            mapCtx.textAlign = 'center';
                            mapCtx.textBaseline = 'middle';
                            mapCtx.fillText('S', px + tileSize / 2, py + tileSize / 2);
                        } else if (ch === 'G') {
                            mapCtx.fillStyle = '#1d2a4d';
                            mapCtx.fillRect(px, py, tileSize, tileSize);
                            mapCtx.fillStyle = '#ff2d2d';
                            mapCtx.font = `${Math.floor(tileSize * 0.6)}px Comic Sans MS`;
                            mapCtx.textAlign = 'center';
                            mapCtx.textBaseline = 'middle';
                            mapCtx.fillText('G', px + tileSize / 2, py + tileSize / 2);
                        } else {
                            if (walkReady) {
                                const iw = walkImg.naturalWidth;
                                const ih = walkImg.naturalHeight;
                                const scale = Math.max(tileSize / iw, tileSize / ih);
                                const dw = Math.ceil(iw * scale);
                                const dh = Math.ceil(ih * scale);
                                const dx = Math.floor(px + (tileSize - dw) / 2);
                                const dy = Math.floor(py + (tileSize - dh) / 2);
                                mapCtx.drawImage(walkImg, dx, dy, dw, dh);
                            } else {
                                mapCtx.fillStyle = '#101521';
                                mapCtx.fillRect(px, py, tileSize, tileSize);
                            }
                        }
                    }
                }
            }

            function renderGooOverlay(cameraX, cameraY) {
                // Draw goo overlays for tiles the Lizard has traversed
                if (!gooTiles || gooTiles.size === 0) return;
                const startX = Math.floor(cameraX / tileSize);
                const startY = Math.floor(cameraY / tileSize);
                const endX = startX + Math.ceil(canvas.width / tileSize) + 1;
                const endY = startY + Math.ceil(canvas.height / tileSize) + 1;
                for (const key of gooTiles) {
                    const [gxStr, gyStr] = key.split(',');
                    const gx = parseInt(gxStr, 10);
                    const gy = parseInt(gyStr, 10);
                    if (gx < startX || gx > endX || gy < startY || gy > endY) continue;
                    const px = gx * tileSize - cameraX;
                    const py = gy * tileSize - cameraY;
                    if (gooReady) {
                        const iw = gooImg.naturalWidth;
                        const ih = gooImg.naturalHeight;
                        const scale = Math.max(tileSize / iw, tileSize / ih);
                        const dw = Math.ceil(iw * scale);
                        const dh = Math.ceil(ih * scale);
                        const dx = Math.floor(px + (tileSize - dw) / 2);
                        const dy = Math.floor(py + (tileSize - dh) / 2);
                        ctx.drawImage(gooImg, dx, dy, dw, dh);
                    } else {
                        ctx.fillStyle = 'rgba(0, 180, 0, 0.5)';
                        ctx.fillRect(px, py, tileSize, tileSize);
                    }
                }
            }

            function renderDustOverlay(cameraX, cameraY) {
                // Draw dust pellets for remaining dustPositions with camera offset
                if (!dustPositions || dustPositions.length === 0) return;
                ctx.fillStyle = '#ffffff';
                const startX = Math.floor(cameraX / tileSize);
                const startY = Math.floor(cameraY / tileSize);
                const endX = startX + Math.ceil(canvas.width / tileSize) + 1;
                const endY = startY + Math.ceil(canvas.height / tileSize) + 1;
                for (const d of dustPositions) {
                    if (d.x < startX || d.x > endX || d.y < startY || d.y > endY) continue;
                    const px = d.x * tileSize - cameraX;
                    const py = d.y * tileSize - cameraY;
                    ctx.beginPath();
                    const r = Math.max(2, Math.floor(tileSize * 0.12));
                    ctx.arc(px + tileSize / 2, py + tileSize / 2, r, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            function renderFrame() {
                // Camera centered on player
                const camCenterX = playerX * tileSize + tileSize / 2;
                const camCenterY = playerY * tileSize + tileSize / 2;
                let cameraX = Math.floor(camCenterX - canvas.width / 2);
                let cameraY = Math.floor(camCenterY - canvas.height / 2);
                // Clamp to map bounds
                cameraX = Math.max(0, Math.min(cameraX, mapCanvas.width - canvas.width));
                cameraY = Math.max(0, Math.min(cameraY, mapCanvas.height - canvas.height));

                // Center circular viewport on player's screen position so Spidey is always visible
                const playerScreenX = Math.floor(playerX * tileSize - cameraX + tileSize / 2);
                const playerScreenY = Math.floor(playerY * tileSize - cameraY + tileSize / 2);
                const cx = playerScreenX;
                const cy = playerScreenY;
                const radius = Math.floor(Math.min(canvas.width, canvas.height) * 0.48);

                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Clip to circle for round viewport
                ctx.save();
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.clip();

                // Draw world within circular clip
                ctx.drawImage(
                    mapCanvas,
                    cameraX,
                    cameraY,
                    canvas.width,
                    canvas.height,
                    0,
                    0,
                    canvas.width,
                    canvas.height
                );
                // Goo goes under dust so pellets remain visible
                renderGooOverlay(cameraX, cameraY);
                renderDustOverlay(cameraX, cameraY);
                if (typeof drawLevel3Lizard === 'function') { drawLevel3Lizard(cameraX, cameraY); }
                drawLevel3Player(cameraX, cameraY);
                ctx.restore();

                // Circular fade border (vignette)
                ctx.save();
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.clip();
                const fade = ctx.createRadialGradient(cx, cy, Math.max(1, radius * 0.82), cx, cy, radius);
                fade.addColorStop(0, 'rgba(0,0,0,0)');
                fade.addColorStop(1, 'rgba(0,0,0,0.35)');
                ctx.fillStyle = fade;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.restore();

                // Draw Level 3 HUD (points, lives, title) above the board
                drawLevel3HUD();
            }

            function drawLevel3HUD() {
                const hudY = 28;
                ctx.save();
                ctx.textBaseline = 'middle';
                let baseFontSize = 20;
                ctx.font = `bold ${baseFontSize}px Comic Sans MS`;
                ctx.lineWidth = 4;
                ctx.strokeStyle = 'rgba(0,0,0,0.7)';
                ctx.fillStyle = '#ffffff';

                // Lives (left)
                const livesText = `Lives: ${lives}`;
                const livesX = 16;
                ctx.strokeText(livesText, livesX, hudY);
                ctx.fillText(livesText, livesX, hudY);
                const livesWidth = ctx.measureText(livesText).width;

                // Precompute Level title (right) metrics and position
                const titleText = 'Level 3: Empire State Blitz';
                const minGap = 24; // gap between lives text and title
                let titleFontSize = baseFontSize;
                let titleWidth = ctx.measureText(titleText).width;
                let availableRight = canvas.width - (livesX + livesWidth + minGap) - 16;
                while (titleWidth > availableRight && titleFontSize > 12) {
                    titleFontSize -= 1;
                    ctx.font = `bold ${titleFontSize}px Comic Sans MS`;
                    titleWidth = ctx.measureText(titleText).width;
                    availableRight = canvas.width - (livesX + livesWidth + minGap) - 16;
                }
                const titleX = Math.max(livesX + livesWidth + minGap, canvas.width - titleWidth - 16);

                // Score (center between lives and title)
                let scoreFontSize = baseFontSize;
                ctx.font = `bold ${scoreFontSize}px Comic Sans MS`;
                const scoreText = `Score: ${score}`;
                let scoreWidth = ctx.measureText(scoreText).width;
                const leftEdge = livesX + livesWidth + minGap;
                const midAvailable = titleX - leftEdge;
                while (scoreWidth > (midAvailable - minGap) && scoreFontSize > 12) {
                    scoreFontSize -= 1;
                    ctx.font = `bold ${scoreFontSize}px Comic Sans MS`;
                    scoreWidth = ctx.measureText(scoreText).width;
                }
                const scoreX = Math.floor(leftEdge + (midAvailable - scoreWidth) / 2);
                ctx.strokeText(scoreText, scoreX, hudY);
                ctx.fillText(scoreText, scoreX, hudY);

                // Draw Level title (right)
                ctx.font = `bold ${titleFontSize}px Comic Sans MS`;
                ctx.strokeText(titleText, titleX, hudY);
                ctx.fillText(titleText, titleX, hudY);

                ctx.restore();
            }

            // Level 3: single life
            lives = 1;

            // Populate dust for every walkable path tile ('.') in Level 3 design
            dustPositions = [];
            totalDust = 0;
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < cols; x++) {
                    const ch = mapData[y][x];
                    if (ch === '.') {
                        dustPositions.push({ x, y });
                        totalDust++;
                    }
                }
            }

            // Goo trail: track all tiles the Lizard steps on (permanent)
            const gooTiles = new Set(); // keys formatted as "x,y"
            const gooImg = new Image();
            let gooReady = false;
            gooImg.onload = function() { gooReady = true; paintAll(); };
            gooImg.onerror = function() { gooReady = false; };
            gooImg.src = '/static/Goo.png';

            function addGooAt(gx, gy) {
                gooTiles.add(gx + ',' + gy);
            }

            // Track Level 3 spawn (S) and set player position
            let level3SpawnX = 0;
            let level3SpawnY = 0;
            (function setLevel3Spawn() {
                for (let y = 0; y < rows; y++) {
                    const ix = mapData[y].indexOf('S');
                    if (ix !== -1) {
                        playerX = ix;
                        playerY = y;
                        level3SpawnX = ix;
                        level3SpawnY = y;
                        break;
                    }
                }
            })();

            // Expose processed map for Level 3 controls
            window.level3ProcessedMap = mapData;
            let playerRotation = 0; // radians; 0 = facing up
            let playerFlipX = false; // flip on vertical axis each move

            // --- Lizard (enemy) setup ---
            let lizardX = playerX;
            let lizardY = playerY;
            let lizardActive = false;
            let lizardRotation = 0;
            let lizardFlipX = false;
            const lizardImg = new Image();
            let lizardReady = false;
            lizardImg.onload = function() { lizardReady = true; paintAll(); };
            lizardImg.onerror = function() { lizardReady = false; };
            lizardImg.src = '/static/Lizard.png';
            if (window.level3LizardInterval) { clearInterval(window.level3LizardInterval); window.level3LizardInterval = null; }

            // Simple draw uses the offscreen map buffer with a camera centered on the player
            function drawLevel3Grid() {
                renderFrame();
            }

            // Draw Spider-Man on the grid
            const level3SpideyImg = new Image();
            let level3SpideyReady = false;
            level3SpideyImg.onload = function() { level3SpideyReady = true; paintAll(); };
            level3SpideyImg.onerror = function() { level3SpideyReady = false; paintAll(); };
            // Choose Miles vs Spider-Man climbing sprite for Level 3
            level3SpideyImg.src = (typeof selectedSpider !== 'undefined' && selectedSpider === 'miles')
                ? '/static/Miles Morales Climbing.png'
                : '/static/Spider-man%20climb.png';

            function drawLevel3Player(cameraX = 0, cameraY = 0) {
                const px = playerX * tileSize - cameraX;
                const py = playerY * tileSize - cameraY;
                const cx = px + tileSize / 2;
                const cy = py + tileSize / 2;
                if (level3SpideyReady) {
                    // Draw the sprite using contain scaling with extra padding; rotate based on movement
                    const iw = level3SpideyImg.naturalWidth;
                    const ih = level3SpideyImg.naturalHeight;
                    const maxDrawW = Math.floor(tileSize * 0.88);
                    const maxDrawH = Math.floor(tileSize * 0.88);
                    const scale = Math.min(maxDrawW / iw, maxDrawH / ih);
                    const dw = Math.max(1, Math.round(iw * scale));
                    const dh = Math.max(1, Math.round(ih * scale));
                    ctx.save();
                    ctx.translate(cx, cy);
                    ctx.rotate(playerRotation);
                    ctx.scale(playerFlipX ? -1 : 1, 1);
                    ctx.drawImage(level3SpideyImg, Math.floor(-dw / 2), Math.floor(-dh / 2), dw, dh);
                    ctx.restore();
                } else {
                    // Fallback: red dot
                    ctx.fillStyle = '#ff2d2d';
                    ctx.beginPath();
                    ctx.arc(cx, cy, Math.max(3, Math.floor(tileSize * 0.25)), 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            function paintAll() {
                drawLevel3Grid();
            }

            paintAll();

            function drawLevel3Lizard(cameraX = 0, cameraY = 0) {
                if (!lizardActive) return;
                const px = lizardX * tileSize - cameraX;
                const py = lizardY * tileSize - cameraY;
                const cx = px + tileSize / 2;
                const cy = py + tileSize / 2;
                if (lizardReady) {
                    const iw = lizardImg.naturalWidth;
                    const ih = lizardImg.naturalHeight;
                    const maxDrawW = Math.floor(tileSize * 0.98);
                    const maxDrawH = Math.floor(tileSize * 0.98);
                    const scale = Math.min(maxDrawW / iw, maxDrawH / ih);
                    const dw = Math.max(1, Math.round(iw * scale));
                    const dh = Math.max(1, Math.round(ih * scale));
                    ctx.save();
                    ctx.translate(cx, cy);
                    ctx.rotate(lizardRotation);
                    ctx.scale(lizardFlipX ? -1 : 1, 1);
                    // subtle shadow for visibility
                    ctx.shadowColor = 'rgba(0,0,0,0.35)';
                    ctx.shadowBlur = Math.max(2, Math.floor(tileSize * 0.1));
                    ctx.shadowOffsetX = 0;
                    ctx.shadowOffsetY = 0;
                    ctx.drawImage(lizardImg, Math.floor(-dw / 2), Math.floor(-dh / 2), dw, dh);
                    ctx.restore();
                } else {
                    ctx.fillStyle = '#3cb043';
                    ctx.beginPath();
                    ctx.arc(cx, cy, Math.max(3, Math.floor(tileSize * 0.25)), 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            function neighborsOf(x, y) {
                const result = [];
                const dirs = [ [1,0], [-1,0], [0,1], [0,-1] ];
                for (const [dx, dy] of dirs) {
                    const nx = x + dx;
                    const ny = y + dy;
                    if (ny >= 0 && ny < rows && nx >= 0 && nx < cols && mapData[ny][nx] !== '#') {
                        result.push([nx, ny]);
                    }
                }
                return result;
            }

            function computeNextStep(ax, ay, bx, by) {
                if (ax === bx && ay === by) return [ax, ay];
                const q = [];
                const visited = new Set();
                const prev = new Map();
                const startKey = ax + ',' + ay;
                q.push([ax, ay]);
                visited.add(startKey);
                let found = false;
                while (q.length) {
                    const [cx, cy] = q.shift();
                    if (cx === bx && cy === by) { found = true; break; }
                    for (const [nx, ny] of neighborsOf(cx, cy)) {
                        const key = nx + ',' + ny;
                        if (!visited.has(key)) {
                            visited.add(key);
                            prev.set(key, cx + ',' + cy);
                            q.push([nx, ny]);
                        }
                    }
                }
                if (!found) {
                    let best = [ax, ay];
                    let bestDist = Number.POSITIVE_INFINITY;
                    for (const [nx, ny] of neighborsOf(ax, ay)) {
                        const d = Math.abs(nx - bx) + Math.abs(ny - by);
                        if (d < bestDist) { bestDist = d; best = [nx, ny]; }
                    }
                    return best;
                }
                let curKey = bx + ',' + by;
                const path = [];
                while (curKey && curKey !== startKey) {
                    const [sx, sy] = curKey.split(',').map(Number);
                    path.push([sx, sy]);
                    curKey = prev.get(curKey);
                }
                path.reverse();
                return path.length ? path[0] : [ax, ay];
            }

            function setLizardFacing(dx, dy) {
                if (dy === 1) { lizardRotation = Math.PI; }
                else if (dy === -1) { lizardRotation = 0; }
                else if (dx === -1) { lizardRotation = -Math.PI / 2; }
                else if (dx === 1) { lizardRotation = Math.PI / 2; }
            }

            function startLizardChase() {
                lizardActive = true;
                // Spawn Lizard exactly where Spider-Man spawned initially
                lizardX = level3SpawnX;
                lizardY = level3SpawnY;
                // Leave goo at spawn
                addGooAt(lizardX, lizardY);
                // Immediately paint so Lizard appears as soon as he spawns
                paintAll();
                window.level3LizardInterval = setInterval(function() {
                    if (currentLevel !== 3 || currentState !== 'gameplay') return;
                    const [nx, ny] = computeNextStep(lizardX, lizardY, playerX, playerY);
                    const dx = nx - lizardX; const dy = ny - lizardY;
                    if (dx !== 0 || dy !== 0) {
                        lizardX = nx; lizardY = ny; lizardFlipX = !lizardFlipX; setLizardFacing(dx, dy);
                        addGooAt(lizardX, lizardY);
                    }
                    if (lizardX === playerX && lizardY === playerY) {
                        clearInterval(window.level3LizardInterval);
                        window.level3LizardInterval = null;
                        lizardActive = false;
                        // Level 3 lose immediately (one life only)
            currentLevel = 3;
                        showLoseScreen();
                        return;
                    }
                    paintAll();
                }, 220);
            }

            setTimeout(function() { if (currentLevel === 3 && currentState === 'gameplay') startLizardChase(); }, 3000);

            // Bind simple Level 3 movement controls (arrow keys / WASD)
            if (!window.level3ControlsBound) {
                window.level3ControlsBound = true;
                document.addEventListener('keydown', function(e) {
                    if (currentLevel !== 3 || currentState !== 'gameplay') return;
                    const map = window.level3ProcessedMap || mapData;
                    let dx = 0, dy = 0;
                    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') { dy = -1; }
                    else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') { dy = 1; }
                    else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') { dx = -1; }
                    else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') { dx = 1; }
                    else { return; }
                    e.preventDefault();
                    const nx = playerX + dx;
                    const ny = playerY + dy;
                    if (ny >= 0 && ny < map.length && nx >= 0 && nx < map[0].length && map[ny][nx] !== '#') {
                        playerX = nx;
                        playerY = ny;
                        // Update facing based on movement
                        if (dy === 1) { playerRotation = Math.PI; }
                        else if (dy === -1) { playerRotation = 0; }
                        else if (dx === -1) { playerRotation = -Math.PI / 2; } // left: 90° CCW
                        else if (dx === 1) { playerRotation = Math.PI / 2; }  // right: 90° CW
                        // Toggle flip each step
                        playerFlipX = !playerFlipX;
                        // Collect dust if present
                        checkDustCollection();
                        paintAll();
                    }
                });
            }

            // Overlay now drawn inside paintAll beneath the player
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
            const isButton = (e.target.tagName === 'BUTTON' || e.target.closest('button'));
            // During character select, ignore ALL non-button clicks silently
            if (!isButton && currentState === 'characterSelect') {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            
            // Log only when not in characterSelect background
            if (!(currentState === 'characterSelect' && !isButton)) {
            console.log('Click detected, currentState:', currentState);
            }
            if (currentState === 'title') {
                startGame();
            } else if (currentState === 'comic') {
                // Require character selection before advancing from first panel
                if ((currentPanel === -1 || currentPanel === 0) && !characterChosen) {
                    // flash overlay to prompt selection
                    const overlay = document.getElementById('comicCharacterSelect');
                    if (overlay) {
                        overlay.style.display = 'flex';
                        overlay.animate([
                            { transform: 'scale(1)', filter: 'brightness(1)' },
                            { transform: 'scale(1.03)', filter: 'brightness(1.3)' },
                            { transform: 'scale(1)', filter: 'brightness(1)' }
                        ], { duration: 300 });
                    }
                    return;
                }
                nextPanel();
            } else if (currentState === 'victoryComic') {
                nextVictoryPanel();
            } else if (currentState === 'level3Intro') {
                nextLevel3IntroPanel();
            } else if (currentState === 'level3Splash') {
                startLevel3DesignOnly();
            } else if (currentState === 'gameplay') {
                // Only handle Level 1/2 splash-skip logic here; ignore for Level 3
                if (currentLevel === 1 || currentLevel === 2) {
                const currentLevelState = currentLevel === 1 ? level1State : level2State;
                if (currentLevelState === 'splash') {
                    if (currentLevel === 1) {
                        level1State = 'gameplay';
                    } else {
                        level2State = 'gameplay';
                    }
                    initGameplay();
                    }
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
                } else if (currentState === 'level3Intro') {
                    nextLevel3IntroPanel();
                } else if (currentState === 'level3Splash') {
                    startLevel3DesignOnly();
                } else if (currentState === 'gameplay') {
                    // Only apply to Level 1/2, never Level 3
                    if (currentLevel === 1 || currentLevel === 2) {
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
        
        // CHEAT CODE: Jump directly to Times Square comic sequence
        function cheatToTimesSquareComic() {
            console.log('🔥🔥🔥 CHEAT CODE ACTIVATED: Jumping to Times Square comic sequence! 🔥🔥🔥');
            
            // Hide all screens first
            document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(panel => {
                panel.classList.remove('active');
                panel.style.display = 'none';
            });
            
            // Hide game canvas if it exists
            const canvas = document.getElementById('gameCanvas');
            if (canvas) canvas.style.display = 'none';
            
            // Set up victory comic state
            currentState = 'victoryComic';
            currentVictoryPanel = 0;
            totalVictoryPanels = 5; // 5 panels: 0, 1, 2, 3, 4
            
            console.log('🔥 Cheat: Setting up Times Square comic...');
            console.log('🔥 Current state:', currentState);
            console.log('🔥 Current victory panel:', currentVictoryPanel);
            console.log('🔥 Total victory panels:', totalVictoryPanels);
            
            // Show the first victory panel
            showVictoryPanel(0);
            
            console.log('🔥🔥🔥 CHEAT COMPLETE: You should now see the Times Square comic sequence! 🔥🔥🔥');
            console.log('🔥 Click to advance through the comic panels');
        }
        
        window.cheatToTimesSquareComic = cheatToTimesSquareComic;
        
        // CHEAT CODE: Jump to END of Level 2 cutscene (Level 3 intro final panel)
        function cheatToEndOfLevel2Cutscene() {
            console.log('🔥🔥🔥 CHEAT CODE ACTIVATED: Jumping to END of Level 2 cutscene (Level 3 Intro final panel)! 🔥🔥🔥');
            try {
                // Hide all other UI first
                document.querySelectorAll('.comic-panel, .victory-panel, #titleScreen').forEach(panel => {
                    panel.classList.remove('active');
                    panel.style.display = 'none';
                });
                const canvas = document.getElementById('gameCanvas');
                if (canvas) canvas.style.display = 'none';

                // Ensure state reflects post-Level-2 flow
                currentLevel = 2; // Still considered Level 2 until splash sets Level 3
                currentState = 'level3Intro';

                // Initialize the Level 3 intro handlers (skip/continue)
                startLevel3IntroCutscene();

                // Start from the first Dr. Strange panel
                level3IntroPanelIndex = 0;
                showLevel3IntroPanel(0);

                console.log('✅ Now showing final Level 3 intro panel with Continue button.');
                console.log('👉 Click anywhere to advance through the Level 3 intro panels.');
            } catch (e) {
                console.error('❌ Cheat to end of Level 2 cutscene failed:', e);
            }
        }
        window.cheatToEndOfLevel2Cutscene = cheatToEndOfLevel2Cutscene;
        
        // Debug function to check image loading status
        function debugImageLoading() {
            console.log('🔍 Image Loading Debug:');
            console.log('- bombImageLoaded:', bombImageLoaded);
            console.log('- bombImage exists:', !!bombImage);
            console.log('- crashImageLoaded:', crashImageLoaded);
            console.log('- crashImage exists:', !!crashImage);
        }
        
        window.debugImageLoading = debugImageLoading;
        
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
            // Character select buttons (add robust handlers to stop bubbling)
            const startIntroBtn = document.getElementById('startIntroBtn');
            const chooseSpiderManBtn = document.getElementById('chooseSpiderManBtn');
            const chooseMilesBtn = document.getElementById('chooseMilesBtn');
            if (startIntroBtn) {
                startIntroBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    goToIntroComic();
                });
            }
            if (chooseSpiderManBtn) {
                chooseSpiderManBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    chooseSpider('spiderman');
                });
            }
            if (chooseMilesBtn) {
                chooseMilesBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    chooseSpider('miles');
                });
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

# Vercel deployment - only run if this is the main module
if __name__ == "__main__":
    print("🕷️ Spider-Run Game Server Starting...")
    print("🎮 Your game will be available at http://localhost:8081")
    print("📖 Comic book style intro sequence ready!")
    print("🎯 Click to advance through Dr. Strange and Spider-Man dialogue")
    app.run(debug=True, host='0.0.0.0', port=8081)
