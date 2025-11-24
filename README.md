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
