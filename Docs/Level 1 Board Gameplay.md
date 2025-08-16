# **PRD — Level 1 Gameplay (Spider-Run, Finalized with All Details)**

## **Purpose**

Define **all gameplay mechanics, states, rules, visuals, and transitions** for Level 1 (“East Village”) so that Cursor can implement it directly.

---

## **Flow Overview**

1. **Comic Intro Scene**

   * Click-through dialogue between Dr. Strange and Spider-Man (already defined in Comic PRD).

   * Ends on Strange warning: “Be careful, some of your enemies are out tonight.”

   * Transitions automatically into next state.

2. **Level Start Splash Screen**

   * Screen text: **“Level 1: East Village.”**

   * Style: comic cover panel — bold letters, neon blue/purple background with silhouetted East Village buildings.

   * Duration: 2 seconds auto, OR skip on button press (space/enter/controller A).

3. **Gameplay Loop**

   * Player’s chosen Spider-character spawns at start tile (directly below villain pen).

   * Dust, villains, power-ups placed as defined in Board Layout PRD.

   * Game runs until **Win** (dust cleared) or **Lose** (lives \= 0).

4. **End of Level Transition**

   * **Win:** Comic-style splash screen, “City Cleaned\!” with Spider-Man quip. Then load Level 2 splash.

   * **Lose:** “Game Over” comic panel with retry/exit menu.

---

## **Player Controls**

* **Keyboard:** Arrow keys or WASD for movement.

* **Controller:** Joystick/D-pad.

* Movement is **grid-based** (one tile per input step).

* Player can reverse direction instantly, or queue turn at corners (Pac-Man style).

---

## **Core Gameplay Rules**

### **Objectives**

* Collect all **space dust** (white/gray dots).

* Survive enemy encounters.

* Use power-ups to temporarily gain advantage.

### **Dust Collection**

* Each tile with dust disappears when touched by player.

* Score: \+10 points per dust.

### **Power-Ups (Web Shooters / Strange Orbs)**

* 6 per board.

* Appear as glowing orbs with pulsing aura.

* On collect:

  * Enemies turn **vulnerable** (sprite flashes).

  * Player gains:

    * **Speed boost** (20% faster for 5 sec).

    * **Web-shot ability** (press key to stun one enemy in range, 1 use).

* Timer: 6 seconds. Orbs flash in final 2 sec before ending.

### **Villains (Enemies)**

* **Spawn:** inside central villain pen.

* **Count in Level 1:** 3 total active at once.

* **Behavior AI:**

  * Random patrol until they “see” player (short chase radius).

  * Paths reset if stunned.

* **Collision with Player:**

  * If active: Player loses 1 life. Respawns at start.

  * If vulnerable: Villain is stunned, teleports back to pen, \+100 points.

* **Respawn Delay:** 2 seconds after being defeated.

### **Lives**

* Start: **3 lives.**

* Lose all \= Game Over.

* Visual: Spider icons at top left of HUD.

---

## **HUD (Heads-Up Display)**

* **Top Left:** Lives (3 Spider icons).

* **Top Center:** Score (numeric).

* **Top Right:** Level indicator (e.g., “Level 1: East Village”).

* **Bottom:** Comic-style speech bubble overlay for tutorial tips (optional).

---

## **Win/Loss States**

### **Win Condition**

* All dust collected.

* Gameplay stops.

* Screen flashes neon colors.

* Overlay comic panel: **“City Cleaned\! Level Complete\!”**

* Spider quip appears in bubble (e.g., *“Guess sweeping the streets really is my job…”*).

* After 2 sec → auto-transition to Level 2 Splash.

### **Lose Condition**

* Lives \= 0\.

* Music fades out.

* “Game Over” comic panel slides in.

* Options:

  * Retry (restart Level 1).

  * Exit (back to title screen).

---

## **Visual Style**

### **General**

* **Comic Book Style:** Thick black borders, halftone textures, bold colors.

* Background: Black with neon maze walls.

* Dust: Small white/gray dots.

* Orbs: Bright glowing spheres with magical aura (color-shift blue/red).

* Villains: Distinct bold colors (red/blue/purple).

* Player: Uses selected Spider-character sprite (mask on).

### **Splash Screens**

* Big comic lettering (inspired by Pac-Man \+ Marvel covers).

* **Level Splash:** “Level 1: East Village” in bold yellow with shadow outline.

* Background \= simplified East Village skyline with neon glow.

---

## **Audio / FX**

* **Music:** Upbeat chiptune with comic-style flair (looping).

* **SFX:**

  * Dust collect \= *ding*.

  * Power-up \= *whoosh*.

  * Enemy hit \= *thud*.

  * Life lost \= *dramatic sting*.

* **Transitions:** Comic “page-flip” sound when changing states.

---

## **Technical Requirements**

* **Game States Needed:**

  * Comic Intro

  * Level Splash

  * Gameplay

  * Win / Lose transition

* **Systems Needed:**

  * Grid-based movement

  * Collision detection (dust, orbs, villains)

  * Power-up timers

  * Enemy AI (patrol \+ chase)

  * Score & HUD updates

  * Transition handlers (page-flip effect)

* **Fail Safes:**

  * Player can’t clip into walls.

  * Villains respawn inside pen only.

  * Dust and orb respawns reset only on restart.

---

✨ **Final Summary:**  
 Level 1 gameplay starts with a **comic intro**, then shows a **“Level 1: East Village” splash screen**, and drops into a grid-maze dust-collection loop. Player uses Spider-powers, avoids villains, collects all dust to win, and has 3 lives before losing. The entire system is presented in **comic book style**, with splash panels, speech bubbles, and page-flip transitions. All mechanics (collision, scoring, HUD, power-ups, win/lose states) are clearly defined for implementation.