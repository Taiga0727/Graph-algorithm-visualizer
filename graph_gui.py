from heapq import heappush, heappop
from collections import deque
import math
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json

INDEX_BASE = 1   # ยังอยู่ แต่ใน GUI เราใช้ชื่อ A,B,C แทนตัวเลข

label_to_index = {}
index_to_label = {}


def index_to_letters(i: int) -> str:
    """แปลง 0 -> A, 1 -> B, ... 25 -> Z, 26 -> AA, ..."""
    s = ""
    while True:
        s = chr(ord('A') + (i % 26)) + s
        i = i // 26 - 1
        if i < 0:
            break
    return s


def format_vertex(i: int) -> str:
    # ใช้ชื่อแบบ A,B,C,... แทนเลข
    return index_to_letters(i)


def parse_vertex_token(tok: str) -> int:
    # ยังเก็บไว้ให้ครบ แต่ใน GUI ไม่ได้ใช้แล้ว
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


# ---------- DFS (เดิม) ----------
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


# ---------- BFS (เดิม) ----------
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

    unreach = [i for i in g.n if not visited[i]]
    return tree, unreach


# ---------- Dijkstra (เดิม) ----------
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


# ---------- Prim (เดิม) ----------
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


# ---------- Kruskal (เดิม) ----------
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


# ---------- Helper: Floating Dropdown ----------

class FloatingDropdown(tk.Frame):
    """กล่อง dropdown แบบลอย ๆ + ปุ่มขยายเมื่อ hover"""
    def __init__(self, parent, title, accent_color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            bg="#16181f",
            highlightthickness=1,
            highlightbackground="#2c2f3a",
            bd=0,
        )

        self.title_font = ("Segoe UI", 10, "bold")
        self.item_font = ("Segoe UI", 10)
        self.item_font_hover = ("Segoe UI", 11, "bold")

        self.opened = False
        self.items_frame = tk.Frame(self, bg="#16181f", bd=0)

        # title bar
        self.title_bar = tk.Frame(self, bg="#16181f")
        self.title_bar.pack(fill="x", padx=8, pady=6)

        self.indicator = tk.Label(
            self.title_bar,
            text="▶",
            font=("Segoe UI", 9),
            fg="#8f95ff",
            bg="#16181f"
        )
        self.indicator.pack(side="left")

        self.title_label = tk.Label(
            self.title_bar,
            text=title,
            font=self.title_font,
            fg=accent_color,
            bg="#16181f",
            pady=2
        )
        self.title_label.pack(side="left", padx=(4, 0))

        self.title_bar.bind("<Button-1>", self.toggle)
        self.title_label.bind("<Button-1>", self.toggle)
        self.indicator.bind("<Button-1>", self.toggle)

        # hover effect ทั้งกล่อง
        for w in (self, self.title_bar, self.title_label, self.indicator):
            w.bind("<Enter>", self._on_hover)
            w.bind("<Leave>", self._on_leave)

        self._hovered = False

        self.buttons = []

    def _on_hover(self, _event):
        if not self._hovered:
            self._hovered = True
            self.configure(highlightbackground="#4a90e2")
            self.title_label.configure(fg="#d0d4ff")

    def _on_leave(self, _event):
        # เช็คว่าเมาส์ออกจากทุก widget ใน frame จริง ๆ หรือยัง
        x, y = self.winfo_pointerxy()
        widget_under = self.winfo_containing(x, y)
        if widget_under is None or not str(widget_under).startswith(str(self)):
            self._hovered = False
            self.configure(highlightbackground="#2c2f3a")
            self.title_label.configure(fg="#b0b5ff")

    def toggle(self, _event=None):
        if self.opened:
            self.close()
        else:
            self.open()

    def open(self):
        if self.opened:
            return
        self.opened = True
        self.indicator.configure(text="▼")
        self.items_frame.pack(fill="x", padx=8, pady=(0, 6))

    def close(self):
        if not self.opened:
            return
        self.opened = False
        self.indicator.configure(text="▶")
        self.items_frame.forget()

    def add_item(self, text, command) -> tk.Button:
        btn = tk.Button(
            self.items_frame,
            text=text,
            command=command,
            font=self.item_font,
            bg="#20232d",
            fg="#f5f5f5",
            activebackground="#34384a",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=4,
            anchor="w",
        )
        btn.pack(fill="x", pady=2)

        def on_enter(_e, b=btn):
            b.configure(font=self.item_font_hover, bg="#34384a")

        def on_leave(_e, b=btn):
            b.configure(font=self.item_font, bg="#20232d")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        self.buttons.append(btn)
        return btn


