# Graph Algorithm Visualizer (Python + Tkinter)

Interactive tool for visualizing classic graph algorithms using a clean Tkinter-based GUI.  
Supports node creation, weighted edges, dynamic editing, and step-by-step animation for each algorithm.

---

## 🚀 Features

### 🧩 Graph Editing
- Click to **create nodes** (A, B, C, …)
- Click node → click another → **add edge** (with weight dialog)
- **Move nodes** freely (drag & drop)
- **Delete node** or **delete edge**
- Reset all edge colors
- Fully **real-time redraw** on each update

---

## 🔍 Supported Algorithms (with animation)
All algorithms follow standard, correct logic from graph theory:

| Algorithm | Description |
|----------|-------------|
| **DFS** | Depth-First Search spanning tree |
| **BFS** | Breadth-First Search spanning tree |
| **Dijkstra** | Shortest path between two nodes |
| **Prim's MST** | Minimum Spanning Tree starting from a selected node |
| **Kruskal's MST** | Global MST using Union-Find |

---

## 🎨 GUI Highlights
- Dark mode UI
- Smooth animations for each step
- Edge highlighting during algorithm execution
- Color-coded nodes:
  - 🟩 **Source**
  - 🟧 **Target**
  - 🟡 **Visited / Path**

---

## 🖼️ Example Screenshot
*(Add screenshot later)*  
You can upload a screenshot to the repo and link it here.

---

## 🛠️ Installation

### 1. Clone the repository
```bash

git clone https://github.com/your-username/graph-algorithm-visualizer.git
cd graph-algorithm-visualizer

```

2. Install dependencies

This project uses only Python standard libraries — no external libraries required.

Python 3.8+ recommended.
```bash
▶️ Run the Program
python graph_gui.py
```

📌 How to Use
➤ Create Nodes

Click empty space → a new node is created (A, B, C, …)

➤ Create Edges

Click node u

Click node v

Enter weight in popup dialog

➤ Move Nodes

Press Move nodes → drag a node to reposition

➤ Delete

Delete node → click node

Delete edge → click line or weight text

➤ Run Algorithms

Click any of the following:

DFS

BFS

Dijkstra

Prim MST

Kruskal MST

Then select nodes if required (e.g., start or destination).

📂 Project Structure
```bash
graph-algorithm-visualizer/
│
├── graph_gui.py          # main GUI program
├── README.md             # project documentation
└── (your future screenshots, assets, etc.)
```

📘 Technical Notes

Nodes stored in self.node_positions

Graph stored using adjacency list (Graph.adj)

All algorithms use original textbook logic

GUI state machine handles:

build mode

move mode

dfs/bfs/prim selection

dijkstra source/target selection

deletion modes

Animation is performed using:

self.root.after(self.anim_delay, ...)

🧑‍💻 Author

Created by Taiga0727
For learning, visualization, and graph algorithm experimentation.

⭐ Future Improvements

Save/load graphs as JSON

Export image of graph

Add directed/undirected toggle

Add Floyd–Warshall, Bellman-Ford

Add animation speed slider

📜 License

This project uses the MIT License 
