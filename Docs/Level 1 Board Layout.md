# **Level 1 PRD — East Village**

## **Theme & Goal**

* **Theme:** Cozy NYC neighborhood streets, retro 16-bit pixel art, based on the classic blue Pac-Man maze.

* **Goal:** Collect all **space dust** while avoiding villains and hazards.

* **Hazard Style:** Flickering/unlit streetlights that create temporary darkness zones for extra challenge.

---

## **Map Layout**

**Grid size:** 27×29 tiles (0-indexed coordinates; top-left \= (0,0))  
 **Tile legend:**  
 `#` \= wall/building • `.` \= space dust • \= empty space (inside villain pen) • `-` \= pen door  
 `W` \= Web Shooter • `T` \= Taxi stop • `S` \= Player spawn • `V` \= Villain spawn (inside pen)

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

## **Key Positions**

* **Player spawn:** (13, 12\)

* **Villain spawns:** (12,5), (14,5), (11,6), (15,6), (12,7), (14,7) (inside central pen)

* **Web Shooters:** (1,1), (23,1), (12,16), (14,16), (6,24), (20,24)

* **Taxi stops:** (1,3), (25,3), (1,9), (25,9), (7,21), (19,21), (1,26), (25,26)

---

## **Villains Present**

* **Doc Ock:** Blocks alleys with arms for 3 seconds.

* **Green Goblin:** Drops pumpkin bomb debris to block paths for 4 seconds.

* **Vulture:** Creates wind gust zones that slow Spidey for 3 seconds.

---

## **Hazards**

* **Darkness zones:**

  * Zone 1: top-left quadrant (cols 0–12, rows 0–10)

  * Zone 2: lower-right quadrant (cols 14–26, rows 18–28)

  * Cycle: 3 seconds on, 6–8 seconds off.

---

## **Power-Up Rules**

* **Web Shooter:** 6s swing duration, automatically stuns villains passed over; stunned villains respawn after 3s.

* **Taxi Ride:** When Spidey steps onto a taxi stop (`T`), jumps onto the roof, travels in a straight line at 2× speed, collecting all dust along that path until reaching the next junction or wall.

---

## **Level Complete Condition**

* All space dust collected.

* “LEVEL COMPLETE” banner shows, then cutscene with Dr. Strange introducing Times Square.

---

## **Ability Timers**

* **Web Shooter:** 6s duration; stunned villains respawn after 3s.

* **Doc Ock arms:** 3s block; cooldown \~12s.

* **Goblin debris:** 4s block; cooldown \~12s.

* **Vulture wind:** 3s slow; cooldown \~12s.