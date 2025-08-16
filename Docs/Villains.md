# **PRD — Villains Gameplay**

### **Doctor Octopus (Doc Ock)**

**Look:**  
 Pixel art sprite with large, flailing metallic arms.

**Movement Pattern:**

* Prefers **short horizontal patrols** near the center.

* At intersections: chooses central lanes rather than corners.

* Speed \= **90%** of base villain speed.

**Special Ability — “Alley Block”**

* Every \~12s, extends arms across the nearest narrow alley.

* **Effect:** Alley blocked for 3s (player cannot pass).

* **Feedback:** Arms stretch out with metallic “CLANG” sound.

* **Impact:** Forces reroutes, raising trap risk with other villains.

  ---

  ### **Green Goblin**

**Look:**  
 Pixel sprite riding a glider, animated tossing pumpkin bombs.

**Movement Pattern:**

* Prefers **outer loops** of the map.

* At intersections: tends to choose routes furthest from player unless chasing.

* Speed \= **100%** (baseline).

**Special Ability — “Pumpkin Bomb Debris”**

* Every \~12s, drops a bomb at a random intersection.

* **Effect:** Rubble blocks that tile for 4s.

* **Feedback:** Goblin laugh SFX, bomb drop animation, rubble with pixel flames.

* **Impact:** Cuts off escape routes unpredictably.

  ---

  ### **Vulture**

**Look:**  
 Pixel sprite with extended wings, swooping motion.

**Movement Pattern:**

* Prefers **vertical movement** (up/down sweeps).

* Occasionally cuts diagonally when map allows.

* Speed \= **110%** (fastest villain).

**Special Ability — “Wind Gust”**

* Every \~12s, creates a gust in the direction he’s flying.

* **Effect:** Player caught is slowed to 50% speed for 3s.

* **Feedback:** Swoosh SFX \+ blue-green wind effect down lane.

* **Impact:** Slowing increases likelihood of being cornered by others.

  ---

  ### **Electro *(Introduced Level 2\)***

**Look:**  
 Bright yellow-green sprite, crackling electricity around him.

**Movement Pattern:**

* Erratic zig-zagging.

* At intersections: **20% chance to choose a random turn** instead of normal chase.

* Speed \= **100%** (baseline).

**Special Ability — “Blackout”**

* Every 10–15s, overloads circuits.

* **Effect:** One quadrant of map darkens for 4s (dust, power-ups, and villains hidden).

* **Feedback:** Screen flicker, electric buzzing crackle.

* **Impact:** Player risks running blind into enemies.

  ---

  ## **Villain Balance**

* **Doc Ock \= Control** (blocks routes).

* **Green Goblin \= Trap-maker** (bombs/rubble).

* **Vulture \= Debuff** (slows player).

* **Electro \= Chaos** (reduces visibility).

Together they form layered pressure:

* Ock reroutes → Goblin cuts exits → Vulture slows → Electro blinds.

  ---

  ## **Difficulty Scaling**

* **Level 1 (East Village):** Only Doc Ock, Green Goblin, and Vulture appear.

  * Longer cooldowns (\~12s).

  * Darkness hazards from flickering streetlights add tension.

* **Level 2 (Times Square):** Electro joins.

  * Shorter cooldowns (\~10s).

  * Hazards more frequent (billboard glare, villain overlap).

  ---

  ## **Timers & Cooldowns Summary**

* Doc Ock (Arms): 3s block / \~12s cooldown.

* Green Goblin (Bomb): 4s rubble / \~12s cooldown.

* Vulture (Wind Gust): 3s slow / \~12s cooldown.

* Electro (Blackout): 4s blackout / \~10–15s cooldown.  
