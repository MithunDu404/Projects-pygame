# Pathfinding Algorithm Visualizer

An interactive visualization tool that demonstrates how various pathfinding algorithms work, allowing users to see the search process in real-time and compare algorithm efficiency.

## 📌 Features

- **Multiple Pathfinding Algorithms**: Visualize A*, Dijkstra's, BFS, and DFS algorithms.
- **Interactive Grid**: Create custom obstacles, set start/end points, and watch algorithms work in real-time.
- **Performance Analysis**: Compare efficiency with metrics for nodes visited, path length, and execution time.
- **Maze Generation**: Automatically generate navigable mazes with adjustable density.
- **Diagonal Movement**: Toggle between 4-directional and 8-directional movement.
- **User-Friendly Interface**: Intuitive controls and clear visual feedback.

## 🛠️ Technologies Used

- **Python 3.x**
- **Pygame**: For graphics and user interface
- **Standard Library**: Queue, PriorityQueue, and other data structures

## 🚀 Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pathfinding-visualizer.git
   cd pathfinding-visualizer
   ```
4. Run the application:
   ```bash
   python pathfinding_visualizer.py
   ```

## 🎮 Usage Instructions

### 📌 Setup the Grid
- **Left-click**: Place the start point (first click), end point (second click), and barriers (subsequent clicks).
- **Right-click**: Remove any placed element.

### 📌 Choose an Algorithm
- Click on the desired algorithm button in the control panel.
- Options include **A***, **Dijkstra's**, **BFS**, and **DFS**.

### 📌 Run the Visualization
- Click the "Start Algorithm" button or press `Space` to begin the visualization.
- Watch as the algorithm explores the grid and finds the shortest path.

### 📌 Create Mazes
- Click "Generate Maze" to automatically create a random maze.
- Adjust maze density using the `+` and `-` keys.
- Clear the grid using the "Clear Grid" button or by pressing `C`.

### 📌 Toggle Settings
- Enable/disable **diagonal movement** for different search patterns.
- Observe how algorithms perform under different conditions.

## 🔍 Algorithms Implemented

### 🔹 A* Algorithm
A best-first search algorithm that uses a heuristic to estimate the distance to the goal. It combines Dijkstra’s algorithm (favoring nodes close to the start) and greedy best-first search (favoring nodes close to the goal).

### 🔹 Dijkstra’s Algorithm
A special case of A* where the heuristic is zero. It guarantees the shortest path by exploring nodes in order of their distance from the start.

### 🔹 Breadth-First Search (BFS)
Explores all nodes at the present depth before moving to nodes at the next depth level. It guarantees the shortest path in unweighted graphs.

### 🔹 Depth-First Search (DFS)
Explores as far as possible along each branch before backtracking. It doesn’t guarantee the shortest path but can be useful for maze generation and solving.

## ⌨️ Controls

### 🖱️ Mouse Controls
- **Left Click**: Place start/end points and barriers.
- **Right Click**: Remove elements from the grid.

### 🎹 Keyboard Shortcuts
- `Space`: Start the selected algorithm.
- `C`: Clear the grid.
- `M`: Generate a random maze.
- `D`: Toggle diagonal movement.
- `+ / -`: Adjust maze density.

## 📊 Performance Analysis
The visualizer provides real-time performance metrics:
- **Nodes Visited**: Number of grid cells the algorithm explored.
- **Path Length**: Length of the final path found.
- **Execution Time**: Time taken to find the path.

These metrics help understand the efficiency and characteristics of different algorithms.

## 💡 Example Use Cases
- **Educational Tool**: Learn how different pathfinding algorithms work.
- **Algorithm Comparison**: Visualize the differences between greedy algorithms like A* and exhaustive algorithms like BFS.
- **Maze Solving**: Test algorithms against different maze configurations and obstacles.

## 🔮 Future Improvements
- Add more algorithms (Greedy Best-First Search, Bidirectional Search).
- Implement weighted grids to simulate terrain costs.
- Add the ability to save and load grid configurations.
- Include a step-by-step execution mode for detailed analysis.
- Implement algorithm animation speed controls.

## 🙌 Acknowledgements
- Special thanks to the **Pygame community** for their documentation and resources.
- Inspired by various online pathfinding visualizers and educational resources on graph algorithms.

## 🤝 Contributors
If you'd like to contribute to this project:
- Fork the repository.
- Submit a pull request with your changes.
- Bug reports, suggestions, and feature requests are welcome through the **GitHub issue tracker**.

---

**Pathfinding Visualizer Demo**  
🚀 *![Screenshot 2025-03-09 013235](https://github.com/user-attachments/assets/dea2101a-a584-45ac-94fa-09e6a4589c5f)*
🚀 *![image](https://github.com/user-attachments/assets/7ffaa3d9-c77f-46ef-97de-39e67c6b1bbe)*

