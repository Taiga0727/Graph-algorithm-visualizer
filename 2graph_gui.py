from heapq import heappush, heappop
from collections import deque
import math
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json

INDEX_BASE = 1

label_to_index = {}
index_to_label = {}


def index_to_letters(i: int) -> str:
    """แปลง 0 -> 1, 1 -> 2, ..."""
    return str(i + 1)

def format_vertex(i: int) -> str:
    return index_to_letters(i)


def parse_vertex_token(tok: str) -> int:
    tok = tok.strip()
    if tok.isdigit():
        return int(tok) - INDEX_BASE
    if tok in label_to_index:
        return label_to_index[tok]
    print("Unknown vertex label:", tok)
    raise SystemExit


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.edges = []

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
        self.edges.append((w, u, v))
        self.edges.append((w, v, u))


# ---------- DFS ----------
def dfs_spanning_tree(g, start):
    visited = [False] * g.n
    tree = []

    def dfs(u):
        visited[u] = True
        for v, w in g.adj[u]:
            if not visited[v]:
                tree.append((u, v, w))
                dfs(v)

    dfs(start)
    unreach = [i for i in range(g.n) if not visited[i]]
    return tree, unreach


# ---------- BFS ----------
def bfs_spanning_tree(g, start):
    visited = [False] * g.n
    tree = []
    q = deque()

    visited[start] = True
    q.append(start)

    while q:
        u = q.popleft()
        for v, w in g.adj[u]:
            if not visited[v]:
                visited[v] = True
                tree.append((u, v, w))
                q.append(v)

    unreach = [i for i in range(g.n) if not visited[i]]
    return tree, unreach


# ---------- Dijkstra ----------
def dijkstra(g, src, dest):
    dist = [math.inf] * g.n
    parent = [-1] * g.n

    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, u = heappop(heap)
        if d != dist[u]:
            continue
        if u == dest:
            break

        for v, w in g.adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(heap, (nd, v))

    if dist[dest] == math.inf:
        return math.inf, []

    path = []
    cur = dest
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return dist[dest], path


# ---------- Prim ----------
def prim(g, start):
    visited = [False] * g.n
    visited[start] = True
    heap = []

    for v, w in g.adj[start]:
        heappush(heap, (w, start, v))

    mst = []
    total = 0

    while heap and len(mst) < g.n - 1:
        w, u, v = heappop(heap)
        if visited[v]:
            continue

        visited[v] = True
        mst.append((u, v, w))
        total += w

        for to, ww in g.adj[v]:
            if not visited[to]:
                heappush(heap, (ww, v, to))

    if len(mst) != g.n - 1:
        return None, math.inf
    return mst, total


# ---------- Kruskal ----------
def kruskal(g):
    parent = [i for i in range(g.n)]
    rank = [0] * g.n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True

    mst = []
    total = 0

    for w, u, v in sorted(g.edges):
        if union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == g.n - 1:
                break

    if len(mst) != g.n - 1:
        return None, math.inf
    return mst, total

# ---------- Modern Floating Dropdown with Smooth Animation ----------
class FloatingDropdown(tk.Frame):
    """macOS-style floating dropdown with smooth expand/collapse animation"""
    def __init__(self, parent, title, icon, accent_color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            bg="#1c1c1e",
            highlightthickness=1,
            highlightbackground="#2c2c2e",
            bd=0,
        )

        self.title_font = ("SF Pro Text", 11, "bold")
        self.item_font = ("SF Pro Text", 10)
        self.item_font_hover = ("SF Pro Text", 10, "bold")

        self.opened = False
        self.accent = accent_color
        self.items_frame = tk.Frame(self, bg="#1c1c1e", bd=0)

        # Title bar with icon
        self.title_bar = tk.Frame(self, bg="#1c1c1e", cursor="hand2")
        self.title_bar.pack(fill="x", padx=10, pady=8)

        self.indicator = tk.Label(
            self.title_bar,
            text="›",
            font=("SF Pro Display", 14, "bold"),
            fg="#8e8e93",
            bg="#1c1c1e"
        )
        self.indicator.pack(side="left")

        self.icon_label = tk.Label(
            self.title_bar,
            text=icon,
            font=("SF Pro Display", 13),
            fg=accent_color,
            bg="#1c1c1e"
        )
        self.icon_label.pack(side="left", padx=(6, 4))

        self.title_label = tk.Label(
            self.title_bar,
            text=title,
            font=self.title_font,
            fg="#f5f5f7",
            bg="#1c1c1e",
        )
        self.title_label.pack(side="left")

        # Bind click events
        for w in (self.title_bar, self.title_label, self.indicator, self.icon_label):
            w.bind("<Button-1>", self.toggle)
            w.bind("<Enter>", self._on_hover)
            w.bind("<Leave>", self._on_leave)

        self._hovered = False
        self.buttons = []

    def _on_hover(self, _event):
        if not self._hovered:
            self._hovered = True
            self.configure(highlightbackground=self.accent, highlightthickness=2)
            self.title_label.configure(fg="#ffffff")
            self.icon_label.configure(fg=self._brighten(self.accent))

    def _on_leave(self, _event):
        x, y = self.winfo_pointerxy()
        widget_under = self.winfo_containing(x, y)
        if widget_under is None or not str(widget_under).startswith(str(self)):
            self._hovered = False
            self.configure(highlightbackground="#2c2c2e", highlightthickness=1)
            self.title_label.configure(fg="#f5f5f7")
            self.icon_label.configure(fg=self.accent)

    def _brighten(self, color):
        """Brighten hex color for hover effect"""
        try:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def toggle(self, _event=None):
        if self.opened:
            self.close()
        else:
            self.open()

    def open(self):
        if self.opened:
            return
        self.opened = True
        self.indicator.configure(text="∨")
        self.items_frame.pack(fill="x", padx=8, pady=(0, 8))

    def close(self):
        if not self.opened:
            return
        self.opened = False
        self.indicator.configure(text="›")
        self.items_frame.forget()

    def add_item(self, text, command, icon="") -> tk.Button:
        item_frame = tk.Frame(self.items_frame, bg="#1c1c1e")
        item_frame.pack(fill="x", pady=1)

        btn = tk.Button(
            item_frame,
            text=f"{icon}  {text}" if icon else text,
            command=command,
            font=self.item_font,
            bg="#2c2c2e",
            fg="#f5f5f7",
            activebackground="#3a3a3c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            anchor="w",
            cursor="hand2"
        )
        btn.pack(fill="x")

        def on_enter(_e, b=btn):
            b.configure(font=self.item_font_hover, bg="#3a3a3c", fg="#ffffff")

        def on_leave(_e, b=btn):
            b.configure(font=self.item_font, bg="#2c2c2e", fg="#f5f5f7")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        self.buttons.append(btn)
        return btn

    def add_separator(self):
        sep = tk.Frame(self.items_frame, bg="#3a3a3c", height=1)
        sep.pack(fill="x", padx=8, pady=4)


