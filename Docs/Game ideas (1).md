# **PRD — Core Gameplay Systems (Spider-Run)**

## **Purpose**

Define the **main mechanics, rules, states, and systems** that power the Spider-Run game. This ensures every level (East Village, Times Square, or future ones) runs consistently, with difficulty tuned per-level.

---

## **Game Loop Overview**

1. **Comic Scene** (intro, cut, or ending).

   * Player advances panels → story delivery.

   * Ends automatically in gameplay or splash.

2. **Level Splash Screen.**

   * Comic-style panel announcing location (e.g., “Level 1: East Village”).

   * Auto-shows for 2 seconds or can be skipped.

3. **Main Gameplay.**

   * Player controls Spider-character in grid-based maze.

   * Objectives: collect all dust, avoid/defeat enemies.

4. **End of Level.**

   * **Win:** dust cleared → comic splash \+ Spider quip → next level/cut scene.

   * **Lose:** lives \= 0 → Game Over comic splash → Retry/Exit.

---

## **Player Controls**

* **Keyboard:** Arrow keys or WASD for 4-directional movement.

* **Controller:** D-pad or joystick for same input.

* **Movement Rules:**

  * Grid-based (1 tile per step).

  * Instant reversal (180°).

  * Corner queue: player can pre-input a turn before reaching tile edge (Pac-Man style).

---

## **Core Gameplay Rules**

### **Objectives**

* Collect all dust on the board.

* Survive enemy encounters.

* Use orbs/power-ups strategically.

---

### **Dust Collection**

* **Spawn:** All valid path tiles except spawn, villain pen, orb tiles.

* **Appearance:** Small glowing white/gray dots with faint sparkle.

* **Scoring:** \+10 points each.

* **Win Condition:** all dust collected.

---

### **Power-Ups (Web Shooters / Strange Orbs)**

* **Spawn:** 4–8 per map (per level design).

* **Appearance:** Larger glowing orbs with pulsing comic aura (blue/red/green depending on level).

* **On Collect:**

  1. **Enemy Vulnerability Mode:**

     * Villains flash colors.

     * Can be stunned if touched.

  2. **Speed Boost:** Player moves \+20–25% faster.

  3. **Web-Shot Ability:**

     * Key/button press to shoot one web.

     * Stuns nearest enemy in straight line (within range).

     * Number of uses depends on orb (1 in Level 1, 2 in Level 2, adjustable).

* **Duration:** 6 seconds (orb flashes in last 2 sec).

* **Score:** \+50 points for collecting orb.

---

### **Villains (Enemies)**

* **Spawn:** Inside villain pen at maze center.

* **Count:** Configurable by level (3 in Level 1, 4 in Level 2).

**AI Behavior:**

1. **Default:** Patrol maze randomly.

2. **Chase Mode:** If Spider-player enters line of sight (LOS), villain switches to chase.

   * Chase radius/detection increases by level.

   * Faster speed at higher levels.

3. **Retreat Mode:** If stunned by player, teleport back to pen after delay.

**Collision Outcomes:**

* **Normal Villain:** Spider loses 1 life → respawn at start.

* **Vulnerable Villain:**

  * Villain defeated.

  * Player gains points (+100 in Level 1, \+200+ in later levels).

  * Villain respawns after delay (2s → shorter at higher levels).

---

### **Lives System**

* **Start:** 3 lives (default).

* **HUD Display:** Spider icons at top left.

* **Lose Life:** On villain collision (not vulnerable).

* **Respawn:** Player respawns at start position, villains reset to pen.

* **Game Over:** Lives \= 0 → Game Over state.

---

### **Scoring System**

* **Dust:** \+10 each.

* **Orb:** \+50 each.

* **Defeating Villain:**

  * \+100 (Level 1).

  * \+200 (Level 2).

* **Bonus Points:** Level clear \= \+500.

* **HUD Display:** Top-center numeric.

---

## **HUD (Heads-Up Display)**

* **Top Left:** Lives (Spider icons).

* **Top Center:** Score.

* **Top Right:** Level indicator (e.g., “Level 2: Times Square”).

* **Optional Bottom Speech Bubble:**

  * For tutorial/help text.

  * e.g., “Grab that orb to web-shoot enemies\!”

---

## **Win / Loss States**

### **Win Condition**

* All dust collected.

* **Visuals:** neon screen flash → comic overlay: “City Cleaned\!” or level-specific message.

* **Spider Quip:** comic speech bubble (randomly pulled from a pool of lines).

* **Transition:** after 2s → next splash or cut scene.

### **Lose Condition**

* Lives \= 0\.

* **Visuals:** Comic “Game Over” panel.

* **Music:** fades out dramatically.

* **Options:** Retry or Exit.

---

## **Visual Style**

* **Overall:** Comic Book aesthetic.

  * Bold outlines.

  * Halftone shading.

  * Primary neon colors (blue, red, yellow, pink).

* **Maze Walls:** Thick black outlines with neon glow per level (blue/purple for East Village, pink/yellow for Times Square).

* **Dust:** Small glowing dots.

* **Orbs:** Larger glowing spheres with magical spark.

* **Enemies:** Distinct neon costumes, comic flair (red, blue, purple, green).

* **Player:** Spider-character sprite (chosen variant).

---

## **Audio / FX**

* **Music:** Looping chiptune \+ comic flair. Faster tempo as levels advance.

* **SFX:**

  * Dust \= “ding.”

  * Orb \= “whoosh/zap.”

  * Enemy hit \= “POW\!” punch.

  * Life lost \= “sting/crash.”

  * Page-flip \= between states.

* **Ambience:** faint NYC city sounds in background (sirens, wind).

---

## **Technical Requirements**

### **Game States**

1. Comic Scene (intro/cut/ending).

2. Level Splash.

3. Gameplay.

4. Win/Lose Transitions.

### **Systems**

* Grid-based movement.

* Collision detection (dust, orbs, enemies).

* Power-up timers and effects.

* Enemy AI (patrol, chase, retreat).

* Scoring.

* Lives system.

* HUD updates.

* Transition manager (comic page-flip FX).

### **Fail Safes**

* Player can’t clip walls.

* Villains only respawn inside pen.

* Dust/orbs reset only on restart.

* Prevent soft-locks: game always ends in Win/Lose.

---

✨ **Final Summary:**  
 This Core Gameplay PRD defines the **engine of Spider-Run**: a grid-based, Pac-Man-inspired loop with dust collection, villains, orbs, scoring, and lives. Everything — visuals, sounds, states, and mechanics — is stylized in comic book fashion. Each level adjusts **parameters** (enemy count, speed, orb strength, visuals), but all run on this same system.