# ---------- GUI ----------

class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Algorithms Visualizer")

        # --- Theme (Dark + Minimal Glass) ---
        self.bg_main = "#05060a"
        self.bg_canvas = "#020308"
        self.accent = "#8f95ff"
        self.accent_soft = "#4a90e2"
        self.glass_bg = "#16181f"
        self.glass_border = "#2c2f3a"

        # สี node / edge
        self.default_node_color = "#3498db"
        self.default_node_outline = "#e8f4ff"
        self.node_text_color = "white"
        self.selected_node_color = "#f1c40f"
        self.source_node_color = "#2ecc71"
        self.target_node_color = "#e67e22"

        self.edge_color = "#666b7e"
        self.edge_highlight_color = "#ff7675"

        self.anim_delay = 380  # ms ระหว่างแต่ละ step (ปรับให้ลื่นขึ้นเล็กน้อย)

        self.root.configure(bg=self.bg_main)

        # --- Menu (File: Save / Load) ---
        menubar = tk.Menu(self.root, bg=self.glass_bg, fg="#f5f5f5", tearoff=0)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.clear_graph)
        file_menu.add_command(label="Open...", command=self.load_graph)
        file_menu.add_command(label="Save As...", command=self.save_graph)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

        # --- Canvas (พื้นที่วาดกราฟ) ---
        self.canvas = tk.Canvas(
            root,
            width=960,
            height=540,
            bg=self.bg_canvas,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # --- Floating Controls (ซ้ายบน) ---
        self.alg_buttons = {}
        self.tool_buttons = {}

        self.controls_container = tk.Frame(self.root, bg="", bd=0)
        self.controls_container.place(x=20, y=20)

        # Dropdown Algorithms
        self.alg_dropdown = FloatingDropdown(
            self.controls_container,
            title="Algorithms",
            accent_color=self.accent
        )
        self.alg_dropdown.pack(fill="x", pady=4)

        self.alg_buttons["dfs"] = self.alg_dropdown.add_item("DFS", self.choose_dfs)
        self.alg_buttons["bfs"] = self.alg_dropdown.add_item("BFS", self.choose_bfs)
        self.alg_buttons["dijkstra"] = self.alg_dropdown.add_item("Dijkstra", self.choose_dijkstra)
        self.alg_buttons["prim"] = self.alg_dropdown.add_item("Prim MST", self.choose_prim)
        # Kruskal ไม่ต้องเลือกจุดเริ่ม ทำเป็นปุ่ม run ตรง ๆ
        self.alg_buttons["kruskal"] = self.alg_dropdown.add_item("Kruskal MST", self.run_kruskal)

        # Dropdown Tools
        self.tools_dropdown = FloatingDropdown(
            self.controls_container,
            title="Edit tools",
            accent_color="#b0b5ff"
        )
        self.tools_dropdown.pack(fill="x", pady=4)

        self.tool_buttons["build"] = self.tools_dropdown.add_item(
            "Draw / Add",
            lambda: self.set_mode("build")
        )
        self.tool_buttons["mouse"] = self.tools_dropdown.add_item(
            "Mouse / Pan",
            lambda: self.set_mode("mouse")
        )
        self.tool_buttons["select"] = self.tools_dropdown.add_item(
            "Select nodes",
            lambda: self.set_mode("select")
        )
        self.tool_buttons["move"] = self.tools_dropdown.add_item(
            "Move nodes",
            lambda: self.set_mode("move")
        )
        self.tool_buttons["del_node"] = self.tools_dropdown.add_item(
            "Delete node",
            lambda: self.set_mode("del_node")
        )
        self.tool_buttons["del_edge"] = self.tools_dropdown.add_item(
            "Delete edge",
            lambda: self.set_mode("del_edge")
        )

        # ปุ่ม action เพิ่มเติม
        self.tools_dropdown.add_item("Delete selected", self.delete_selected)
        self.tools_dropdown.add_item("Reset edge colors", self.reset_edge_colors)
        self.tools_dropdown.add_item("Clear graph", self.clear_graph)

        # Dropdown View
        self.view_dropdown = FloatingDropdown(
            self.controls_container,
            title="View",
            accent_color="#8de6ff"
        )
        self.view_dropdown.pack(fill="x", pady=4)

        self.view_dropdown.add_item("+  Zoom in", lambda: self.zoom(1.12))
        self.view_dropdown.add_item("−  Zoom out", lambda: self.zoom(1 / 1.12))

        # --- Floating Result Panel (ขวาล่าง) ---
        self.result_frame = tk.Frame(
            self.root,
            bg=self.glass_bg,
            highlightthickness=1,
            highlightbackground=self.glass_border,
            bd=0,
        )
        self.result_width = 360
        self.result_height = 240
        self.result_frame.place(
            relx=1.0, rely=1.0,
            anchor="se",
            width=self.result_width,
            height=self.result_height
        )

        # hover card effect
        self.result_frame.bind("<Enter>", self._on_result_hover)
        self.result_frame.bind("<Leave>", self._on_result_leave)

        title_bar = tk.Frame(self.result_frame, bg=self.glass_bg)
        title_bar.pack(fill="x", padx=10, pady=(8, 4))

        title_label = tk.Label(
            title_bar,
            text="Result / Steps",
            font=("Segoe UI", 10, "bold"),
            fg="#f5f5f5",
            bg=self.glass_bg
        )
        title_label.pack(side="left")

        self.result_status = tk.Label(
            title_bar,
            text="",
            font=("Segoe UI", 8),
            fg="#a0a4b8",
            bg=self.glass_bg
        )
        self.result_status.pack(side="right")

        self.info_text = tk.Text(
            self.result_frame,
            width=40,
            height=12,
            bg="#11131a",
            fg="#f5f5f5",
            relief=tk.FLAT,
            wrap=tk.WORD,
            insertbackground="#f5f5f5",
            font=("Segoe UI", 10)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # --- state ภายใน ---
        self.node_radius = 18
        self.node_positions = []       # index -> (x, y)
        self.node_items = {}           # index -> (circle_id, text_id)
        self.edge_items = {}           # (u, v) -> (line_id, text_id, w)

        self.line_to_edge = {}         # line_id -> (u, v) canonical (min,max)
        self.text_to_edge = {}         # weight_text_id -> (u, v) canonical

        self.graph = Graph(0)

        # mode: build, mouse, select, move, dfs, bfs, prim, dijkstra_src, dijkstra_dest, del_node, del_edge
        self.mode = "build"
        self.edge_start = None
        self.dijkstra_src = None

        self.dragging_node = None
        self.last_mouse_pos = None
        self.pan_last_pos = None

        self.selected_nodes = set()
        self.selection_rect = None
        self.sel_start = None

        # bind event canvas (mouse)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # mouse wheel zoom
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)         # Windows / macOS
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_linux_up)  # Linux
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_linux_down)

        # key bindings (Delete เพื่อลบ selection)
        self.root.bind("<Delete>", self.on_delete_key)
        self.root.bind("<BackSpace>", self.on_delete_key)

        # เริ่มต้นให้โหมด build ถูกเลือก
        self.set_mode("build")
        self.alg_dropdown.close()
        self.tools_dropdown.open()
        self.view_dropdown.close()

        # Hint เริ่มต้น
        self.log(
            "วิธีใช้โดยสรุป:\n"
            "• Draw / Add: คลิกพื้นที่ว่างเพื่อสร้าง node (A,B,C,...), คลิก node สองครั้งเพื่อลากเส้น\n"
            "• Mouse / Pan: คลิกเลือก node, ลากที่พื้นหลังเพื่อเลื่อนทั้งกราฟ (pan)\n"
            "• Select nodes: ลากกรอบคลุมหลาย node เพื่อเลือก\n"
            "• Move nodes: ลาก node (หรือชุดที่ select ไว้) เพื่อย้ายทั้งกลุ่ม\n"
            "• Algorithms: เลือก DFS / BFS / Dijkstra / Prim / Kruskal เพื่อลองรันพร้อมอนิเมชัน\n"
            "• View: ใช้ scroll เมาส์ หรือ + / − เพื่อ zoom in / out กราฟ\n"
            "• ปุ่ม Delete: ลบ node ที่ select ไว้ หรือเส้นที่ชี้อยู่ด้วยเมาส์\n"
        )

    # ---------- Result hover effect ----------

    def _on_result_hover(self, _e):
        # ขยายเล็กน้อยแบบ card ลอย
        self.result_frame.place_configure(
            width=self.result_width + 16,
            height=self.result_height + 12
        )
        self.result_frame.configure(highlightbackground=self.accent_soft)

    def _on_result_leave(self, _e):
        x, y = self.root.winfo_pointerxy()
        widget_under = self.root.winfo_containing(x, y)
        if widget_under is None or not str(widget_under).startswith(str(self.result_frame)):
            self.result_frame.place_configure(
                width=self.result_width,
                height=self.result_height
            )
            self.result_frame.configure(highlightbackground=self.glass_border)

    # ---------- utility log ----------

    def log(self, text, status=""):
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)
        self.result_status.configure(text=status)

    # ---------- mode helpers ----------

    def set_mode(self, mode):
        self.mode = mode
        # ไฮไลต์ปุ่มเครื่องมือ
        for name, btn in self.tool_buttons.items():
            btn.configure(bg="#20232d")
        if mode in self.tool_buttons:
            self.tool_buttons[mode].configure(bg="#34384a")

    def set_active_algorithm(self, key=None):
        for name, btn in self.alg_buttons.items():
            btn.configure(bg="#20232d")
        if key and key in self.alg_buttons:
            self.alg_buttons[key].configure(bg="#34384a")

    # ---------- node / edge helpers ----------

    def find_node_at(self, x, y):
        for i, (nx, ny) in enumerate(self.node_positions):
            dx = x - nx
            dy = y - ny
            if dx * dx + dy * dy <= self.node_radius * self.node_radius:
                return i
        return None

    def reset_node_colors(self):
        for idx, (circle_id, text_id) in self.node_items.items():
            self.canvas.itemconfig(circle_id, fill=self.default_node_color, outline=self.default_node_outline)

    def highlight_node(self, idx, color=None):
        if idx is None:
            return
        if color is None:
            color = self.selected_node_color
        circle_id, _ = self.node_items[idx]
        self.canvas.itemconfig(circle_id, fill=color)

    def reset_edge_colors(self):
        for (u, v), (line_id, text_id, w) in self.edge_items.items():
            self.canvas.itemconfig(line_id, fill=self.edge_color, width=2)

    def edge_coords(self, u, v):
        """คำนวณปลายเส้นไม่ให้ผ่านกลาง node (เชื่อมที่ขอบวงกลมแทน)"""
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy) or 1.0
        r = self.node_radius
        sx = x1 + dx * r / dist
        sy = y1 + dy * r / dist
        ex = x2 - dx * r / dist
        ey = y2 - dy * r / dist
        return sx, sy, ex, ey

    # ---------- animation helper ----------

    def animate_edges(self, edge_list, header_lines):
        """
        แสดงผลลัพธ์ + ทำอนิเมชันทีละเส้น ตามลำดับใน edge_list
        """
        if not edge_list:
            self.log("\n".join(header_lines) + "\n\n(ไม่มีเส้นในผลลัพธ์)")
            return

        step_lines = header_lines[:]
        for i, (u, v, w) in enumerate(edge_list, 1):
            step_lines.append(f"Step {i}: {format_vertex(u)} → {format_vertex(v)} (w={w})")

        self.log("\n".join(step_lines))
        self.reset_edge_colors()

        def pulse(line_id, k):
            if k <= 0:
                self.canvas.itemconfig(line_id, width=3)
                return
            width = 2 + (k % 2) * 2
            self.canvas.itemconfig(line_id, width=width)
            self.root.after(90, lambda: pulse(line_id, k - 1))

        def step(i):
            if i >= len(edge_list):
                return
            u, v, w = edge_list[i]
            item = self.edge_items.get((u, v)) or self.edge_items.get((v, u))
            if item:
                line_id, text_id, _ = item
                self.canvas.itemconfig(line_id, fill=self.edge_highlight_color)
                pulse(line_id, 4)
            self.root.after(self.anim_delay, lambda: step(i + 1))

        step(0)

    # ---------- canvas events ----------

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        idx = self.find_node_at(x, y)

        # mouse tool: select + pan + move
        if self.mode == "mouse":
            if idx is not None:
                # toggle selection
                if idx in self.selected_nodes:
                    self.selected_nodes.remove(idx)
                else:
                    self.selected_nodes.add(idx)
                self.reset_node_colors()
                for nid in self.selected_nodes:
                    self.highlight_node(nid, self.selected_node_color)
                # start dragging selection
                self.dragging_node = idx
                self.last_mouse_pos = (x, y)
                self.pan_last_pos = None
            else:
                # start panning
                self.pan_last_pos = (x, y)
                self.dragging_node = None
                self.last_mouse_pos = None
            return

        # select mode: เริ่มลากกรอบ
        if self.mode == "select":
            self.sel_start = (x, y)
            if self.selection_rect is not None:
                self.canvas.delete(self.selection_rect)
                self.selection_rect = None
            return

        if self.mode == "move":
            self.dragging_node = idx
            self.last_mouse_pos = (x, y)
            return

        if self.mode == "del_node":
            if idx is not None:
                self.delete_node(idx)
            return

        if self.mode == "del_edge":
            closest = self.canvas.find_closest(x, y)
            if closest:
                self.delete_edge_by_item(closest[0])
            return

        # โหมด build + algorithms
        if self.mode == "build":
            if idx is None:
                self.edge_start = None
                self.reset_node_colors()
                self.add_node(x, y)
            else:
                if self.edge_start is None:
                    self.edge_start = idx
                    self.reset_node_colors()
                    self.highlight_node(idx)
                else:
                    if self.edge_start != idx:
                        self.add_edge_with_weight(self.edge_start, idx)
                    self.edge_start = None
                    self.reset_node_colors()

        elif self.mode in ("dfs", "bfs", "prim"):
            if idx is not None:
                self.reset_node_colors()
                self.highlight_node(idx, self.source_node_color)
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
                    self.highlight_node(idx, self.source_node_color)
                    self.mode = "dijkstra_dest"
                    messagebox.showinfo("Dijkstra", "คลิกเลือกจุดปลาย (target)")
                else:
                    self.highlight_node(idx, self.target_node_color)
                    self.run_dijkstra(self.dijkstra_src, idx)
                    self.set_active_algorithm(None)
                    self.set_mode("build")
                    self.dijkstra_src = None

    def on_mouse_drag(self, event):
        x, y = event.x, event.y

        # mouse mode: pan or move selection
        if self.mode == "mouse":
            # pan ทั้งกราฟ
            if self.pan_last_pos is not None and self.dragging_node is None:
                dx = x - self.pan_last_pos[0]
                dy = y - self.pan_last_pos[1]
                self.pan_last_pos = (x, y)
                if dx != 0 or dy != 0:
                    for i, (nx, ny) in enumerate(self.node_positions):
                        self.node_positions[i] = (nx + dx, ny + dy)
                    self.redraw_all()
                return

            # move nodes (เหมือนโหมด move)
            if self.dragging_node is not None:
                if self.last_mouse_pos is None:
                    self.last_mouse_pos = (x, y)
                    return
                dx = x - self.last_mouse_pos[0]
                dy = y - self.last_mouse_pos[1]
                self.last_mouse_pos = (x, y)

                if self.selected_nodes and self.dragging_node in self.selected_nodes:
                    moving = self.selected_nodes
                else:
                    moving = {self.dragging_node}

                for idx in moving:
                    nx, ny = self.node_positions[idx]
                    nx += dx
                    ny += dy
                    self.node_positions[idx] = (nx, ny)
                    circle_id, text_id = self.node_items[idx]
                    r = self.node_radius
                    self.canvas.coords(circle_id, nx - r, ny - r, nx + r, ny + r)
                    self.canvas.coords(text_id, nx, ny)

                for (u, v), (line_id, weight_id, w) in self.edge_items.items():
                    if u in moving or v in moving:
                        sx, sy, ex, ey = self.edge_coords(u, v)
                        self.canvas.coords(line_id, sx, sy, ex, ey)
                        mx, my = (sx + ex) / 2, (sy + ey) / 2
                        self.canvas.coords(weight_id, mx, my - 10)
                return

        # select mode: วาดกรอบ
        if self.mode == "select":
            if self.sel_start is None:
                return
            x0, y0 = self.sel_start
            if self.selection_rect is None:
                self.selection_rect = self.canvas.create_rectangle(
                    x0, y0, x, y,
                    outline="#8f95ff",
                    dash=(4, 3)
                )
            else:
                self.canvas.coords(self.selection_rect, x0, y0, x, y)
            return

        # move mode
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

            if self.selected_nodes and self.dragging_node in self.selected_nodes:
                moving = self.selected_nodes
            else:
                moving = {self.dragging_node}

            for idx in moving:
                nx, ny = self.node_positions[idx]
                nx += dx
                ny += dy
                self.node_positions[idx] = (nx, ny)
                circle_id, text_id = self.node_items[idx]
                r = self.node_radius
                self.canvas.coords(circle_id, nx - r, ny - r, nx + r, ny + r)
                self.canvas.coords(text_id, nx, ny)

            for (u, v), (line_id, weight_id, w) in self.edge_items.items():
                if u in moving or v in moving:
                    sx, sy, ex, ey = self.edge_coords(u, v)
                    self.canvas.coords(line_id, sx, sy, ex, ey)
                    mx, my = (sx + ex) / 2, (sy + ey) / 2
                    self.canvas.coords(weight_id, mx, my - 10)

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
                self.highlight_node(idx, self.selected_node_color)
            return

        if self.mode == "move":
            self.dragging_node = None
            self.last_mouse_pos = None

    # ---------- node / edge creation ----------

    def add_node(self, x, y):
        idx = len(self.node_positions)
        self.node_positions.append((x, y))

        new_g = Graph(idx + 1)
        for u in range(self.graph.n):
            for v, w in self.graph.adj[u]:
                if u < new_g.n and v < new_g.n:
                    new_g.adj[u].append((v, w))
        for w, u, v in self.graph.edges:
            if u < new_g.n and v < new_g.n:
                new_g.edges.append((w, u, v))
        self.graph = new_g

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
            font=("Segoe UI", 11, "bold")
        )
        self.node_items[idx] = (circle_id, text_id)

    def add_edge_with_weight(self, u, v):
        if u == v:
            return
        w = simpledialog.askinteger("น้ำหนัก", "กรอกค่าน้ำหนักของเส้น:", minvalue=0)
        if w is None:
            return

        self.graph.add_edge(u, v, w)

        sx, sy, ex, ey = self.edge_coords(u, v)
        line_id = self.canvas.create_line(
            sx, sy, ex, ey,
            width=2,
            fill=self.edge_color
        )
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        weight_id = self.canvas.create_text(
            mx, my - 10,
            text=str(w),
            font=("Segoe UI", 9, "bold"),
            fill="#c2c6dd"
        )

        self.edge_items[(u, v)] = (line_id, weight_id, w)
        self.edge_items[(v, u)] = (line_id, weight_id, w)

        cu, cv = sorted((u, v))
        self.line_to_edge[line_id] = (cu, cv)
        self.text_to_edge[weight_id] = (cu, cv)

    # ---------- delete helpers ----------

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

        self.graph.adj[u] = [
            (to, ww) for (to, ww) in self.graph.adj[u]
            if not (to == v and ww == w)
        ]
        self.graph.adj[v] = [
            (to, ww) for (to, ww) in self.graph.adj[v]
            if not (to == u and ww == w)
        ]

        new_edges = []
        for ww, uu, vv in self.graph.edges:
            if (uu == u and vv == v and ww == w) or (uu == v and vv == u and ww == w):
                continue
            new_edges.append((ww, uu, vv))
        self.graph.edges = new_edges

        self.canvas.delete(line_id)
        self.canvas.delete(weight_id)

        for key in [(u, v), (v, u)]:
            if key in self.edge_items:
                del self.edge_items[key]

        if line_id in self.line_to_edge:
            del self.line_to_edge[line_id]
        if weight_id in self.text_to_edge:
            del self.text_to_edge[weight_id]

    def delete_node(self, del_idx):
        if del_idx < 0 or del_idx >= self.graph.n:
            return

        if del_idx in self.node_items:
            circle_id, text_id = self.node_items[del_idx]
            self.canvas.delete(circle_id)
            self.canvas.delete(text_id)

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

        old_n = self.graph.n
        idx_map = {}
        new_idx = 0
        for old_idx in range(old_n):
            if old_idx == del_idx:
                continue
            idx_map[old_idx] = new_idx
            new_idx += 1

        new_g = Graph(old_n - 1)
        for w, u, v in self.graph.edges:
            if u == del_idx or v == del_idx:
                continue
            nu = idx_map[u]
            nv = idx_map[v]
            if nu <= nv:
                new_g.add_edge(nu, nv, w)
        self.graph = new_g

        new_positions = []
        for old_idx, pos in enumerate(self.node_positions):
            if old_idx == del_idx:
                continue
            new_positions.append(pos)
        self.node_positions = new_positions

        new_selected = set()
        for old_idx, new_idx in idx_map.items():
            if old_idx in self.selected_nodes:
                new_selected.add(new_idx)
        self.selected_nodes = new_selected

        self.redraw_all()

    def delete_selected(self):
        if not self.selected_nodes:
            messagebox.showinfo("Delete selected", "ยังไม่ได้เลือก node ใด")
            return
        for idx in sorted(self.selected_nodes, reverse=True):
            self.delete_node(idx)
        self.selected_nodes = set()
        self.reset_node_colors()

    def redraw_all(self):
        self.canvas.delete("all")
        self.node_items.clear()
        self.edge_items.clear()
        self.line_to_edge.clear()
        self.text_to_edge.clear()

        for idx, (x, y) in enumerate(self.node_positions):
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
                font=("Segoe UI", 11, "bold")
            )
            self.node_items[idx] = (circle_id, text_id)

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
                fill=self.edge_color
            )
            mx, my = (sx + ex) / 2, (sy + ey) / 2
            weight_id = self.canvas.create_text(
                mx, my - 10,
                text=str(w),
                font=("Segoe UI", 9, "bold"),
                fill="#c2c6dd"
            )

            self.edge_items[(cu, cv)] = (line_id, weight_id, w)
            self.edge_items[(cv, cu)] = (line_id, weight_id, w)
            self.line_to_edge[line_id] = (cu, cv)
            self.text_to_edge[weight_id] = (cu, cv)

        for idx in self.selected_nodes:
            if idx in self.node_items:
                self.highlight_node(idx, self.selected_node_color)

    # ---------- clear graph ----------

    def clear_graph(self):
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
        self.log("กราฟถูกล้างแล้ว\nเริ่มสร้างจุดใหม่ได้เลยโดยคลิกบนพื้นที่ว่าง", status="Ready")

    # ---------- zoom ----------

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
        except Exception:
            cx, cy = 0, 0
        self.zoom_at(factor, cx, cy)

    # ---------- mouse wheel handlers ----------

    def on_mouse_wheel(self, event):
        # Windows / macOS: event.delta > 0 คือ scroll up
        if event.delta == 0:
            return
        base = 1.08 if event.delta > 0 else 1 / 1.08
        # ตรวจ ctrl (bit 0x4)
        if event.state & 0x4:
            base = base ** 1.5
        self.zoom_at(base, event.x, event.y)

    def on_mouse_wheel_linux_up(self, event):
        base = 1.08
        if event.state & 0x4:
            base = base ** 1.5
        self.zoom_at(base, event.x, event.y)

    def on_mouse_wheel_linux_down(self, event):
        base = 1 / 1.08
        if event.state & 0x4:
            base = base ** 1.5
        self.zoom_at(base, event.x, event.y)

    # ---------- key handlers ----------

    def on_delete_key(self, event=None):
        # ถ้ามี selection ของ node ให้ลบ node ก่อน
        if self.selected_nodes:
            self.delete_selected()
            return

        # ถ้าไม่มี selection ลองลบเส้นที่ชี้อยู่ด้วยเมาส์
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
        except Exception:
            pass

    # ---------- save / load ----------

    def save_graph(self):
        if not self.node_positions:
            messagebox.showinfo("Save graph", "ยังไม่มีกราฟให้บันทึก")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON graph", "*.json"), ("All files", "*.*")]
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
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.log(f"บันทึกกราฟลงไฟล์:\n{path}", status="Saved")

    def load_graph(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON graph", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Load graph", f"ไม่สามารถอ่านไฟล์ได้:\n{e}")
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
        self.log(f"โหลดกราฟจากไฟล์:\n{path}", status="Loaded")

    # ---------- algorithm mode buttons ----------

    def choose_dfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("DFS", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "dfs"
        self.reset_node_colors()
        self.set_active_algorithm("dfs")
        messagebox.showinfo("DFS", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_bfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("BFS", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "bfs"
        self.reset_node_colors()
        self.set_active_algorithm("bfs")
        messagebox.showinfo("BFS", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_prim(self):
        if self.graph.n == 0:
            messagebox.showwarning("Prim", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "prim"
        self.reset_node_colors()
        self.set_active_algorithm("prim")
        messagebox.showinfo("Prim", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_dijkstra(self):
        if self.graph.n == 0:
            messagebox.showwarning("Dijkstra", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "dijkstra_src"
        self.reset_node_colors()
        self.set_active_algorithm("dijkstra")
        messagebox.showinfo("Dijkstra", "คลิกเลือกจุดเริ่มต้น (source) บนกราฟ")

    # ---------- run algorithms + animation ----------

    def run_dfs(self, start):
        tree, un = dfs_spanning_tree(self.graph, start)
        header = ["DFS Tree:"]
        if tree:
            seq = [format_vertex(start)]
            for u, v, w in tree:
                seq.append(format_vertex(v))
            header.append("Order: " + " → ".join(seq))
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append("Unreachable: " + ", ".join(un_labels))
        self.animate_edges(tree, header)

    def run_bfs(self, start):
        tree, un = bfs_spanning_tree(self.graph, start)
        header = ["BFS Tree:"]
        if tree:
            seq = [format_vertex(start)]
            for u, v, w in tree:
                seq.append(format_vertex(v))
            header.append("Order: " + " → ".join(seq))
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append("Unreachable: " + ", ".join(un_labels))
        self.animate_edges(tree, header)

    def run_prim(self, start):
        mst, total = prim(self.graph, start)
        if mst is None:
            messagebox.showinfo("Prim", "กราฟไม่เชื่อมถึงกัน ไม่มี MST")
            self.log("Prim MST: No MST (graph not connected)", status="No MST")
            return
        header = [f"Prim MST (Total weight = {total}):"]
        if mst:
            edge_desc = " → ".join(f"{format_vertex(u)}-{format_vertex(v)}" for (u, v, w) in mst)
            header.append("Edges: " + edge_desc)
        self.animate_edges(mst, header)

    def run_kruskal(self):
        mst, total = kruskal(self.graph)
        if mst is None:
            messagebox.showinfo("Kruskal", "กราฟไม่เชื่อมถึงกัน ไม่มี MST")
            self.log("Kruskal MST: No MST (graph not connected)", status="No MST")
            return
        header = [f"Kruskal MST (Total weight = {total}):"]
        if mst:
            edge_desc = " → ".join(f"{format_vertex(u)}-{format_vertex(v)}" for (u, v, w) in mst)
            header.append("Edges: " + edge_desc)
        self.animate_edges(mst, header)

    def run_dijkstra(self, src, dest):
        dist, path = dijkstra(self.graph, src, dest)
        if dist == math.inf:
            messagebox.showinfo("Dijkstra", "ไม่มีเส้นทางจากจุดเริ่มถึงจุดปลาย")
            self.log("Dijkstra: No path.", status="No path")
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

        header = [
            "Dijkstra Shortest Path:",
            f"Distance = {dist}",
            "Path: " + " → ".join(format_vertex(v) for v in path),
            ""
        ]

        self.reset_node_colors()

        def color_nodes_step(i):
            if i >= len(path):
                return
            node = path[i]
            if i == 0:
                self.highlight_node(node, self.source_node_color)
            elif i == len(path) - 1:
                self.highlight_node(node, self.target_node_color)
            else:
                self.highlight_node(node, self.selected_node_color)
            self.root.after(self.anim_delay, lambda: color_nodes_step(i + 1))

        color_nodes_step(0)
        self.animate_edges(edges, header)


def main():
    root = tk.Tk()
    root.geometry("1200x700")
    app = GraphGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