# ---------- Modern Toolbar Button ----------
class ToolbarButton(tk.Frame):
    """macOS-style toolbar button with icon and label"""
    def __init__(self, parent, icon, label, command, accent_color="#007aff", *args, **kwargs):
        super().__init__(parent, bg="#1c1c1e", *args, **kwargs)
        self.command = command
        self.accent = accent_color
        self.active = False

        self.btn = tk.Button(
            self,
            text=f"{icon}\n{label}",
            font=("SF Pro Display", 10),
            bg="#2c2c2e",
            fg="#f5f5f7",
            activebackground="#3a3a3c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._on_click
        )
        self.btn.pack()

        self.btn.bind("<Enter>", self._on_hover)
        self.btn.bind("<Leave>", self._on_leave)

    def _on_hover(self, _e):
        if not self.active:
            self.btn.configure(bg="#3a3a3c")

    def _on_leave(self, _e):
        if not self.active:
            self.btn.configure(bg="#2c2c2e")

    def _on_click(self):
        self.command()

    def set_active(self, active):
        self.active = active
        if active:
            self.btn.configure(bg=self.accent, fg="#ffffff")
        else:
            self.btn.configure(bg="#2c2c2e", fg="#f5f5f7")


# ---------- Modern Result Panel ----------
class ResultPanel(tk.Frame):
    """macOS-style result panel with smooth animations"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#1c1c1e", highlightthickness=1, 
                        highlightbackground="#2c2c2e", bd=0, *args, **kwargs)

        # Title bar
        title_bar = tk.Frame(self, bg="#1c1c1e")
        title_bar.pack(fill="x", padx=12, pady=(10, 6))

        title_icon = tk.Label(
            title_bar,
            text="📊",
            font=("SF Pro Display", 12),
            bg="#1c1c1e"
        )
        title_icon.pack(side="left")

        title_label = tk.Label(
            title_bar,
            text="Results",
            font=("SF Pro Text", 11, "bold"),
            fg="#f5f5f7",
            bg="#1c1c1e"
        )
        title_label.pack(side="left", padx=6)

        self.status_label = tk.Label(
            title_bar,
            text="",
            font=("SF Pro Text", 9),
            fg="#8e8e93",
            bg="#1c1c1e"
        )
        self.status_label.pack(side="right")

        # Text area with custom scrollbar
        text_container = tk.Frame(self, bg="#1c1c1e")
        text_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        self.text = tk.Text(
            text_container,
            width=40,
            height=12,
            bg="#2c2c2e",
            fg="#f5f5f7",
            relief=tk.FLAT,
            wrap=tk.WORD,
            insertbackground="#007aff",
            font=("SF Mono", 10),
            padx=10,
            pady=8,
            spacing1=2,
            spacing3=2
        )
        self.text.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_container, command=self.text.yview, 
                                bg="#1c1c1e", troughcolor="#2c2c2e",
                                activebackground="#3a3a3c")
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        # Hover effect
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

    def _on_hover(self, _e):
        self.configure(highlightbackground="#007aff", highlightthickness=2)

    def _on_leave(self, _e):
        x, y = self.master.winfo_pointerxy()
        widget_under = self.master.winfo_containing(x, y)
        if widget_under is None or not str(widget_under).startswith(str(self)):
            self.configure(highlightbackground="#2c2c2e", highlightthickness=1)

    def log(self, text, status=""):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, text)
        self.status_label.configure(text=status)

    def append(self, text):
        self.text.insert(tk.END, text)
        self.text.see(tk.END)

# ---------- Main Graph GUI Application ----------
class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Algorithm Visualizer")

        # --- macOS-inspired Dark Theme ---
        self.bg_main = "#000000"
        self.bg_canvas = "#0a0a0a"
        self.bg_panel = "#1c1c1e"
        self.bg_secondary = "#2c2c2e"
        self.bg_tertiary = "#3a3a3c"
        
        self.accent_blue = "#007aff"
        self.accent_purple = "#af52de"
        self.accent_green = "#30d158"
        self.accent_orange = "#ff9f0a"
        self.accent_red = "#ff453a"
        self.accent_pink = "#ff375f"
        
        self.text_primary = "#f5f5f7"
        self.text_secondary = "#8e8e93"
        self.text_tertiary = "#636366"
        
        # Node colors
        self.default_node_color = "#007aff"
        self.default_node_outline = "#0a84ff"
        self.node_text_color = "#ffffff"
        self.selected_node_color = "#ff9f0a"
        self.source_node_color = "#30d158"
        self.target_node_color = "#ff453a"
        
        # Edge colors
        self.edge_color = "#48484a"
        self.edge_highlight_color = "#ff375f"
        self.edge_selected_color = "#af52de"
        
        self.anim_delay = 320  # Smoother animation timing

        self.root.configure(bg=self.bg_main)

        # --- Menu Bar ---
        menubar = tk.Menu(self.root, bg=self.bg_panel, fg=self.text_primary, 
                         tearoff=0, relief=tk.FLAT)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_panel, 
                           fg=self.text_primary, activebackground=self.accent_blue,
                           activeforeground=self.text_primary)
        file_menu.add_command(label="New Graph       ⌘N", command=self.clear_graph)
        file_menu.add_command(label="Open...         ⌘O", command=self.load_graph)
        file_menu.add_command(label="Save As...      ⌘S", command=self.save_graph)
        file_menu.add_separator()
        file_menu.add_command(label="Exit            ⌘Q", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_panel,
                           fg=self.text_primary, activebackground=self.accent_blue,
                           activeforeground=self.text_primary)
        edit_menu.add_command(label="Delete Selected ⌫", command=self.delete_selected)
        edit_menu.add_command(label="Select All      ⌘A", command=self.select_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset Colors", command=self.reset_all_colors)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_panel,
                           fg=self.text_primary, activebackground=self.accent_blue,
                           activeforeground=self.text_primary)
        view_menu.add_command(label="Zoom In         ⌘+", command=lambda: self.zoom(1.15))
        view_menu.add_command(label="Zoom Out        ⌘-", command=lambda: self.zoom(1/1.15))
        view_menu.add_command(label="Fit to Screen   ⌘0", command=self.fit_to_screen)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=menubar)

        # --- Canvas (Main drawing area) ---
        self.canvas = tk.Canvas(
            root,
            width=1200,
            height=700,
            bg=self.bg_canvas,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # --- Floating Controls (Left side) ---
        self.alg_buttons = {}
        self.tool_buttons = {}

        controls_bg = tk.Frame(self.root, bg=self.bg_main, bd=0)
        controls_bg.place(x=16, y=16)

        self.controls_container = tk.Frame(controls_bg, bg=self.bg_main, bd=0)
        self.controls_container.pack(padx=4, pady=4)

        # Algorithm Dropdown
        self.alg_dropdown = FloatingDropdown(
            self.controls_container,
            title="Algorithms",
            icon="⚡",
            accent_color=self.accent_purple
        )
        self.alg_dropdown.pack(fill="x", pady=3)

        self.alg_buttons["dfs"] = self.alg_dropdown.add_item("DFS Traversal", self.choose_dfs, "🌲")
        self.alg_buttons["bfs"] = self.alg_dropdown.add_item("BFS Traversal", self.choose_bfs, "🔄")
        self.alg_dropdown.add_separator()
        self.alg_buttons["dijkstra"] = self.alg_dropdown.add_item("Dijkstra Path", self.choose_dijkstra, "🎯")
        self.alg_dropdown.add_separator()
        self.alg_buttons["prim"] = self.alg_dropdown.add_item("Prim MST", self.choose_prim, "🌳")
        self.alg_buttons["kruskal"] = self.alg_dropdown.add_item("Kruskal MST", self.run_kruskal, "🔗")

        # Tools Dropdown
        self.tools_dropdown = FloatingDropdown(
            self.controls_container,
            title="Tools",
            icon="🛠",
            accent_color=self.accent_blue
        )
        self.tools_dropdown.pack(fill="x", pady=3)

        self.tool_buttons["build"] = self.tools_dropdown.add_item("Draw Mode", lambda: self.set_mode("build"), "✏️")
        self.tool_buttons["mouse"] = self.tools_dropdown.add_item("Select & Pan", lambda: self.set_mode("mouse"), "👆")
        self.tool_buttons["move"] = self.tools_dropdown.add_item("Move Nodes", lambda: self.set_mode("move"), "↔️")
        self.tools_dropdown.add_separator()
        self.tool_buttons["del_node"] = self.tools_dropdown.add_item("Delete Node", lambda: self.set_mode("del_node"), "🗑")
        self.tool_buttons["del_edge"] = self.tools_dropdown.add_item("Delete Edge", lambda: self.set_mode("del_edge"), "✂️")

        # View Dropdown
        self.view_dropdown = FloatingDropdown(
            self.controls_container,
            title="View",
            icon="👁",
            accent_color=self.accent_green
        )
        self.view_dropdown.pack(fill="x", pady=3)

        self.view_dropdown.add_item("Zoom In", lambda: self.zoom(1.15), "➕")
        self.view_dropdown.add_item("Zoom Out", lambda: self.zoom(1/1.15), "➖")
        self.view_dropdown.add_item("Fit Screen", self.fit_to_screen, "⛶")
        self.view_dropdown.add_separator()
        self.view_dropdown.add_item("Reset Colors", self.reset_all_colors, "🎨")
        self.view_dropdown.add_item("Clear Graph", self.clear_graph, "🗑")

        # --- Result Panel (Bottom right) ---
        self.result_panel = ResultPanel(self.root)
        self.result_width = 400
        self.result_height = 260
        self.result_panel.place(
            relx=1.0, rely=1.0,
            anchor="se",
            x=-16, y=-16,
            width=self.result_width,
            height=self.result_height
        )

        # --- Internal State ---
        self.node_radius = 20
        self.node_positions = []
        self.node_items = {}
        self.edge_items = {}
        self.line_to_edge = {}
        self.text_to_edge = {}
        self.graph = Graph(0)

        self.mode = "build"
        self.edge_start = None
        self.dijkstra_src = None
        self.dragging_node = None
        self.last_mouse_pos = None
        self.pan_last_pos = None
        self.selected_nodes = set()
        self.selection_rect = None
        self.sel_start = None

        # --- Event Bindings ---
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_linux_up)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_linux_down)

        self.root.bind("<Delete>", self.on_delete_key)
        self.root.bind("<BackSpace>", self.on_delete_key)
        self.root.bind("<Command-a>", lambda e: self.select_all())  # macOS
        self.root.bind("<Control-a>", lambda e: self.select_all())  # Windows/Linux

        # --- Initialize ---
        self.set_mode("build")
        self.alg_dropdown.close()
        self.tools_dropdown.open()
        self.view_dropdown.close()

        self.log_welcome()

    def log_welcome(self):
        welcome = """Welcome to Graph Visualizer! 🎨

