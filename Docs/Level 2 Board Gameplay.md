# **PRD — Level 2 Gameplay (Spider-Run, Times Square)**

## **Purpose**

Define gameplay mechanics, states, rules, visuals, and transitions for Level 2 (“Times Square”). This level raises difficulty from Level 1 with **denser dust patterns, more enemies, brighter visuals, and stronger power-ups** — matching the chaotic, neon-lit Times Square setting.

---

## **Flow Overview**

### **Mid-Game Comic Cut Scene**

* Plays after Level 1 Win.

* Dr. Strange congratulates, Spider-Man quips, Strange reveals Times Square dust (already defined in cut-scene PRD).

* Ends → auto-transition to Level 2 splash.

---

### **Level Start Splash Screen**

* **Screen text:** “Level 2: Times Square.”

* **Style:** Comic cover panel — bold yellow/pink letters, neon billboard glow, silhouetted Times Square skyscrapers with flashing comic halftone “ads.”

* **Duration:** 2 seconds auto OR skip on button press (space/enter/controller A).

---

### **Gameplay Loop**

* Player spawns at maze start tile (below villain pen).

* Dust, villains, and orbs placed as defined in Level 2 Board Layout PRD.

* **Differences from Level 1:**

  * More dust clusters (denser maze).

  * Enemies: 4 active at once (instead of 3).

  * Faster enemy chase speed.

  * Larger, flashier orb effects.

* Runs until Win (dust cleared) or Lose (lives \= 0).

---

### **End of Level Transition**

* **Win:** Comic-style splash: “Times Square Saved\!” \+ Spider-Man quip. Then auto-transition (if more levels).

* **Lose:** “Game Over” comic panel, retry/exit menu.

---

## **Player Controls**

Same as Level 1:

* Keyboard: Arrow keys / WASD.

* Controller: Joystick / D-pad.

* Grid-based, instant reversal, corner queue.

---

## **Core Gameplay Rules**

### **Objectives**

* Collect all dust in maze.

* Avoid or defeat enemies.

### **Dust Collection**

* Each tile disappears on touch.

* \+10 points per dust.

### **Power-Ups (Enhanced Web Shooters / Strange Orbs)**

* Count: 6–8 on map.

* Look: Brighter than Level 1 (flashing neon outline, billboard glow).

* Effect:

  * Enemies vulnerable (flash brighter, pulse).

  * Speed boost (25% faster for 6 sec).

  * Web-shot ability (1–2 uses per orb, instead of just 1).

* Timer: 6 sec, flashing in last 2 sec.

### **Villains (Enemies)**

* Spawn inside villain pen.

* Count: **4 active at once** (red, blue, purple, green).

* Behavior AI:

  * Patrol → chase when Spider is in line of sight (longer range than Level 1).

  * Faster chase than Level 1\.

* Collision:

  * Active: player loses life, respawn at start.

  * Vulnerable: stunned → back to pen, \+200 points (reward higher for harder level).

* Respawn Delay: 1.5 seconds (shorter).

### **Lives**

* Start with whatever was carried from Level 1\.

* HUD shows Spider icons.

* Lose all → Game Over.

---

## **HUD (Heads-Up Display)**

Same structure as Level 1:

* Top Left: Lives.

* Top Center: Score.

* Top Right: Level indicator (“Level 2: Times Square”).

* Bottom: Optional speech bubble tutorial (e.g., “Watch those lights — the villains are faster here\!”).

---

## **Win/Loss States**

### **Win Condition**

* Dust cleared.

* Flashing neon (more chaotic colors than Level 1).

* Comic panel overlay: “Times Square Saved\!”

* Spider quip example: “Good thing I don’t charge for street cleaning…”

* Transition: If last level → game complete panel. If more levels → next cut scene.

### **Lose Condition**

* Lives \= 0\.

* Music fades, “Game Over” panel.

* Retry or Exit.

---

## **Visual Style**

### **General**

* Comic Book style (same as Level 1).

* Maze walls brighter neon (pink, yellow, green outlines like Times Square lights).

* Dust \= glowing specks with faint reflections (like glitter in neon).

* Orbs \= bigger, pulsing billboard-style glow.

* Villains \= distinct neon-colored costumes (so they pop).

### **Splash Screens**

* “Level 2: Times Square” in bold pink/yellow letters.

* Background: Simplified Times Square billboards and skyscraper silhouettes with comic halftone glow.

---

## **Audio / FX**

* **Music:** More intense, “arcade chiptune with neon flair.” Faster tempo than Level 1\.

* **SFX:**

  * Dust collect \= brighter “ding.”

  * Orb \= stronger neon “zap.”

  * Enemy stun \= “POW\!” comic punch sound.

  * Life lost \= dramatic “CRASH\!”

* **Transitions:** Comic page-flip sound.

---

## **Technical Requirements**

### **Game States Needed**

* Mid-Game Comic Cut Scene

* Level Splash

* Gameplay

* Win/Lose

### **Systems Needed**

* Same as Level 1 (grid movement, collision, timers, AI, HUD).

* Adjusted parameters (enemy count, speed, orb strength).

### **Fail Safes**

* Player can’t clip walls.

* Villains respawn in pen only.

* Dust/orbs reset on restart.

---

✨ **Final Summary:**  
 Level 2 keeps the **core Pac-Man-inspired loop** but raises difficulty: **4 enemies, denser dust, faster AI, flashier power-ups.** The setting is **Times Square**, shown through neon visuals, glowing billboards, and brighter comic design. Player wins by clearing dust and survives with carried-over lives. Win/loss states are consistent, with bolder colors and effects to reflect the chaos of Times Square.

