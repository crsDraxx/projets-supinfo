import tkinter as tk
from tkinter import filedialog, messagebox
from logic import determine_variables, determine_domains, get_neighbors, display_solution
from backtracking       import backtracking
from forwardChecking    import forward_checking
from forwardCheckingMin import forward_checking_min
import threading
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Palette ────────────────────────────────────────────────────────────────────
BG       = "#EAF4FB"
ACCENT   = "#2E86C1"
BTN_BLUE = "#85C1E9"
BTN_BLH  = "#5DADE2"
BTN_GRN  = "#A9DFBF"
BTN_GRH  = "#76C893"
DARK     = "#1A3A4A"
WHITE    = "#FFFFFF"
CELL_BLK = "#2E4053"
CELL_WHT = "#FFFFFF"
CELL_GRN = "#A9DFBF"
CANVAS_W = 500
CANVAS_H = 500


def _hover(b, n, h):
    b.bind("<Enter>", lambda e: b.config(bg=h))
    b.bind("<Leave>", lambda e: b.config(bg=n))


def _read_grid(path):
    grid = []
    with open(path, "r") as f:
        for line in f:
            row = []
            for c in line.rstrip("\n"):
                if c == "_":   row.append(0)
                elif c == "#": row.append(1)
            if row:
                grid.append(row)
    return grid


