# **PRD – Level 3 (Blitz Mode)**

## **Overview**

Level 3 is a **blitz-style chase** level. Spider-Man must navigate a **vertical maze** representing the **Empire State Building**, while **Lizard** relentlessly pursues him. The objective is to reach the **goal (G)** before Lizard catches Spider-Man.

---

## **Gameplay Flow**

1. **Start Point (S):** Spider-Man spawns at the bottom left of the maze.

2. **Lizard Chase:** Lizard enters shortly after Spider-Man and moves **directly toward him**, tracking his path through the maze.

3. **Maze Navigation:** The maze is tighter and more linear than previous levels, encouraging **constant motion**.

4. **Victory Condition:** Spider-Man reaches **G** at the top right.

5. **Failure Condition:** Lizard collides with Spider-Man.

---

## **ASCII Map Layout**

`##############################`  
`#.......###.......#.....#...G#`  
`#.#####.###.#####.#.###.###.##`  
`#.#...#.###.....#...#.....#.##`  
`#.#.#.#.#######.#####.#####.##`  
`#...#.#.........#...#.....#..#`  
`#####.###########.#.#####.#.##`  
`#.....#.........#.#.#...#.#..#`  
`#.#####.#######.#.#.#.#.#.#.##`  
`#.#.....###.....#.#.#.#...#..#`  
`#.###.#####.#####.#.#.#####.##`  
`#.....#...#.....#.#.......#..#`  
`#######.#.#####.#.#########.##`  
`#.......#.......#............#`  
`S#############################`

* **S \= Spider-Man starting position (bottom left).**

* **G \= Goal (top right).**

* **Path \= single main route** with tight corridors and choke points.

* **Enemy (Lizard) \= chases Spider-Man upward through the maze.**

---

## **Core Features**

* **Chase Mechanic:** Lizard always advances toward Spider-Man; if the player hesitates, Lizard closes in.

* **Vertical Urgency:** Maze forces upward/rightward progression to simulate climbing the Empire State Building.

* **Blitz Pressure:** No safe resting zones — Spider-Man must keep moving.

* **Victory Animation:** Upon reaching G, Spider-Man swings upward and escapes.

* **Defeat Animation:** If caught, Lizard slams Spider-Man down (quick animation).

---

## **Technical Notes**

* **Lizard AI:** Simple pursuit algorithm (follows Spider-Man’s current path with slight delay).

* **Speed Tuning:** Spider-Man moves faster but must navigate; Lizard is slower but smooth in movement.

* **Collision States:** Contact \= instant failure.

* **Art Assets:** Empire State Building theme, Lizard climbing/crawling sprite, chase tension effects (screen shake, red flashes).

