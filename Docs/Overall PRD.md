# **PRD — Spider-Run (Master Document)**

## **Purpose**

Define the **complete game experience** for Spider-Run, including narrative flow, state transitions, gameplay mechanics, visual/audio style, and technical requirements. This PRD consolidates all other PRDs (comic scenes, level PRDs, core gameplay) into one **grand outline** so Cursor understands the game’s overall design.

---

## **High-Level Concept**

Spider-Run is a **Pac-Man-inspired, comic book-styled maze game** starring Spider-variants (Spider-Man, Spider-Gwen, Miles Morales).

* Player goal: clean up **Dr. Strange’s spilled space dust** across NYC while avoiding enemies.

* Gameplay: collect dust, use orbs/power-ups, avoid or defeat villains.

* Style: **Comic book brought to life** — halftone textures, thick outlines, splash panels, and page-flip transitions.

* Progression: Told through **comic cut scenes** and **2 playable levels** (expandable).

---

## **Flow Overview (Game Order)**

1. **Title Screen**

   * Comic cover style.

   * Options: Start Game, Instructions, Exit.

2. **Comic Intro Scene** (PRD: Intro Comic)

   * Dr. Strange introduces story: spilled space dust, needs Spider-Man’s help.

   * Player clicks through dialogue squares.

   * Ends with Strange warning: “Be careful, some of your enemies are out tonight.”

3. **Level 1 Splash Screen**

   * Text: “Level 1: East Village.”

   * Neon skyline background.

   * Auto 2s or skip.

4. **Level 1 Gameplay** (PRD: Level 1 Gameplay)

   * Grid maze in East Village style.

   * Player collects dust, avoids villains, uses orbs.

   * Ends with Win → Level Complete comic panel OR Lose → Game Over comic panel.

5. **Cut Scene Between Levels** (PRD: Mid-Cut Comic)

   * Dr. Strange congratulates player.

   * Spider-Man makes sarcastic quip.

   * Strange reveals next mission: Times Square is also covered.

6. **Level 2 Splash Screen**

   * Text: “Level 2: Times Square.”

   * Neon billboards skyline background.

   * Auto 2s or skip.

7. **Level 2 Gameplay** (PRD: Level 2 Gameplay)

   * More difficult maze with Times Square theme.

   * Extra villains, faster AI, more orb power.

   * Ends with Win → City Saved comic finale OR Lose → Game Over.

8. **Ending (if Win)**

   * Comic splash finale: “NYC Saved\!”

   * Spider quip \+ closing Dr. Strange line.

9. **Game Over (if Lose at any level)**

   * Comic “Game Over” panel.

   * Options: Retry (restart at Level 1\) or Exit.

---

## **Core Gameplay Systems (PRD: Core Gameplay)**

* **Movement:** grid-based, 4 directions, queue turns, instant reversal.

* **Objectives:** collect all dust, survive enemies, use power-ups.

* **Dust:** \+10 points each, total collection \= win condition.

* **Power-Ups (Strange Orbs):** vulnerability mode, speed boost, 1–2 web-shots.

* **Villains:** patrol \+ chase AI, collision rules (lose life or defeat).

* **Lives:** 3 lives per run, HUD displayed, reset on death, Game Over if 0\.

* **Scoring:** dust, orb, villain defeats, bonus for level clear.

* **HUD:** Lives (top-left), Score (center), Level ID (top-right), optional comic bubble tutorials (bottom).

* **Win State:** Level cleared → neon flash \+ splash → next state.

* **Lose State:** Lives \= 0 → Game Over splash → Retry/Exit.

---

## **Visual & Audio Style**

* **Overall:** Comic Book brought to life.

  * Thick black outlines, halftones, neon colors.

  * Splash panels for transitions.

  * Page-flip FX between scenes.

* **Levels:**

  * East Village: blue/purple neon skyline, simple buildings.

  * Times Square: pink/yellow neon billboards, busier/flashier.

* **Characters:**

  * Player: selectable Spider-variant sprite (Spider-Man, Gwen, Miles).

  * Villains: bold neon enemies with distinct colors.

* **HUD:** comic-style speech bubbles & iconography.

* **Audio:**

  * Music: upbeat comic chiptune.

  * SFX: ding (dust), zap (orb), POW\! (villain defeat), sting (life lost), page-flip (transition).

  * Optional ambience: faint NYC sounds.

---

## **Technical Requirements**

**Game States Needed:**

* Title Screen

* Comic Scene

* Level Splash

* Gameplay (Level 1, Level 2\)

* Win Transition

* Lose Transition

* Ending

**Systems Required:**

* Grid-based movement engine.

* Collision detection (dust/orb/enemy).

* Power-up manager (timers \+ effects).

* Enemy AI (patrol \+ chase \+ reset).

* Score & lives tracking.

* HUD updates.

* Transition manager (page-flip effect).

**Fail Safes:**

* Player cannot clip through walls.

* Villains respawn only in pen.

* No soft locks (always Win or Lose).

* Reset dust/orb only on restart.

---

## **Difficulty & Scaling**

* **Level 1 (East Village):** 3 villains, slower speed, 1 web-shot per orb.

* **Level 2 (Times Square):** 4 villains, faster chase, 2 web-shots per orb.

* **Future Scaling:** add more villains, tighter mazes, shorter orb timers.

---

## **Final Summary**

Spider-Run is a **comic book arcade game** where players pick a Spider-variant and help Dr. Strange clean NYC of spilled space dust. The game alternates between **comic cut scenes** and **maze gameplay**. Players collect dust, use Strange Orbs for powers, and survive villains. The style is bold, comic-inspired, with splash panels, quips, and page-flip transitions.

* **Intro Comic → Level 1 → Cut Scene → Level 2 → Finale.**

* Win \= City Saved splash, Lose \= Game Over splash.

* All mechanics (movement, collision, HUD, AI, scoring, lives, power-ups) are defined.

* All visuals/audio are unified under a comic-book aesthetic.

This document serves as the **master guide** for implementation. Sub-PRDs (Comic Scenes, Level 1, Level 2, Core Gameplay) contain detailed specifications that plug into this flow.

