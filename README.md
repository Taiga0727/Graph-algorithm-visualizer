# Graph Algorithm Visualizer (Python + Tkinter)

An interactive tool for visualizing classic graph algorithms through an intuitive Tkinter-based GUI.  
Supports node creation, weighted edges, dynamic editing, and step-by-step animations for every algorithm.

---

## 🖼️ Overview

*(Preview Screenshot — replace with your own later)*  
https://your-image-link-here.com/screenshot.png

This tool lets you build graphs visually and run algorithms like DFS, BFS, Dijkstra, Prim, and Kruskal with live animations.

---

## 🚀 Features

### 🧩 Graph Editing
- Click to **create nodes** (A, B, C, …)
- Click node → click another → **add weighted edge**
- **Move nodes** (drag & drop)
- **Delete node** or **delete edge**
- Reset colors / Clear graph
- Smooth redrawing for all updates

---

## 🔍 Supported Algorithms (with animation)

| Algorithm      | Description |
|----------------|-------------|
| **DFS**        | Depth-First Search spanning tree |
| **BFS**        | Breadth-First Search spanning tree |
| **Dijkstra**   | Shortest path from source to target |
| **Prim MST**   | Minimum Spanning Tree |
| **Kruskal MST**| Global MST using Union-Find |

All algorithms preserve their **original textbook logic** from your original non-GUI code.

---

## 🎨 GUI Highlights
- ✔ Dark mode UI  
- ✔ Smooth animations  
- ✔ Edge highlighting on algorithm steps  
- ✔ Color-coded nodes  
  - 🟩 Source  
  - 🟧 Target  
  - 🟡 Visited / Path  

## 🛠️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/graph-algorithm-visualizer.git
cd graph-algorithm-visualizer
```
2️⃣ Install dependencies

No external libraries required (only Python standard library).

Python 3.8+ recommended.

3️⃣ Run the program
```bash
python graph_gui.py
```
📌 How to Use

➤ Create Nodes

  Click anywhere on the canvas to create a node (A, B, C…).

➤ Create Edges

  Click node u
  Click node v
  Enter weight in popup dialog

➤ Move Nodes

  Click Move nodes
  Drag node to reposition

➤ Delete

  Delete node → click node
  Delete edge → click edge line or weight text

➤ Run Algorithms

  Choose:
    DFS
    BFS
    Dijkstra
    Prim MST
    Kruskal MST
    Then select the required start/target node(s).

📂 Project Structure
```bash
graph-algorithm-visualizer/
│
├── graph_gui.py          # Main Tkinter program
├── README.md             # Project documentation
└── (optional links or assets if added later)
```
📘 Technical Notes

Node list stored in:
```bash
self.node_positions
```
Graph stored using adjacency list (unchanged from original logic)

Uses root.after() for animation timing

Clean state-machine handling:
  build
  move
  dfs/bfs/prim
  dijkstra source/target
  delete node / delete edge

👨‍💻 Author

  Created by Taiga0727 , Ter , Wu
  A tool for learning, visualizing, and experimenting with graph algorithms.

⭐ Future Improvements

  Save/load graph as JSON
  Export canvas as PNG
  Support directed edges
  Add Bellman–Ford & Floyd–Warshall
  Speed control for animations

📜 License
  This project uses the MIT License.
git clone https://github.com/your-username/graph-algorithm-visualizer.git
cd graph-algorithm-visualizer