def _read_dict(path):
    with open(path, "r") as f:
        return [l.strip() for l in f if l.strip()]


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Solver")
        self.root.configure(bg=BG)

        self.grid_data  = None
        self.dict_words = None
        self.solution   = None

        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        self._build()

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _build(self):
        header = tk.Frame(self.root, bg=ACCENT, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Crossword Solver",
                 font=("Georgia", 14, "bold"), bg=ACCENT, fg=WHITE
                 ).pack(side="left", padx=16, pady=10)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=BG, padx=16, pady=14, width=230)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(body, bg=BG, padx=10, pady=14)
        right.pack(side="left", fill="both", expand=True)

        self._build_controls(left)
        self._build_canvas(right)

    def _build_controls(self, p):
        # ── Jeu de données ────────────────────────────────────────────────────
        self._section(p, "Jeu de donnees")

        self.dataset_var = tk.StringVar(value="Aucun jeu charge")
        tk.Label(p, textvariable=self.dataset_var, font=("Helvetica", 8, "italic"),
                 bg=BG, fg=DARK, wraplength=200).pack(anchor="w", pady=(0, 6))

        self.preset_btns = []
        for txt, key in [("MP1", "1"),
                         ("MP2", "2")]:
            b = tk.Button(p, text=txt, font=("Helvetica", 9, "bold"),
                          bg=BTN_BLUE, fg=DARK, activebackground=BTN_BLH,
                          relief="flat", bd=0, cursor="hand2", padx=6, pady=8,
                          command=lambda k=key: self._load_preset(k))
            b.pack(fill="x", pady=3)
            _hover(b, BTN_BLUE, BTN_BLH)
            self.preset_btns.append(b)

        tk.Frame(p, bg=ACCENT, height=1).pack(fill="x", pady=8)

        # ── Algorithme ────────────────────────────────────────────────────────
        self._section(p, "Algorithme")

        self.algo_btns = []
        for val, txt in [(1, "Backtracking"),
                         (2, "Forward Checking"),
                         (3, "Forward Checking MRV"),
                         (4, "Les trois")]:
            b = tk.Button(p, text=txt, font=("Helvetica", 9, "bold"),
                          bg=BTN_GRN, fg=DARK, activebackground=BTN_GRH,
                          relief="flat", bd=0, cursor="hand2", padx=6, pady=7,
                          command=lambda v=val: self._run(v))
            b.pack(fill="x", pady=3)
            _hover(b, BTN_GRN, BTN_GRH)
            self.algo_btns.append(b)

        # ── Bouton Reset ──────────────────────────────────────────────────────
        reset_btn = tk.Button(p, text="\U0001f504  Reinitialiser la grille",
                              font=("Helvetica", 9, "bold"),
                              bg="#D5D8DC", fg=DARK, activebackground="#BFC9CA",
                              relief="flat", bd=0, cursor="hand2", padx=6, pady=7,
                              command=self._reset)
        reset_btn.pack(fill="x", pady=(6, 3))
        _hover(reset_btn, "#D5D8DC", "#BFC9CA")

        self.status = tk.StringVar(value="Choisissez un jeu de donnees.")
        tk.Label(p, textvariable=self.status, font=("Helvetica", 8, "italic"),
                 bg=BG, fg=ACCENT, wraplength=200, justify="center"
                 ).pack(pady=(10, 0))

    def _build_canvas(self, p):
        # ── Vue simple (1 grille) ────────────────────────────────────────────
        self.single_frame = tk.Frame(p, bg=BG)
        self.single_frame.pack(fill="both", expand=True)

        tk.Label(self.single_frame, text="Grille", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w")
        self.canvas = tk.Canvas(self.single_frame, width=CANVAS_W, height=CANVAS_H,
                                bg="#D6EAF8", highlightthickness=1,
                                highlightbackground=ACCENT)
        self.canvas.pack(pady=(4, 0))

        # ── Vue triple (3 grilles côte à côte) ──────────────────────────────
        self.triple_frame = tk.Frame(p, bg=BG)
        # (caché par défaut, affiché seulement pour "Les trois")

        self.triple_canvases   = []   # liste des 3 Canvas
        self.triple_title_lbls = []   # liste des 3 Labels de titre

        SMALL_W = 300
        SMALL_H = 300
        self._triple_canvas_size = (SMALL_W, SMALL_H)

        algo_names = ["Backtracking", "Forward Checking", "Forward Checking MRV"]
        self.triple_status_lbls = []
        for name in algo_names:
            col = tk.Frame(self.triple_frame, bg=BG, padx=6)
            col.pack(side="left", fill="both", expand=True)

            lbl = tk.Label(col, text=name, font=("Helvetica", 9, "bold"),
                           bg=BG, fg=ACCENT)
            lbl.pack(anchor="center")
            self.triple_title_lbls.append(lbl)

            c = tk.Canvas(col, width=SMALL_W, height=SMALL_H,
                          bg="#D6EAF8", highlightthickness=1,
                          highlightbackground=ACCENT)
            c.pack(pady=(2, 0))
            self.triple_canvases.append(c)

            slbl = tk.Label(col, text="", font=("Helvetica", 8, "bold"),
                            bg=BG, fg=ACCENT)
            slbl.pack(pady=(4, 0))
            self.triple_status_lbls.append(slbl)

    def _section(self, p, t):
        tk.Label(p, text=t, font=("Helvetica", 10, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w", pady=(0, 4))

    def _short(self, path):
        """Affiche un chemin court."""
        parts = path.replace("\\", "/").split("/")
        return "/".join(parts[-3:]) if len(parts) > 3 else path


    # ── Chargement preset ──────────────────────────────────────────────────────

    def _load_preset(self, key):
        names = {"1": ("gridMP1.txt", "dictMP1.txt"),
                 "2": ("gridMP2.txt", "dictMP2.txt")}
        gname, dname = names[key]
        label = "MP1" if key == "1" else "MP2"

        grid_path = os.path.join(self.data_dir, gname)
        dict_path = os.path.join(self.data_dir, dname)


        try:
            self.grid_data  = _read_grid(grid_path)
            self.dict_words = _read_dict(dict_path)
            self.solution   = None
            n, m = len(self.grid_data), len(self.grid_data[0])
            self.dataset_var.set(f"grid{label} + dict{label}")
            self.status.set(f"{label} : grille {n}x{m} | {len(self.dict_words)} mots")
            self._draw()
        except Exception as e:
            messagebox.showerror("Erreur de lecture", str(e))

    # ── Résolution ─────────────────────────────────────────────────────────────

    def _run(self, algo):
        if self.grid_data is None or self.dict_words is None:
            messagebox.showwarning("Manquant", "Choisissez d'abord MP1 ou MP2.")
            return
        for b in self.algo_btns:
            b.config(state="disabled")
        self.status.set("Resolution en cours...")
        threading.Thread(target=self._solve, args=(algo,), daemon=True).start()

    def _reset(self):
        """Efface la solution et réaffiche la grille vide."""
        self.solution = None
        self._show_single()
        self._draw_on_canvas(self.canvas, CANVAS_W, CANVAS_H, solution=None)
        self.status.set("Grille reinitialise.")

    def _solve(self, algo):
        try:
            variables = determine_variables(self.grid_data)
            domains   = determine_domains(variables, self.dict_words)
            neighbors = get_neighbors(variables)

            runs = {
                1: [("Backtracking",         backtracking)],
                2: [("Forward Checking",     forward_checking)],
                3: [("Forward Checking MRV", forward_checking_min)],
                4: [("Backtracking",         backtracking),
                    ("Forward Checking",     forward_checking),
                    ("Forward Checking MRV", forward_checking_min)],
            }[algo]

            last_sol = None
            lines    = []
            solutions = []   # pour stocker les 3 solutions (mode "Les trois")

            for name, fn in runs:
                t0  = time.time()
                sol = fn(variables, domains.copy(), neighbors)
                t   = time.time() - t0
                if sol:
                    lines.append(f"✓ {name} : {t:.4f}s")
                    last_sol = sol
                    display_solution(self.grid_data, sol)
                else:
                    lines.append(f"✗ {name} : aucune solution ({t:.4f}s)")
                solutions.append(sol)   # None si pas de solution

            self.solution = last_sol
            msg = "\n".join(lines)
            self.root.after(0, lambda: self.status.set(msg))

            if algo == 4:
                # Afficher les 3 grilles côte à côte
                sols_copy = list(solutions)
                self.root.after(0, lambda: self._show_triple(sols_copy))
            elif last_sol:
                self.root.after(0, self._show_single)
                self.root.after(0, self._draw_solution)

        except Exception as e:
            self.root.after(0, lambda: self.status.set(f"Erreur : {e}"))
        finally:
            self.root.after(0, lambda: [b.config(state="normal") for b in self.algo_btns])

    # ── Basculement vue simple / triple ────────────────────────────────────────

    def _show_single(self):
        """Affiche seulement la vue 1 grille."""
        self.triple_frame.pack_forget()
        self.single_frame.pack(fill="both", expand=True)

    def _show_triple(self, solutions):
        """Bascule vers la vue 3 grilles et les dessine."""
        self.single_frame.pack_forget()
        self.triple_frame.pack(fill="both", expand=True)

        sw, sh = self._triple_canvas_size
        for i, (canvas, sol, slbl) in enumerate(
                zip(self.triple_canvases, solutions, self.triple_status_lbls)):
            self._draw_on_canvas(canvas, sw, sh, sol)
            if sol:
                slbl.config(text="✓ Complété", fg="#1E8449")
            else:
                slbl.config(text="✗ Aucune solution", fg="#C0392B")

    # ── Dessin ─────────────────────────────────────────────────────────────────

    def _cell_size(self):
        n, m = len(self.grid_data), len(self.grid_data[0])
        return min(CANVAS_W // m, CANVAS_H // n)

    def _draw_on_canvas(self, canvas, cw, ch, solution=None):
        """Dessine la grille (et optionnellement une solution) sur n'importe quel canvas."""
        canvas.delete("all")
        if not self.grid_data:
            return
        n, m = len(self.grid_data), len(self.grid_data[0])
        s = min(cw // m, ch // n)
        off_x = (cw - m * s) // 2
        off_y = (ch - n * s) // 2

        # Dessin grille de base
        for i in range(n):
            for j in range(m):
                x0, y0 = off_x + j * s, off_y + i * s
                x1, y1 = x0 + s, y0 + s
                color = CELL_BLK if self.grid_data[i][j] == 1 else CELL_WHT
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#AAB7B8")

        if not solution:
            return

        # Dessin solution
        from logic import get_word_cells
        for var in solution:
            for (r, c) in get_word_cells(var):
                canvas.create_rectangle(
                    off_x + c*s, off_y + r*s,
                    off_x + (c+1)*s, off_y + (r+1)*s,
                    fill=CELL_GRN, outline="#AAB7B8")
        for var, word in solution.items():
            for k, (r, c) in enumerate(get_word_cells(var)):
                canvas.create_text(
                    off_x + c*s + s//2, off_y + r*s + s//2,
                    text=word[k].upper(),
                    font=("Arial", max(s//2, 7), "bold"),
                    fill=DARK)

    def _draw(self):
        self._show_single()
        self._draw_on_canvas(self.canvas, CANVAS_W, CANVAS_H, solution=None)

    def _draw_solution(self):
        self._show_single()
        self._draw_on_canvas(self.canvas, CANVAS_W, CANVAS_H, solution=self.solution)


if __name__ == "__main__":
    root = tk.Tk()
    GUI(root)
    root.mainloop()
