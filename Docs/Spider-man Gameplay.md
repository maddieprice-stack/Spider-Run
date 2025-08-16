# **PRD — Spider-Man (Playable Character)**

---

## **🎮 Role in Gameplay**

Spider-Man is the **sole player-controlled character.**

* Goal: Collect all **Space Dust Fragments** to clear each level.

* Must avoid **villains** and hazards, using **power-ups** for survival and strategy.

* Designed to feel **agile, responsive, and instantly recognizable** in retro pixel art style.

  ---

  ## **🕷️ Look & Sprite Design**

  ### **Sprite Specs**

* **Base size:** 32×32 px (consistent with villains).

* **Style:** Retro pixel art (to match Pac-Man era).

* **Frames per state:**

  * Idle (breathing): 2 frames.

  * Walk cycle (per direction): 4 frames.

  * Swing (Web Shooter): 3 frames.

  * Taxi teleport: 2 frames (fade out / fade in).

  * Death: 4 frames (spin in web \+ fade).

  ### **Color Palette**

* Red \+ blue body (classic Spider-Man).

* White eye lenses (oversized for clarity).

* Grey/white web strands (animated during swing).

  ### **Visual Effects**

* Invulnerability: Spider-Man sprite flashes white/blue (overlay, 4 frames per second).

* Freeze (Fragment): Villains flash purple, Spider-Man glows faintly purple.

  ---

  ## **🕹️ Core Movement**

* **Input:** Arrow keys (↑ ↓ ← →) or WASD.

* **Movement grid:** 1 tile \= 32px.

* **Speed:** 100% baseline (equal to Goblin/Electro).

* **Allowed directions:** Up, down, left, right.

* **Tile collisions:** Spider-Man cannot pass through walls/buildings.

* **Turns:** Snap-to-grid logic — can only turn at intersections if aligned.

  ---

  ## **🍬 Collectibles**

  ### **1\. Space Dust Fragments**

* **Look:** Small glowing yellow pixel dots (8×8 px).

* **Placement:** Lined along all open street paths.

* **Rule:** All fragments must be collected to clear level.

* **Pickup:** Auto-collect when Spider-Man moves over tile.

  ### **2\. Power-Ups**

**Web Shooter (Main Power-Up)**

* Look: Small glowing white cartridge.

* Effect: Next villain Spider-Man collides with → auto web swing overhead.

* Animation: 3-frame swing (thwip → mid-air flip → land).

* Rules: Single-use. Consumed after swing.

* Invulnerability: Lasts only during swing animation (approx. 1s).

**Taxi Ride (Teleport)**

* Look: Pixel yellow cab, stationary on map.

* Function: Teleports Spider-Man instantly to paired cab.

* Animation: Fade-out (2 frames) → fade-in (2 frames) at new taxi.

* Invulnerability: Entire teleport duration.

* Rule: Taxis are paired; stepping on one always leads to the other.

**Dimensional Fragment (Bonus, Level 2+)**

* Look: Purple-glowing crystal shard.

* Function: \+Score bonus \+ freezes all villains for 3 seconds.

* Animation: Villains flash purple, Spider-Man glows.

* Rule: Only appears in Level 2+.

  ---

  ## **❤️ Lives & Death**

* **Starting lives:** 3\.

* **Death trigger:** Villain collision (unless invulnerable).

* **Death animation:**

  * 4 frames → Spider-Man caught in web, spins, fades out.

* **Respawn:**

  * Reappears at level start position after 2s.

  * Board remains in same state (dust, villains, hazards persist).

  ---

  ## **🪄 Special Gameplay Rules**

* **Collision:**

  * With villain: Lose 1 life.

  * With dust/power-up: Auto-collect.

* **Invulnerability sources:**

  * Web Swing.

  * Taxi teleport.

* **Respawn immunity:**

  * After death, Spider-Man is invulnerable for 1s.

* **Overlap:**

  * Spider-Man cannot share a tile with a villain unless using swing/taxi (otherwise \= death).

  ---

  ## **🔊 Audio Cues**

* Web Shooter: “Thwip\!”

* Taxi: Honk \+ whoosh.

* Fragment: Magical shimmer.

* Collect dust: Soft “ding.”

* Death: Web snap \+ flat sting.

  ---

  ## **🌆 Strategic Role**

Spider-Man is **fast but fragile.**

* Must use **maze awareness \+ power-ups** to survive.

* Vulnerability makes villain mechanics more dangerous (alley blocks, bombs, gusts, blackouts).

* Invulnerability windows are **short**, so timing is critical.