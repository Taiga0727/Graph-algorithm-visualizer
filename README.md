# Graph Algorithms Visualizer

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%2020OS%20%7C%20-lightgrey))
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

An interactive **desktop GUI application** for creating graphs and visualizing classical graph algorithms  
with smooth animations, a modern dark UI, and intuitive editing tools.  
Built using **Python + Tkinter**, with clean algorithm logic preserved exactly as in theory.

---

## 🚀 Download Executable (.exe)

You can download the latest pre-built executable here:

👉 **GitHub Releases:**  
https://github.com/Taiga0727/Graph-algorithm-visualizer/blob/main/graph_gui.exe

---

## ✨ Supported Algorithms

All algorithms use **textbook-accurate, untouched original logic**:

- **DFS – Depth-First Search Spanning Tree**
- **BFS – Breadth-First Search Spanning Tree**
- **Dijkstra – Shortest Path**
- **Prim – Minimum Spanning Tree (starting from a root)**
- **Kruskal – Minimum Spanning Tree (Union-Find)**

Each algorithm displays:

- Step-by-step expansion  
- Highlighted edges and nodes  
- Execution order  
- Live animation on the graph  
- Result summary panel  

---

## 🧩 Graph Editor Features

- Click to **create nodes** (A, B, C, …)
- Click node → node to **create weighted edges**
- **Drag nodes** to move their positions
- **Select multiple nodes** with a box selection tool
- Delete node / delete edge / delete selected
- **Run algorithms with animations**
- Save graph to `.json`
- Load graph back anytime

---

## 🖱️ Tools Overview

### **Draw / Add**
- Click empty canvas → create node  
- Click node → other node → create edge (weight dialog pops up)

### **Mouse / Pan Mode**
- Click node → select  
- Drag empty space → pan canvas  
- Scroll → zoom  
- Ctrl + Scroll → fast zoom  

### **Select Nodes**
- Drag a rectangle → select multiple nodes

### **Move Nodes**
- Drag selected nodes → move as a group

### **Delete Node / Delete Edge**
- Click to remove individual nodes or edges

### **Delete Selected**
- Remove all highlighted nodes in one action

---

## 🔍 Zoom & View Controls

- **Mouse Wheel** → zoom in/out  
- **Ctrl + Wheel** → faster zoom  
- View menu provides + / − zoom buttons as well  

---

## ⌨️ Keyboard Shortcuts

- **Delete / Backspace**
  - If nodes are selected → delete nodes  
  - If nothing selected → delete nearest edge  

---

## 📊 Result Panel (Bottom-Right)

Includes:

- Full step list of algorithm execution  
- Live-updating logs  
- Card-style hover animation  
- Node coloring:
  - 🟩 Source  
  - 🟧 Target  
  - 🟡 Visited / Path  

---

## 💾 Saving & Loading Graphs

### Save
**File → Save As…**  
Exports a `.json` file with:

```json
{
  "nodes": [{ "x": ..., "y": ... }],
```

Load

File → Open…
Reads a previously saved graph and redraws it.

💻 Running from Source

Install Python 3.8+

Create a file graph_visualizer.py

Paste the full code

Run:
```bash
python graph_visualizer.py
```
📁 Project Structure
```bash
GraphAlgorithmsVisualizer/
│
├── graph_visualizer.py      # Main application
├── README.md                # Documentation
└── /releases                # (optional) compiled executables on GitHub
```

📝 License

This project is distributed under the MIT License.
You may fork, use, and modify freely while crediting the original author.

👨‍💻 Author

Taiga0727
Designed for algorithm learning, visualization, and educational projects.

---
