### **Implement Movement & Wrapping for This ASCII Board**

Use the ASCII map below as the **authoritative layout** for the level. Treat characters as follows:

**Legend**

* `#` \= wall/blocker (solid; never enterable)

* `.` \= pellet (walkable; collect on enter)

* `W` \= power pellet (walkable; collect on enter; triggers power mode)

* `-` \= ghost-house door (passable by villains only; **not** passable by the player)

* `' '` (space) \= empty walkable tile (a corridor tile without a pellet—e.g., in front of the ghost house)

**Board**

`###############################`  
`#W............##............W#`  
`#.####.#####.##.#####.####.#.#`  
`#.#  #.#   #.##.#   #.#  #.#.#`  
`#.#  #.#   #.##.#   #.#  #.#.#`  
`#.####.#####.##.#####.####.#.#`  
`#............................#`  
`#.####.##.########.##.####.#.#`  
`#.####.##.########.##.####.#.#`  
`#......##....##....##......#.#`  
`######.##### ## #####.######.#`  
     `#.##### ## #####.#`         
     `#.##          ##.#`         
     `#.## ###--### ##.#`         
`######.## #      # ##.######.#`  
      `.   #      #   .`         
`######.## #      # ##.######.#`  
     `#.## ######## ##.#`         
     `#.##          ##.#`         
     `#.## ######## ##.#`         
`######.## ######## ##.######.#`  
`#............##............#.#`  
`#.####.#####.##.#####.####.#.#`  
`#.#  #.#   #.##.#   #.#  #.#.#`  
`#.#  #.#   #.##.#   #.#  #.#.#`  
`#.####.#####.##.#####.####.#.#`  
`#W..........................W#`  
`###############################`

#### **Movement Rules**

1. **Walkable tiles:** `.` `W` and space `' '` are walkable for the player. `#` is not.

2. **Ghost house:** The central house is enclosed by `#`; the **door** is the `--` segment.

   * **Player cannot cross `--`.**

   * **Villains can** cross `--` (both directions).

3. **Grid movement:** 4 directions only (up/down/left/right). Snap to tile centers; turns are allowed only when the next tile in that direction is walkable.

4. **Wrap-around tunnels:** If a move would take the player **off the left or right edge**, wrap to the **same row on the opposite edge** *if* that destination tile is walkable.

   * Implementation: when `x < 0`, set `x = width - 1` **if** `grid[y][width-1]` is walkable; when `x >= width`, set `x = 0` **if** `grid[y][0]` is walkable.

   * Do **not** wrap vertically (top/bottom).

5. **Pellets:** entering a `.` removes it and adds pellet score.

6. **Power pellets:** entering a `W` removes it and triggers power mode (timer), per existing PRD.

7. **Collisions:** walls `#` always block; ghost door `--` blocks the player only.

#### **Rendering & Integrity**

* Keep **row width constant**; do not trim leading spaces—those spaces are intentional walkable tiles.

* Walls are **solid** (no hollow interiors); draw them as continuous filled blocks per `#`.

* Power pellets appear **only** where `W` is placed (four corners).

With this, implement the tile map loader, movement/turning, pellet collection, power-pellet logic, and the horizontal wrap mechanic tied directly to this ASCII.

