from heapq import heappush, heappop
from collections import deque
import math
import tkinter as tk
from tkinter import simpledialog, messagebox

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

    unreach = [i for i in range(g.n) if not visited[i]]
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


# ---------- GUI ----------
class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Algorithms Visualizer")

        # --- Theme (Dark) ---
        self.bg_main = "#101010"
        self.bg_panel = "#181818"
        self.bg_canvas = "#050505"
        self.bg_button = "#262626"
        self.bg_button_active = "#404040"
        self.fg_text = "#f5f5f5"
        self.fg_subtle = "#bbbbbb"

        # สี node / edge
        self.default_node_color = "#3498db"
        self.default_node_outline = "#ecf0f1"
        self.node_text_color = "white"
        self.selected_node_color = "#f1c40f"
        self.source_node_color = "#2ecc71"
        self.target_node_color = "#e67e22"

        self.edge_color = "#555555"
        self.edge_highlight_color = "#e74c3c"

        self.anim_delay = 450  # ms ระหว่างแต่ละ step

        self.root.configure(bg=self.bg_main)

        # พื้นที่วาดกราฟ
        self.canvas = tk.Canvas(
            root,
            width=800,
            height=600,
            bg=self.bg_canvas,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # แถบด้านขวา
        right_frame = tk.Frame(root, bg=self.bg_panel)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        title_label = tk.Label(
            right_frame,
            text="Graph Controls",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_panel,
            fg=self.fg_text
        )
        title_label.pack(fill=tk.X, pady=(8, 4))

        btn_frame = tk.Frame(right_frame, bg=self.bg_panel)
        btn_frame.pack(fill=tk.X, pady=4)

        def make_btn(parent, text, cmd):
            return tk.Button(
                parent,
                text=text,
                command=cmd,
                bg=self.bg_button,
                fg=self.fg_text,
                activebackground=self.bg_button_active,
                activeforeground=self.fg_text,
                relief=tk.FLAT,
                font=("Segoe UI", 10)
            )

        # ปุ่มอัลกอริทึม
        make_btn(btn_frame, "DFS", self.choose_dfs).pack(fill=tk.X, pady=1)
        make_btn(btn_frame, "BFS", self.choose_bfs).pack(fill=tk.X, pady=1)
        make_btn(btn_frame, "Dijkstra", self.choose_dijkstra).pack(fill=tk.X, pady=1)
        make_btn(btn_frame, "Prim MST", self.choose_prim).pack(fill=tk.X, pady=1)
        make_btn(btn_frame, "Kruskal MST", self.run_kruskal).pack(fill=tk.X, pady=1)

        tk.Label(
            right_frame,
            text="Edit graph",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_panel,
            fg=self.fg_text
        ).pack(fill=tk.X, pady=(10, 4))

        edit_frame = tk.Frame(right_frame, bg=self.bg_panel)
        edit_frame.pack(fill=tk.X, pady=4)

        make_btn(edit_frame, "Move nodes", self.toggle_move_mode).pack(fill=tk.X, pady=1)
        make_btn(edit_frame, "Delete node", self.choose_delete_node).pack(fill=tk.X, pady=1)
        make_btn(edit_frame, "Delete edge", self.choose_delete_edge).pack(fill=tk.X, pady=1)
        make_btn(edit_frame, "Reset edge colors", self.reset_edge_colors).pack(fill=tk.X, pady=1)
        make_btn(edit_frame, "Clear graph", self.clear_graph).pack(fill=tk.X, pady=(6, 2))

        tk.Label(
            right_frame,
            text="Result / Steps",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_panel,
            fg=self.fg_text
        ).pack(fill=tk.X, pady=(10, 4))

        self.info_text = tk.Text(
            right_frame,
            width=40,
            height=25,
            bg="#111111",
            fg=self.fg_text,
            relief=tk.FLAT,
            wrap=tk.WORD,
            insertbackground=self.fg_text
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 6))

        # state ภายใน
        self.node_radius = 18
        self.node_positions = []       # index -> (x, y)
        self.node_items = {}           # index -> (circle_id, text_id)
        self.edge_items = {}           # (u, v) -> (line_id, text_id, w)

        self.line_to_edge = {}         # line_id -> (u, v) canonical (min,max)
        self.text_to_edge = {}         # weight_text_id -> (u, v) canonical

        self.graph = Graph(0)

        self.mode = "build"  # build, move, dfs, bfs, prim, dijkstra_src, dijkstra_dest, del_node, del_edge
        self.edge_start = None
        self.dijkstra_src = None

        self.dragging_node = None

        # bind event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # แสดง hint เบื้องต้น
        self.log(
            "วิธีใช้เบื้องต้น:\n"
            "• คลิกที่พื้นที่ว่างเพื่อสร้างจุด (A,B,C,...)\n"
            "• คลิกจุดหนึ่ง แล้วคลิกอีกจุดเพื่อสร้างเส้น จะมี popup ให้ใส่น้ำหนัก\n"
            "• ใช้ปุ่ม DFS / BFS / Dijkstra / Prim / Kruskal เพื่อดูผลพร้อมอนิเมชัน\n"
            "• Move nodes: ลากจุดเพื่อย้ายตำแหน่ง เส้นและน้ำหนักจะขยับตาม\n"
            "• Delete node / Delete edge เพื่อลบ\n"
            "• Clear graph เพื่อล้างและเริ่มใหม่\n"
        )

    # -------- utility log ----------
    def log(self, text):
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)

    # -------- node / edge helpers ----------
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

    # -------- animation helper ----------
    def animate_edges(self, edge_list, header_lines):
        """
        แสดงผลลัพธ์ + ทำอนิเมชันทีละเส้น ตามลำดับใน edge_list
        edge_list: [(u,v,w), ...]
        header_lines: list[str] ข้อความด้านบนในช่อง Result
        """
        if not edge_list:
            self.log("\n".join(header_lines) + "\n\n(ไม่มีเส้นในผลลัพธ์)")
            return

        # เตรียมข้อความ step ทั้งหมด
        step_lines = header_lines[:]
        for i, (u, v, w) in enumerate(edge_list, 1):
            step_lines.append(f"Step {i}: {format_vertex(u)} - {format_vertex(v)} (w={w})")

        self.log("\n".join(step_lines))
        self.reset_edge_colors()

        def step(i):
            if i >= len(edge_list):
                return
            u, v, w = edge_list[i]
            item = self.edge_items.get((u, v)) or self.edge_items.get((v, u))
            if item:
                line_id, text_id, _ = item
                # เน้นเส้นปัจจุบัน
                self.canvas.itemconfig(line_id, fill=self.edge_highlight_color, width=3)
            self.root.after(self.anim_delay, lambda: step(i + 1))

        step(0)

    # -------- canvas events ----------
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        idx = self.find_node_at(x, y)

        if self.mode == "move":
            # โหมด move ใช้ drag อย่างเดียว ไม่ทำ action อื่นตอนคลิก
            return

        if self.mode == "del_node":
            if idx is not None:
                self.delete_node(idx)
            self.mode = "build"
            return

        if self.mode == "del_edge":
            # คลิกใกล้เส้น หรือตัวเลขน้ำหนัก
            closest = self.canvas.find_closest(x, y)
            if closest:
                item_id = closest[0]
                self.delete_edge_by_item(item_id)
            self.mode = "build"
            return

        # โหมดปกติ / อัลกอริทึม
        if self.mode == "build":
            # สร้างจุดหรือเส้น
            if idx is None:
                # คลิกที่ว่าง -> สร้างจุดใหม่
                self.edge_start = None
                self.reset_node_colors()
                self.add_node(x, y)
            else:
                # คลิกบนจุด -> ใช้สร้างเส้น (คลิกต้น-ปลาย)
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
                self.mode = "build"

        elif self.mode in ("dijkstra_src", "dijkstra_dest"):
            if idx is not None:
                if self.mode == "dijkstra_src":
                    self.reset_node_colors()
                    self.dijkstra_src = idx
                    self.highlight_node(idx, self.source_node_color)
                    self.mode = "dijkstra_dest"
                    messagebox.showinfo("Dijkstra", "เลือกจุดปลาย (target) ด้วยการคลิก")
                else:
                    self.highlight_node(idx, self.target_node_color)
                    self.run_dijkstra(self.dijkstra_src, idx)
                    self.mode = "build"
                    self.dijkstra_src = None

    def on_mouse_drag(self, event):
        if self.mode != "move":
            return
        x, y = event.x, event.y
        if self.dragging_node is None:
            idx = self.find_node_at(x, y)
            if idx is None:
                return
            self.dragging_node = idx

        idx = self.dragging_node
        self.node_positions[idx] = (x, y)
        circle_id, text_id = self.node_items[idx]

        r = self.node_radius
        self.canvas.coords(circle_id, x - r, y - r, x + r, y + r)
        self.canvas.coords(text_id, x, y)

        # อัปเดตเส้นและน้ำหนักที่ติดกับ node นี้
        for (u, v), (line_id, weight_id, w) in self.edge_items.items():
            if u == idx or v == idx:
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]
                self.canvas.coords(line_id, x1, y1, x2, y2)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.coords(weight_id, mx, my - 10)

    def on_mouse_release(self, event):
        self.dragging_node = None

    # -------- node / edge creation ----------
    def add_node(self, x, y):
        idx = len(self.node_positions)
        self.node_positions.append((x, y))

        # ขยายกราฟให้รองรับจุดใหม่ (ไม่แตะ logic อัลกอริทึม)
        new_g = Graph(idx + 1)
        # copy adj เดิม
        for u in range(self.graph.n):
            for v, w in self.graph.adj[u]:
                if u < new_g.n and v < new_g.n:
                    new_g.adj[u].append((v, w))
        # copy edges เดิม
        for w, u, v in self.graph.edges:
            if u < new_g.n and v < new_g.n:
                new_g.edges.append((w, u, v))
        self.graph = new_g

        cx, cy = x, y
        circle_id = self.canvas.create_oval(
            cx - self.node_radius, cy - self.node_radius,
            cx + self.node_radius, cy + self.node_radius,
            fill=self.default_node_color,
            outline=self.default_node_outline,
            width=2
        )
        label = format_vertex(idx)
        text_id = self.canvas.create_text(
            cx, cy,
            text=label,
            fill=self.node_text_color,
            font=("Segoe UI", 10, "bold")
        )
        self.node_items[idx] = (circle_id, text_id)

    def add_edge_with_weight(self, u, v):
        if u == v:
            return
        w = simpledialog.askinteger("น้ำหนัก", "กรอกค่าน้ำหนักของเส้น:", minvalue=0)
        if w is None:
            return

        self.graph.add_edge(u, v, w)

        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]

        line_id = self.canvas.create_line(
            x1, y1, x2, y2,
            width=2,
            fill=self.edge_color
        )
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # ให้เลขทับเส้น (ยกขึ้นมานิดนึง)
        weight_id = self.canvas.create_text(
            mx, my - 10,
            text=str(w),
            font=("Segoe UI", 9),
            fill=self.fg_subtle
        )

        # เก็บทั้ง (u,v) และ (v,u) สำหรับ lookup ช่วงไฮไลต์
        self.edge_items[(u, v)] = (line_id, weight_id, w)
        self.edge_items[(v, u)] = (line_id, weight_id, w)

        # canonical key สำหรับลบ (ไม่ให้ซ้ำ)
        cu, cv = sorted((u, v))
        self.line_to_edge[line_id] = (cu, cv)
        self.text_to_edge[weight_id] = (cu, cv)

    # -------- delete helpers ----------
    def delete_edge_by_item(self, item_id):
        # ลบจาก line หรือ text ก็ได้
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
        # หาน้ำหนักจาก edge_items
        item = self.edge_items.get((u, v)) or self.edge_items.get((v, u))
        if not item:
            return
        line_id, weight_id, w = item

        # ลบจาก Graph.adj
        self.graph.adj[u] = [
            (to, ww) for (to, ww) in self.graph.adj[u]
            if not (to == v and ww == w)
        ]
        self.graph.adj[v] = [
            (to, ww) for (to, ww) in self.graph.adj[v]
            if not (to == u and ww == w)
        ]

        # ลบจาก Graph.edges (2 ทิศ)
        new_edges = []
        for ww, uu, vv in self.graph.edges:
            if (uu == u and vv == v and ww == w) or (uu == v and vv == u and ww == w):
                continue
            new_edges.append((ww, uu, vv))
        self.graph.edges = new_edges

        # ลบจาก canvas
        self.canvas.delete(line_id)
        self.canvas.delete(weight_id)

        # ลบจาก dict
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

        # ลบ node บน canvas ทั้งจุดและข้อความ
        if del_idx in self.node_items:
            circle_id, text_id = self.node_items[del_idx]
            self.canvas.delete(circle_id)
            self.canvas.delete(text_id)

        # ลบเส้นทั้งหมดที่ติด node นี้ (จาก canvas)
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

        # สร้าง mapping old_index -> new_index
        old_n = self.graph.n
        idx_map = {}
        new_idx = 0
        for old_idx in range(old_n):
            if old_idx == del_idx:
                continue
            idx_map[old_idx] = new_idx
            new_idx += 1

        # สร้าง Graph ใหม่
        new_g = Graph(old_n - 1)
        for w, u, v in self.graph.edges:
            if u == del_idx or v == del_idx:
                continue
            nu = idx_map[u]
            nv = idx_map[v]
            if nu <= nv:   # ใส่ครั้งเดียวพอ เดี๋ยว add_edge ใส่ให้ครบสองทิศ
                new_g.add_edge(nu, nv, w)
        self.graph = new_g

        # อัปเดต node_positions (ลบตำแหน่งของ node ที่ถูกลบ)
        new_positions = []
        for old_idx, pos in enumerate(self.node_positions):
            if old_idx == del_idx:
                continue
            new_positions.append(pos)
        self.node_positions = new_positions

        # ล้างข้อมูล node/edge visuals แล้ววาดใหม่ตาม Graph/positions ปัจจุบัน
        self.redraw_all()

    def redraw_all(self):
        self.canvas.delete("all")
        self.node_items.clear()
        self.edge_items.clear()
        self.line_to_edge.clear()
        self.text_to_edge.clear()

        # วาด node ใหม่
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
                font=("Segoe UI", 10, "bold")
            )
            self.node_items[idx] = (circle_id, text_id)

        # วาด edge ใหม่จาก Graph.edges (ใช้เฉพาะคู่ u<v เพื่อไม่ซ้ำ)
        drawn = set()
        for w, u, v in self.graph.edges:
            cu, cv = sorted((u, v))
            if (cu, cv) in drawn:
                continue
            drawn.add((cu, cv))
            x1, y1 = self.node_positions[cu]
            x2, y2 = self.node_positions[cv]
            line_id = self.canvas.create_line(
                x1, y1, x2, y2,
                width=2,
                fill=self.edge_color
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            weight_id = self.canvas.create_text(
                mx, my - 10,
                text=str(w),
                font=("Segoe UI", 9),
                fill=self.fg_subtle
            )

            self.edge_items[(cu, cv)] = (line_id, weight_id, w)
            self.edge_items[(cv, cu)] = (line_id, weight_id, w)
            self.line_to_edge[line_id] = (cu, cv)
            self.text_to_edge[weight_id] = (cu, cv)

    # -------- clear graph ----------
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
        self.log("กราฟถูกล้างแล้ว\nเริ่มสร้างจุดใหม่ได้เลยโดยคลิกบนพื้นที่ว่าง")

    # -------- mode buttons ----------
    def choose_dfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("DFS", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "dfs"
        self.reset_node_colors()
        messagebox.showinfo("DFS", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_bfs(self):
        if self.graph.n == 0:
            messagebox.showwarning("BFS", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "bfs"
        self.reset_node_colors()
        messagebox.showinfo("BFS", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_prim(self):
        if self.graph.n == 0:
            messagebox.showwarning("Prim", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "prim"
        self.reset_node_colors()
        messagebox.showinfo("Prim", "คลิกเลือกจุดเริ่มต้นบนกราฟ")

    def choose_dijkstra(self):
        if self.graph.n == 0:
            messagebox.showwarning("Dijkstra", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "dijkstra_src"
        self.reset_node_colors()
        messagebox.showinfo("Dijkstra", "คลิกเลือกจุดเริ่มต้น (source) บนกราฟ")

    def toggle_move_mode(self):
        if self.mode != "move":
            self.mode = "move"
            self.reset_node_colors()
            self.edge_start = None
            messagebox.showinfo("Move nodes", "โหมด Move: ลากจุดบนกราฟเพื่อย้ายตำแหน่ง")
        else:
            self.mode = "build"

    def choose_delete_node(self):
        if self.graph.n == 0:
            messagebox.showwarning("Delete node", "ยังไม่มีจุดในกราฟ")
            return
        self.mode = "del_node"
        self.reset_node_colors()
        messagebox.showinfo("Delete node", "คลิกจุดที่ต้องการลบ")

    def choose_delete_edge(self):
        if not self.edge_items:
            messagebox.showwarning("Delete edge", "ยังไม่มีเส้นในกราฟ")
            return
        self.mode = "del_edge"
        messagebox.showinfo("Delete edge", "คลิกใกล้เส้นหรือเลขน้ำหนักที่ต้องการลบ")

    # -------- run algorithms + animation ----------
    def run_dfs(self, start):
        tree, un = dfs_spanning_tree(self.graph, start)
        header = ["DFS Tree:"]
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append("Unreachable: " + ", ".join(un_labels))
        self.animate_edges(tree, header)

    def run_bfs(self, start):
        tree, un = bfs_spanning_tree(self.graph, start)
        header = ["BFS Tree:"]
        if un:
            un_labels = [format_vertex(i) for i in un]
            header.append("Unreachable: " + ", ".join(un_labels))
        self.animate_edges(tree, header)

    def run_prim(self, start):
        mst, total = prim(self.graph, start)
        if mst is None:
            messagebox.showinfo("Prim", "กราฟไม่เชื่อมถึงกัน ไม่มี MST")
            self.log("Prim MST: No MST (graph not connected)")
            return
        header = [f"Prim MST (Total weight = {total}):"]
        self.animate_edges(mst, header)

    def run_kruskal(self):
        mst, total = kruskal(self.graph)
        if mst is None:
            messagebox.showinfo("Kruskal", "กราฟไม่เชื่อมถึงกัน ไม่มี MST")
            self.log("Kruskal MST: No MST (graph not connected)")
            return
        header = [f"Kruskal MST (Total weight = {total}):"]
        self.animate_edges(mst, header)

    def run_dijkstra(self, src, dest):
        dist, path = dijkstra(self.graph, src, dest)
        if dist == math.inf:
            messagebox.showinfo("Dijkstra", "ไม่มีเส้นทางจากจุดเริ่มถึงจุดปลาย")
            self.log("Dijkstra: No path.")
            return

        # สร้าง list ของเส้นบน path
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

        # เตรียมข้อความ
        header = [
            "Dijkstra Shortest Path:",
            f"Distance = {dist}",
            "Path: " + " -> ".join(format_vertex(v) for v in path),
            ""
        ]

        # รีเซ็ต node แล้วไล่สีตาม path ในระหว่างอนิเมชัน
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
    app = GraphGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    