Quick Start:
- Draw Mode: Click to add nodes (A, B, C...)
  Click two nodes to connect them
- Select & Pan: Click nodes to select
  Drag background to pan the canvas
- Move Mode: Drag nodes around
- Algorithms: Choose DFS, BFS, Dijkstra, etc.

Shortcuts:
⌘/Ctrl + Scroll = Fast zoom
Delete/⌫ = Remove selected items

Ready to create your graph!"""
        self.result_panel.log(welcome, "Ready")

    # --- Utility Methods ---
    def log(self, text, status=""):
        self.result_panel.log(text, status)

    def set_mode(self, mode):
        self.mode = mode
        # Update cursor
        cursors = {
            "build": "crosshair",
            "mouse": "hand2",
            "move": "fleur",
            "del_node": "X_cursor",
            "del_edge": "X_cursor"
        }
        self.canvas.config(cursor=cursors.get(mode, "arrow"))
        
        # Highlight active tool
        for name, btn in self.tool_buttons.items():
            btn.configure(bg=self.bg_secondary)
        if mode in self.tool_buttons:
            self.tool_buttons[mode].configure(bg=self.accent_blue)

    def set_active_algorithm(self, key=None):
        for name, btn in self.alg_buttons.items():
            btn.configure(bg=self.bg_secondary)
        if key and key in self.alg_buttons:
            self.alg_buttons[key].configure(bg=self.accent_purple)

    def find_node_at(self, x, y):
        for i, (nx, ny) in enumerate(self.node_positions):
            dx, dy = x - nx, y - ny
            if dx * dx + dy * dy <= self.node_radius * self.node_radius:
                return i
        return None

    def reset_node_colors(self):
        for idx, (circle_id, text_id) in self.node_items.items():
            self.canvas.itemconfig(circle_id, fill=self.default_node_color, 
                                  outline=self.default_node_outline, width=2)

    def highlight_node(self, idx, color=None, glow=True):
        if idx is None or idx not in self.node_items:
            return
        color = color or self.selected_node_color
        circle_id, _ = self.node_items[idx]
        width = 3 if glow else 2
        self.canvas.itemconfig(circle_id, fill=color, outline=color, width=width)

    def reset_edge_colors(self):
        for (u, v), (line_id, text_id, w) in self.edge_items.items():
            self.canvas.itemconfig(line_id, fill=self.edge_color, width=2, dash=())

    def reset_all_colors(self):
        self.reset_node_colors()
        self.reset_edge_colors()
        for idx in self.selected_nodes:
            self.highlight_node(idx, self.selected_node_color, glow=False)

    def edge_coords(self, u, v):
        """Calculate edge endpoints at circle boundary"""
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) or 1.0
        r = self.node_radius
        sx = x1 + dx * r / dist
        sy = y1 + dy * r / dist
        ex = x2 - dx * r / dist
        ey = y2 - dy * r / dist
        return sx, sy, ex, ey
    
# --- Animation Methods ---
    def animate_edges(self, edge_list, header_lines):
        """Animate edges with smooth wave effect"""
        if not edge_list:
            self.log("\n".join(header_lines) + "\n\n(No edges in result)")
            return

        step_lines = header_lines[:]
        for i, (u, v, w) in enumerate(edge_list, 1):
            step_lines.append(f"Step {i}: {format_vertex(u)} → {format_vertex(v)} (weight={w})")

        self.log("\n".join(step_lines), f"{len(edge_list)} edges")
        self.reset_edge_colors()

        def pulse_wave(line_id, k, color):
            """Smooth pulsing wave animation"""
            if k <= 0:
                self.canvas.itemconfig(line_id, width=3, fill=color)
                return
            # Sine wave for smooth pulsing
            intensity = 2 + abs(math.sin(k * 0.5)) * 2
            self.canvas.itemconfig(line_id, width=int(intensity))
            self.root.after(60, lambda: pulse_wave(line_id, k - 1, color))

        def step(i):
            if i >= len(edge_list):
                return
            u, v, w = edge_list[i]
            item = self.edge_items.get((u, v)) or self.edge_items.get((v, u))
            if item:
                line_id, text_id, _ = item
                self.canvas.itemconfig(line_id, fill=self.edge_highlight_color, dash=(6, 3))
                self.canvas.itemconfig(text_id, fill=self.accent_pink, 
                                      font=("SF Mono", 11, "bold"))
                pulse_wave(line_id, 8, self.edge_highlight_color)
            self.root.after(self.anim_delay, lambda: step(i + 1))

        step(0)

    def animate_path_nodes(self, path, delay=0):
        """Animate nodes along a path with stagger effect"""
        def color_step(i):
            if i >= len(path):
                return
            node = path[i]
            if i == 0:
                self.highlight_node(node, self.source_node_color, glow=True)
            elif i == len(path) - 1:
                self.highlight_node(node, self.target_node_color, glow=True)
            else:
                self.highlight_node(node, self.selected_node_color, glow=True)
            
            # Bounce effect
            if node in self.node_items:
                circle_id, text_id = self.node_items[node]
                self._bounce_node(circle_id, text_id, node)
            
            self.root.after(self.anim_delay // 2, lambda: color_step(i + 1))

        self.root.after(delay, lambda: color_step(0))

    def _bounce_node(self, circle_id, text_id, idx):
        """Small bounce animation for node"""
        x, y = self.node_positions[idx]
        r = self.node_radius
        
        def bounce(step, direction=1):
            if step > 6:
                # Reset to original position
                self.canvas.coords(circle_id, x - r, y - r, x + r, y + r)
                self.canvas.coords(text_id, x, y)
                return
            
            offset = direction * (3 - abs(step - 3)) * 0.8
            self.canvas.coords(circle_id, x - r, y - r + offset, x + r, y + r + offset)
            self.canvas.coords(text_id, x, y + offset)
            
            self.root.after(30, lambda: bounce(step + 1, direction))
        
        bounce(0)

    # --- Node & Edge Creation ---
    def add_node(self, x, y):
        idx = len(self.node_positions)
        self.node_positions.append((x, y))

        # Expand graph
        new_g = Graph(idx + 1)
        for u in range(self.graph.n):
            for v, w in self.graph.adj[u]:
                if u < new_g.n and v < new_g.n:
                    new_g.adj[u].append((v, w))
        for w, u, v in self.graph.edges:
            if u < new_g.n and v < new_g.n:
                new_g.edges.append((w, u, v))
        self.graph = new_g

        # แทนที่ fill="#00000040" ด้วยสีทึบ
        shadow = self.canvas.create_oval(
            x - self.node_radius + 2, y - self.node_radius + 2,
            x + self.node_radius + 2, y + self.node_radius + 2,
            fill="#1a1a1a", outline="", width=0  # <--- ใช้สีเทาเข้มทึบแทน
        )
        
        circle_id = self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill=self.default_node_color,
            outline=self.default_node_outline,
            width=2
        )
        
        label = format_vertex(idx)
        text_id = self.canvas.create_text(
            x, y,
            text=label,
            fill=self.node_text_color,
            font=("SF Pro Display", 12, "bold")
        )
        
        self.node_items[idx] = (circle_id, text_id)
        
        # Pop-in animation
        self._pop_in_node(circle_id, text_id, x, y)

    def _pop_in_node(self, circle_id, text_id, x, y):
        """Scale-in animation for new nodes"""
        def scale(step):
            if step > 5:
                return
            progress = step / 5.0
            scale_factor = 0.3 + progress * 0.7
            r = self.node_radius * scale_factor
            self.canvas.coords(circle_id, x - r, y - r, x + r, y + r)
            self.root.after(30, lambda: scale(step + 1))
        scale(0)

    def add_edge_with_weight(self, u, v):
        if u == v:
            return
        
        # Custom dialog with macOS style
        dialog = tk.Toplevel(self.root)
        dialog.title("Edge Weight")
        dialog.configure(bg=self.bg_panel)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        label = tk.Label(
            dialog,
            text=f"Enter weight for edge {format_vertex(u)} → {format_vertex(v)}:",
            font=("SF Pro Text", 11),
            fg=self.text_primary,
            bg=self.bg_panel
        )
        label.pack(pady=20)
        
        entry = tk.Entry(
            dialog,
            font=("SF Mono", 12),
            bg=self.bg_secondary,
            fg=self.text_primary,
            insertbackground=self.accent_blue,
            relief=tk.FLAT,
            bd=0
        )
        entry.pack(pady=10, padx=20, fill="x")
        entry.insert(0, "1")
        entry.select_range(0, tk.END)
        entry.focus()
        
        result = [None]
        
        def on_ok():
            try:
                w = int(entry.get())
                if w < 0:
                    raise ValueError
                result[0] = w
                dialog.destroy()
            except:
                entry.delete(0, tk.END)
                entry.insert(0, "Invalid!")
                entry.select_range(0, tk.END)
        
        def on_cancel():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.bg_panel)
        btn_frame.pack(pady=10)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=on_cancel,
            font=("SF Pro Text", 10),
            bg=self.bg_secondary,
            fg=self.text_primary,
            activebackground=self.bg_tertiary,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=6
        )
        cancel_btn.pack(side="left", padx=5)
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            command=on_ok,
            font=("SF Pro Text", 10, "bold"),
            bg=self.accent_blue,
            fg="#ffffff",
            activebackground=self.accent_purple,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=6
        )
        ok_btn.pack(side="left", padx=5)
        
        entry.bind("<Return>", lambda e: on_ok())
        entry.bind("<Escape>", lambda e: on_cancel())
        
        self.root.wait_window(dialog)
        
        w = result[0]
        if w is None:
            return

        self.graph.add_edge(u, v, w)

        sx, sy, ex, ey = self.edge_coords(u, v)
        line_id = self.canvas.create_line(
            sx, sy, ex, ey,
            width=2,
            fill=self.edge_color,
            smooth=True,
            capstyle=tk.ROUND
        )
        
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        weight_id = self.canvas.create_text(
            mx, my - 12,
            text=str(w),
            font=("SF Mono", 10, "bold"),
            fill=self.text_secondary
        )

        self.edge_items[(u, v)] = (line_id, weight_id, w)
        self.edge_items[(v, u)] = (line_id, weight_id, w)

        cu, cv = sorted((u, v))
        self.line_to_edge[line_id] = (cu, cv)
        self.text_to_edge[weight_id] = (cu, cv)
        
        # Draw animation
        self._draw_edge_animation(line_id)

    def _draw_edge_animation(self, line_id):
        """Animate edge drawing with dash effect"""
        def animate(step):
            if step > 8:
                self.canvas.itemconfig(line_id, dash=())
                return
            dash_pattern = (step * 2, 10 - step * 2)
            self.canvas.itemconfig(line_id, dash=dash_pattern)
            self.root.after(40, lambda: animate(step + 1))
        animate(1)

    # --- Delete Methods ---
    def delete_edge_by_item(self, item_id):
        key = None
        if item_id in self.line_to_edge:
            key = self.line_to_edge[item_id]
        elif item_id in self.text_to_edge:
            key = self.text_to_edge[item_id]
        if key is None:
            return
        u, v = key
        self.remove_edge_pair(u, v)

    def remove_edge_pair(self, u, v):
        item = self.edge_items.get((u, v)) or self.edge_items.get((v, u))
        if not item:
            return
        line_id, weight_id, w = item

        # Fade out animation
        self._fade_out_edge(line_id, weight_id)

        # Update graph structure
        self.graph.adj[u] = [(to, ww) for (to, ww) in self.graph.adj[u] 
                            if not (to == v and ww == w)]
        self.graph.adj[v] = [(to, ww) for (to, ww) in self.graph.adj[v] 
                            if not (to == u and ww == w)]

        new_edges = []
        for ww, uu, vv in self.graph.edges:
            if (uu == u and vv == v and ww == w) or (uu == v and vv == u and ww == w):
                continue
            new_edges.append((ww, uu, vv))
        self.graph.edges = new_edges

        # Clean up references
        for key in [(u, v), (v, u)]:
            if key in self.edge_items:
                del self.edge_items[key]

        if line_id in self.line_to_edge:
            del self.line_to_edge[line_id]
        if weight_id in self.text_to_edge:
            del self.text_to_edge[weight_id]

    def _fade_out_edge(self, line_id, weight_id):
        """Fade out animation for edge deletion"""
        def fade(step):
            if step > 5:
                self.canvas.delete(line_id)
                self.canvas.delete(weight_id)
                return
            alpha = 1.0 - (step / 5.0)
            # Simulate fade by changing to lighter color
            self.canvas.itemconfig(line_id, width=max(1, int(3 - step * 0.5)))
            self.root.after(40, lambda: fade(step + 1))
        fade(0)

    def delete_node(self, del_idx):
        if del_idx < 0 or del_idx >= self.graph.n:
            return

        if del_idx in self.node_items:
            circle_id, text_id = self.node_items[del_idx]
            # Fade out animation
            def shrink(step):
                if step > 5:
                    self.canvas.delete(circle_id)
                    self.canvas.delete(text_id)
                    return
                scale = 1.0 - (step / 5.0)
                x, y = self.node_positions[del_idx]
                r = self.node_radius * scale
                self.canvas.coords(circle_id, x - r, y - r, x + r, y + r)
                self.root.after(40, lambda: shrink(step + 1))
            shrink(0)

        # Delete connected edges
        to_delete_lines = set()
        to_delete_texts = set()
        for (u, v), (line_id, weight_id, w) in list(self.edge_items.items()):
            if u == del_idx or v == del_idx:
                to_delete_lines.add(line_id)
                to_delete_texts.add(weight_id)
                del self.edge_items[(u, v)]

        for line_id in to_delete_lines:
            self.canvas.delete(line_id)
            if line_id in self.line_to_edge:
                del self.line_to_edge[line_id]
        for text_id in to_delete_texts:
            self.canvas.delete(text_id)
            if text_id in self.text_to_edge:
                del self.text_to_edge[text_id]

        # Remap indices
        old_n = self.graph.n
        idx_map = {}
        new_idx = 0
        for old_idx in range(old_n):
            if old_idx == del_idx:
                continue
            idx_map[old_idx] = new_idx
            new_idx += 1

        # Rebuild graph
        new_g = Graph(old_n - 1)
        for w, u, v in self.graph.edges:
            if u == del_idx or v == del_idx:
                continue
            nu = idx_map[u]
            nv = idx_map[v]
            if nu <= nv:
                new_g.add_edge(nu, nv, w)
        self.graph = new_g

        # Update positions
        new_positions = []
        for old_idx, pos in enumerate(self.node_positions):
            if old_idx == del_idx:
                continue
            new_positions.append(pos)
        self.node_positions = new_positions

        # Update selection
        new_selected = set()
        for old_idx, new_idx in idx_map.items():
            if old_idx in self.selected_nodes:
                new_selected.add(new_idx)
        self.selected_nodes = new_selected

        self.root.after(250, self.redraw_all)

    def delete_selected(self):
        if not self.selected_nodes:
            messagebox.showinfo("Delete", "No nodes selected", parent=self.root)
            return
        count = len(self.selected_nodes)
        for idx in sorted(self.selected_nodes, reverse=True):
            self.delete_node(idx)
        self.selected_nodes = set()
        self.log(f"Deleted {count} node(s)", "Done")

    def select_all(self):
        self.selected_nodes = set(range(self.graph.n))
        self.reset_node_colors()
        for idx in self.selected_nodes:
            self.highlight_node(idx, self.selected_node_color, glow=False)
        self.log(f"Selected all {self.graph.n} nodes", f"{self.graph.n} nodes")

    def redraw_all(self):
        """Redraw entire graph with smooth transitions"""
        self.canvas.delete("all")
        self.node_items.clear()
        self.edge_items.clear()
        self.line_to_edge.clear()
        self.text_to_edge.clear()

        # Draw edges first (behind nodes)
        drawn = set()
        for w, u, v in self.graph.edges:
            cu, cv = sorted((u, v))
            if (cu, cv) in drawn:
                continue
            drawn.add((cu, cv))
            sx, sy, ex, ey = self.edge_coords(cu, cv)
            line_id = self.canvas.create_line(
                sx, sy, ex, ey,
                width=2,
                fill=self.edge_color,
                smooth=True,
                capstyle=tk.ROUND
            )
            mx, my = (sx + ex) / 2, (sy + ey) / 2
            weight_id = self.canvas.create_text(
                mx, my - 12,
                text=str(w),
                font=("SF Mono", 10, "bold"),
                fill=self.text_secondary
            )

            self.edge_items[(cu, cv)] = (line_id, weight_id, w)
            self.edge_items[(cv, cu)] = (line_id, weight_id, w)
            self.line_to_edge[line_id] = (cu, cv)
            self.text_to_edge[weight_id] = (cu, cv)

        # Draw nodes with shadows
        for idx, (x, y) in enumerate(self.node_positions):
            shadow = self.canvas.create_oval(
                x - self.node_radius + 2, y - self.node_radius + 2,
                x + self.node_radius + 2, y + self.node_radius + 2,
                fill="#1a1a1a", outline="", width=0  # <--- เปลี่ยนเป็นสีทึบ
            )
            
            circle_id = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill=self.default_node_color,
                outline=self.default_node_outline,
                width=2
            )
            label = format_vertex(idx)
            text_id = self.canvas.create_text(
                x, y,
                text=label,
                fill=self.node_text_color,
                font=("SF Pro Display", 12, "bold")
            )
            self.node_items[idx] = (circle_id, text_id)

        # Restore selection highlights
        for idx in self.selected_nodes:
            if idx in self.node_items:
                self.highlight_node(idx, self.selected_node_color, glow=False)

    def clear_graph(self):
        """Clear entire graph with confirmation"""
        if self.graph.n > 0:
            response = messagebox.askyesno(
                "Clear Graph",
                "Are you sure you want to clear the entire graph?",
                parent=self.root
            )
            if not response:
                return
        
        self.canvas.delete("all")
        self.node_positions = []
        self.node_items.clear()
        self.edge_items.clear()
        self.line_to_edge.clear()
        self.text_to_edge.clear()
        self.graph = Graph(0)
        self.mode = "build"
        self.edge_start = None
        self.dijkstra_src = None
        self.dragging_node = None
        self.selected_nodes = set()
        self.selection_rect = None
        self.sel_start = None
        self.last_mouse_pos = None
        self.pan_last_pos = None
        self.set_mode("build")
        self.set_active_algorithm(None)
        self.log("Graph cleared. Ready to create!", "Ready")

    # --- Zoom & View Methods ---
    def zoom_at(self, factor, cx, cy):
        if not self.node_positions:
            return
        new_positions = []
        for (x, y) in self.node_positions:
            dx = x - cx
            dy = y - cy
            new_positions.append((cx + dx * factor, cy + dy * factor))
        self.node_positions = new_positions
        self.redraw_all()

    def zoom(self, factor):
        if not self.node_positions:
            return
        try:
            cx = self.canvas.winfo_width() / 2
            cy = self.canvas.winfo_height() / 2
        except:
            cx, cy = 0, 0
        self.zoom_at(factor, cx, cy)

    def fit_to_screen(self):
        """Fit graph to screen with padding"""
        if not self.node_positions:
            return
        
        xs = [x for x, y in self.node_positions]
        ys = [y for x, y in self.node_positions]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        graph_w = max_x - min_x
        graph_h = max_y - min_y
        
        if graph_w == 0 or graph_h == 0:
            return
        
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        padding = 80
        scale_x = (canvas_w - padding * 2) / graph_w
        scale_y = (canvas_h - padding * 2) / graph_h
        scale = min(scale_x, scale_y, 2.0)  # Max 2x zoom
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        target_cx = canvas_w / 2
        target_cy = canvas_h / 2
        
        new_positions = []
        for (x, y) in self.node_positions:
            nx = target_cx + (x - center_x) * scale
            ny = target_cy + (y - center_y) * scale
            new_positions.append((nx, ny))
        
        self.node_positions = new_positions
        self.redraw_all()

    # --- Mouse Wheel Handlers ---
    def on_mouse_wheel(self, event):
        if event.delta == 0:
            return
        base = 1.1 if event.delta > 0 else 1 / 1.1
        if event.state & 0x4:  # Ctrl held
            base = base ** 1.8
        self.zoom_at(base, event.x, event.y)

    def on_mouse_wheel_linux_up(self, event):
        base = 1.1
        if event.state & 0x4:
            base = base ** 1.8
        self.zoom_at(base, event.x, event.y)

    def on_mouse_wheel_linux_down(self, event):
        base = 1 / 1.1
        if event.state & 0x4:
            base = base ** 1.8
        self.zoom_at(base, event.x, event.y)

    def on_delete_key(self, event=None):
        if self.selected_nodes:
            self.delete_selected()
            return

        try:
            x_global, y_global = self.root.winfo_pointerxy()
            x = x_global - self.canvas.winfo_rootx()
            y = y_global - self.canvas.winfo_rooty()
            all_items = self.canvas.find_all()
            if not all_items:
                return
            closest = self.canvas.find_closest(x, y)
            if closest:
                self.delete_edge_by_item(closest[0])
        except:
            pass

    # --- Canvas Click Handler ---
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        idx = self.find_node_at(x, y)

        # Mouse mode: select + pan
        if self.mode == "mouse":
            if idx is not None:
                if event.state & 0x1:  # Shift for multi-select
                    if idx in self.selected_nodes:
                        self.selected_nodes.remove(idx)
                    else:
                        self.selected_nodes.add(idx)
                else:
                    self.selected_nodes = {idx}
                
                self.reset_node_colors()
                for nid in self.selected_nodes:
                    self.highlight_node(nid, self.selected_node_color, glow=False)
                
                self.dragging_node = idx
                self.last_mouse_pos = (x, y)
                self.pan_last_pos = None
            else:
                self.pan_last_pos = (x, y)
                self.dragging_node = None
                self.last_mouse_pos = None
            return

        # Select mode: start selection rectangle
        if self.mode == "select":
            self.sel_start = (x, y)
            if self.selection_rect is not None:
                self.canvas.delete(self.selection_rect)
                self.selection_rect = None
            return

        # Move mode
        if self.mode == "move":
            self.dragging_node = idx
            self.last_mouse_pos = (x, y)
            return

        # Delete node mode
        if self.mode == "del_node":
            if idx is not None:
                self.delete_node(idx)
            return

        # Delete edge mode
        if self.mode == "del_edge":
            closest = self.canvas.find_closest(x, y)
            if closest:
                self.delete_edge_by_item(closest[0])
            return

        # Build mode
        if self.mode == "build":
            if idx is None:
                self.edge_start = None
                self.reset_node_colors()
                self.add_node(x, y)
            else:
                if self.edge_start is None:
                    self.edge_start = idx
                    self.reset_node_colors()
                    self.highlight_node(idx, self.accent_orange, glow=True)
                else:
                    if self.edge_start != idx:
                        self.add_edge_with_weight(self.edge_start, idx)
                    self.edge_start = None
                    self.reset_node_colors()

        # Algorithm modes
        elif self.mode in ("dfs", "bfs", "prim"):
            if idx is not None:
                self.reset_node_colors()
                self.highlight_node(idx, self.source_node_color, glow=True)
                if self.mode == "dfs":
                    self.run_dfs(idx)
                elif self.mode == "bfs":
                    self.run_bfs(idx)
                elif self.mode == "prim":
                    self.run_prim(idx)
                self.set_active_algorithm(None)
                self.set_mode("build")

        elif self.mode in ("dijkstra_src", "dijkstra_dest"):
            if idx is not None:
                if self.mode == "dijkstra_src":
                    self.reset_node_colors()
                    self.dijkstra_src = idx
                    self.highlight_node(idx, self.source_node_color, glow=True)
                    self.mode = "dijkstra_dest"
                    messagebox.showinfo("Dijkstra", "Now click the destination node", parent=self.root)
                else:
                    self.highlight_node(idx, self.target_node_color, glow=True)
                    self.run_dijkstra(self.dijkstra_src, idx)
                    self.set_active_algorithm(None)
                    self.set_mode("build")
                    self.dijkstra_src = None

    # --- Mouse Drag Handler ---
    def on_mouse_drag(self, event):
        x, y = event.x, event.y

        # Mouse mode: pan or move
        if self.mode == "mouse":
            if self.pan_last_pos is not None and self.dragging_node is None:
                dx = x - self.pan_last_pos[0]
                dy = y - self.pan_last_pos[1]
                self.pan_last_pos = (x, y)
                if dx != 0 or dy != 0:
                    for i, (nx, ny) in enumerate(self.node_positions):
                        self.node_positions[i] = (nx + dx, ny + dy)
                    self.redraw_all()
                return

            if self.dragging_node is not None:
                if self.last_mouse_pos is None:
                    self.last_mouse_pos = (x, y)
                    return
                dx = x - self.last_mouse_pos[0]
                dy = y - self.last_mouse_pos[1]
                self.last_mouse_pos = (x, y)

                moving = self.selected_nodes if (self.selected_nodes and 
                         self.dragging_node in self.selected_nodes) else {self.dragging_node}

                for idx in moving:
                    nx, ny = self.node_positions[idx]
                    self.node_positions[idx] = (nx + dx, ny + dy)
                    circle_id, text_id = self.node_items[idx]
                    r = self.node_radius
                    self.canvas.coords(circle_id, nx + dx - r, ny + dy - r, 
                                     nx + dx + r, ny + dy + r)
                    self.canvas.coords(text_id, nx + dx, ny + dy)

                for (u, v), (line_id, weight_id, w) in self.edge_items.items():
                    if u in moving or v in moving:
                        sx, sy, ex, ey = self.edge_coords(u, v)
                        self.canvas.coords(line_id, sx, sy, ex, ey)
                        mx, my = (sx + ex) / 2, (sy + ey) / 2
                        self.canvas.coords(weight_id, mx, my - 12)
                return

        # Select mode: draw selection rectangle
        if self.mode == "select":
            if self.sel_start is None:
                return
            x0, y0 = self.sel_start
            if self.selection_rect is None:
                self.selection_rect = self.canvas.create_rectangle(
                    x0, y0, x, y,
                    outline=self.accent_blue,
                    width=2,
                    dash=(6, 4)
                )
            else:
                self.canvas.coords(self.selection_rect, x0, y0, x, y)
            return

        # Move mode
        if self.mode == "move":
            if self.last_mouse_pos is None:
                self.last_mouse_pos = (x, y)
                return
            dx = x - self.last_mouse_pos[0]
            dy = y - self.last_mouse_pos[1]
            self.last_mouse_pos = (x, y)

            if self.dragging_node is None:
                idx = self.find_node_at(x, y)
                if idx is None:
                    return
                self.dragging_node = idx

            moving = self.selected_nodes if (self.selected_nodes and 
                     self.dragging_node in self.selected_nodes) else {self.dragging_node}

            for idx in moving:
                nx, ny = self.node_positions[idx]
                self.node_positions[idx] = (nx + dx, ny + dy)
                circle_id, text_id = self.node_items[idx]
                r = self.node_radius
                self.canvas.coords(circle_id, nx + dx - r, ny + dy - r, 
                                 nx + dx + r, ny + dy + r)
                self.canvas.coords(text_id, nx + dx, ny + dy)

            for (u, v), (line_id, weight_id, w) in self.edge_items.items():
                if u in moving or v in moving:
                    sx, sy, ex, ey = self.edge_coords(u, v)
                    self.canvas.coords(line_id, sx, sy, ex, ey)
                    mx, my = (sx + ex) / 2, (sy + ey) / 2
                    self.canvas.coords(weight_id, mx, my - 12)

    # --- Mouse Release Handler ---
    def on_mouse_release(self, event):
        if self.mode == "mouse":
            self.dragging_node = None
            self.last_mouse_pos = None
            self.pan_last_pos = None

        if self.mode == "select" and self.sel_start is not None:
            x0, y0 = self.sel_start
            x1, y1 = event.x, event.y
            x_min, x_max = sorted([x0, x1])
            y_min, y_max = sorted([y0, y1])
            self.selected_nodes = set()
            for idx, (nx, ny) in enumerate(self.node_positions):
                if x_min <= nx <= x_max and y_min <= ny <= y_max:
                    self.selected_nodes.add(idx)
            if self.selection_rect is not None:
                self.canvas.delete(self.selection_rect)
                self.selection_rect = None
            self.sel_start = None

            self.reset_node_colors()
            for idx in self.selected_nodes:
                self.highlight_node(idx, self.selected_node_color, glow=False)
            return

        if self.mode == "move":
            self.dragging_node = None
            self.last_mouse_pos = None
    
# --- Save & Load Methods ---
    def save_graph(self):
        if not self.node_positions:
            messagebox.showinfo("Save Graph", "No graph to save!", parent=self.root)
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Graph", "*.json"), ("All Files", "*.*")],
            parent=self.root
        )
        if not path:
            return
        
        edges_set = set()
        for w, u, v in self.graph.edges:
            a, b = sorted((u, v))
            edges_set.add((a, b, w))
        
        data = {
            "nodes": [{"x": x, "y": y} for (x, y) in self.node_positions],
            "edges": [{"u": u, "v": v, "w": w} for (u, v, w) in edges_set],
        }
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.log(f"✓ Graph saved to:\n{path}", "Saved")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save:\n{e}", parent=self.root)

    def load_graph(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON Graph", "*.json"), ("All Files", "*.*")],
            parent=self.root
        )
        if not path:
            return
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load file:\n{e}", parent=self.root)
            return

        nodes = data.get("nodes", [])
        edges = data.get("edges", [])

        self.node_positions = [(float(n["x"]), float(n["y"])) for n in nodes]
        n = len(self.node_positions)
        self.graph = Graph(n)
        
        for e in edges:
            u = int(e["u"])
            v = int(e["v"])
            w = float(e["w"])
            if 0 <= u < n and 0 <= v < n:
                self.graph.add_edge(u, v, w)

        self.selected_nodes = set()
        self.redraw_all()
        self.set_mode("build")
        self.set_active_algorithm(None)
        self.log(f"✓ Graph loaded from:\n{path}\n\nNodes: {n}, Edges: {len(edges)}", "Loaded")

    # --- Algorithm Mode Choosers ---
    def choose_dfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("DFS", "Graph is empty! Add nodes first.", parent=self.root)
            return
        self.mode = "dfs"
        self.reset_node_colors()
        self.set_active_algorithm("dfs")
        messagebox.showinfo("DFS", "Click any node to start DFS traversal", parent=self.root)

    def choose_bfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("BFS", "Graph is empty! Add nodes first.", parent=self.root)
            return
        self.mode = "bfs"
        self.reset_node_colors()
        self.set_active_algorithm("bfs")
        messagebox.showinfo("BFS", "Click any node to start BFS traversal", parent=self.root)

    def choose_prim(self):
        if self.graph.n == 0:
            messagebox.showwarning("Prim MST", "Graph is empty! Add nodes first.", parent=self.root)
            return
        self.mode = "prim"
        self.reset_node_colors()
        self.set_active_algorithm("prim")
        messagebox.showinfo("Prim MST", "Click any node to start Prim's algorithm", parent=self.root)

    def choose_dijkstra(self):
        if self.graph.n == 0:
            messagebox.showwarning("Dijkstra", "Graph is empty! Add nodes first.", parent=self.root)
            return
        self.mode = "dijkstra_src"
        self.reset_node_colors()
        self.set_active_algorithm("dijkstra")
        messagebox.showinfo("Dijkstra", "Click the source node", parent=self.root)

    # --- Algorithm Runners ---
    def run_dfs(self, start):
        tree, un = dfs_spanning_tree(self.graph, start)
        
        header = ["🌲 DFS Spanning Tree"]
        header.append(f"Starting from: {format_vertex(start)}")
        
        if tree:
            seq = [format_vertex(start)]
            for u, v, w in tree:
                seq.append(format_vertex(v))
            header.append(f"Traversal order: {' → '.join(seq)}")
        
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append(f"⚠️ Unreachable nodes: {', '.join(un_labels)}")
        
        header.append("")
        self.animate_edges(tree, header)

    def run_bfs(self, start):
        tree, un = bfs_spanning_tree(self.graph, start)
        
        header = ["🔄 BFS Spanning Tree"]
        header.append(f"Starting from: {format_vertex(start)}")
        
        if tree:
            seq = [format_vertex(start)]
            for u, v, w in tree:
                seq.append(format_vertex(v))
            header.append(f"Traversal order: {' → '.join(seq)}")
        
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append(f"⚠️ Unreachable nodes: {', '.join(un_labels)}")
        
        header.append("")
        self.animate_edges(tree, header)

    def run_prim(self, start):
        mst, total = prim(self.graph, start)
        
        if mst is None:
            messagebox.showinfo("Prim MST", "Graph is not connected!\nNo MST exists.", 
                              parent=self.root)
            self.log("⚠️ Prim MST: Graph not connected", "No MST")
            return
        
        header = ["🌳 Prim's Minimum Spanning Tree"]
        header.append(f"Starting from: {format_vertex(start)}")
        header.append(f"Total weight: {total}")
        
        if mst:
            edge_desc = ", ".join(f"{format_vertex(u)}-{format_vertex(v)}" for (u, v, w) in mst)
            header.append(f"Edges: {edge_desc}")
        
        header.append("")
        self.animate_edges(mst, header)

    def run_kruskal(self):
        if self.graph.n == 0:
            messagebox.showwarning("Kruskal MST", "Graph is empty! Add nodes first.", 
                                 parent=self.root)
            return
        
        mst, total = kruskal(self.graph)
        
        if mst is None:
            messagebox.showinfo("Kruskal MST", "Graph is not connected!\nNo MST exists.", 
                              parent=self.root)
            self.log("⚠️ Kruskal MST: Graph not connected", "No MST")
            return
        
        header = ["🔗 Kruskal's Minimum Spanning Tree"]
        header.append(f"Total weight: {total}")
        
        if mst:
            edge_desc = ", ".join(f"{format_vertex(u)}-{format_vertex(v)}" for (u, v, w) in mst)
            header.append(f"Edges: {edge_desc}")
        
        header.append("")
        self.reset_node_colors()
        self.animate_edges(mst, header)

    def run_dijkstra(self, src, dest):
        dist, path = dijkstra(self.graph, src, dest)
        
        if dist == math.inf:
            messagebox.showinfo("Dijkstra", 
                              f"No path exists from {format_vertex(src)} to {format_vertex(dest)}", 
                              parent=self.root)
            self.log("⚠️ Dijkstra: No path found", "No path")
            return

        edges = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            w = None
            for to, ww in self.graph.adj[u]:
                if to == v:
                    w = ww
                    break
            if w is None:
                continue
            edges.append((u, v, w))

        header = ["🎯 Dijkstra's Shortest Path"]
        header.append(f"From: {format_vertex(src)} → To: {format_vertex(dest)}")
        header.append(f"Total distance: {dist}")
        header.append(f"Path: {' → '.join(format_vertex(v) for v in path)}")
        header.append("")

        self.reset_node_colors()
        self.animate_path_nodes(path, delay=0)
        self.animate_edges(edges, header)


# ---------- Main Entry Point ----------
def main():
    root = tk.Tk()
    root.geometry("1400x850")
    root.minsize(1000, 600)
    
    # macOS-style window title
    try:
        root.tk.call('tk', 'scaling', 2.0)  # Retina support
    except:
        pass
    
    app = GraphGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
