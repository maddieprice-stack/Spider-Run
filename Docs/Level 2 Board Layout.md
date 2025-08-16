# **PRD — Level 2 Board Layout (Times Square)**

---

## **Overview**

Level 2 takes place in **Times Square**. Compared to Level 1 (East Village), it is **larger, denser, and more chaotic**, reflecting Times Square’s crowded energy. The board includes **tighter corridors, more dead ends, and hazard-prone intersections**.

Key changes from Level 1:

* **Dimensional Fragments (`T`)** are now introduced, appearing in key intersections.

* **Electro** is added to the villain roster, bringing blackout mechanics.

* **Pellet density** is slightly increased for higher collection pressure.

* **Maze symmetry** is preserved left/right, but the central lanes are tighter.

---

## **Legend for Map Symbols**

* `#` \= Wall (buildings, impassable)

* `.` \= Space dust pellet (collectible)

* `W` \= Web Shooter (power pellet, gives stun ability)

* `T` \= Dimensional Fragment (bonus item, only spawns in Level 2+)

* `-` \= Pen gate (villains exit here)

* `V` \= Villain pen (Doc Ock, Goblin, Vulture, Electro)

* `S` \= Player spawn point (Spider-Man starts here)

* (space) \= Open street/lane

---

## **ASCII Layout — Times Square**

`###########################`  
`#W........###...........W#`  
`#.####.#.###.###.#.####.#`   
`#T#  #.#..... .....#. #T#`   
`#.#  #.#####-#####.#  #.#`   
`#.#  #.#   V V   #.#  #.#`   
`#.#  #.#  V   V  #.#  #.#`   
`#.#  #.#   V V   #.#  #.#`   
`#.#  #.#####-#####.#  #.#`   
`#T#  #.#..... .....#. #T#`   
`#.####.#.###.###.#.####.#`   
`#W........###...........#`   
`#########  S  ###########`   
`#...............T........#`  
`#.####.#####.#####.####.#`   
`#.#  #.#   #.#   #.#  #.#`   
`#.#  #.# W #.# W #.#  #.#`   
`#.#  #.#####.#####.#  #.#`   
`#.#  #.............#  #.#`   
`#.####.###.#.#.###.####.#`   
`#.....T...#.#.#...T.....#`   
`###.#####.#.#.#.#####.###`   
`#...#   #.......#   #...#`   
`#.#.# W ####### W #.#.#.#`   
`#.#.#   #.....#   #.#.#.#`   
`#.#.#####.#.#.#####.#.#.#`   
`#T.......T.#.#.T.......T#`   
`###########################`

---

## **Row-by-Row Breakdown**

### **Top Section (Rows 1–4)**

* **Row 1:** Solid wall border.

* **Row 2:** Web Shooters (`W`) in both corners, long horizontal pellet line leading toward the center.

* **Row 3:** Heavier wall section with three central lanes. This creates **outer loops** for villains to patrol.

* **Row 4:** First Dimensional Fragments (`T`) appear near the edges, placed just beyond short corridors. This tempts the player into risky routes.

### **Central Pen Area (Rows 5–9)**

* **Rows 5–9:** Villain pen.

  * `V` \= villain pen cells.

  * `-` \= pen gates.

  * This is where all villains (Doc Ock, Green Goblin, Vulture, Electro) spawn at the start of the level.

* Narrow lanes around the pen make it harder to kite villains compared to Level 1\.

### **Middle Rows (10–15)**

* **Row 10:** More Dimensional Fragments (`T`) placed symmetrically near side alleys.

* **Row 12:** Another set of Web Shooters (`W`) near the left/middle/right, forcing player to dive deeper to collect.

* **Row 13:** Player spawn (`S`) directly below villain pen, meaning **high initial danger**.

* **Row 14:** Central alley holds another Fragment (`T`), requiring risky mid-board navigation.

### **Lower Maze (Rows 16–26)**

* **Row 17:** Symmetrical chamber with **Web Shooters inside walls** — forces careful entry.

* **Rows 18–22:** Long corridors and pellet-heavy stretches; more dead ends to trap the player.

* **Row 20:** Side Fragments (`T`) placed inside narrow intersections. Villains can easily ambush here.

* **Row 24:** Web Shooters (`W`) placed inside enclosed wall clusters, forcing bold routes to collect.

* **Row 26:** Final set of Fragments (`T`) near the bottom corners.

### **Row 27 (Bottom Border)**

* Fully walled-in with no exits.

---

## **Gameplay Flow**

1. **Start:** Spider-Man spawns under villain pen (Row 13). Villains exit pen one-by-one after a short delay.

2. **Player Goal:** Collect all pellets (`.`) and fragments (`T`) while avoiding villains.

3. **Web Shooters (`W`):** Used to stun villains temporarily, crucial when trapped in dead ends.

4. **Dimensional Fragments (`T`):** Only introduced in Level 2\. Adds high-risk, high-reward strategy since they are placed in **dangerous intersections**.

5. **Villain Behavior:**

   * Doc Ock may block central alleys.

   * Goblin’s bombs can cut off outer loops.

   * Vulture swoops through vertical stretches.

   * Electro darkens one quadrant, forcing blind navigation.

---

## **Design Philosophy**

* **Chaos Factor:** Level 2 is deliberately more claustrophobic, with intersections that villains can trap players in.

* **Fragment Placement:** Fragments (`T`) are placed in intersections that mimic Times Square’s crowded, crisscrossing streets.

* **Higher Difficulty:** Player is forced to navigate closer to the pen more often, creating higher sustained pressure.

* **Balance:** Symmetry ensures fairness while maintaining tension.

---

## **Developer Notes for Cursor**

* Map is **28 rows tall, 27 columns wide** (matches Pac-Man dimensions).

* Symmetry means left half can be mirrored for collision/pathfinding checks.

* Ensure pellet placement (`.`) fills all lanes except walls, pen, spawn, and power-ups.

* Fragments (`T`) should only appear **after Level 2 starts**.

* Villain pen must allow **sequential release** (not all villains at once).

* Paths should remain fully navigable (no single-tile dead ends that strand the player permanently).

