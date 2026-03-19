import tkinter as tk
from tkinter import ttk, font
import math

BG        = "#0d0d0d"
CARD      = "#161616"
BORDER    = "#2a2a2a"
ACCENT    = "#00ff88"
ACCENT2   = "#00ccff"
TEXT      = "#f0f0f0"
MUTED     = "#666666"
RED       = "#ff4757"
ORANGE    = "#ffa502"
GREEN     = "#00ff88"
BLUE      = "#00ccff"

CATS = [
    ("Dénutrition",  0,   16,   "#ff6b9d"),
    ("Maigreur",    16,  18.5,  "#ffa502"),
    ("Normal",      18.5,25,    "#00ff88"),
    ("Surpoids",    25,  30,    "#ffa502"),
    ("Obésité I",   30,  35,    "#ff6348"),
    ("Obésité II",  35,  40,    "#ff4757"),
    ("Obésité III", 40,  999,   "#c0392b"),
]

def get_category(imc):
    for name, lo, hi, color in CATS:
        if lo <= imc < hi:
            return name, color
    return "Obésité III", "#c0392b"

class IMCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculateur IMC — Statistiques Personnelles")
        self.geometry("520x720")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.f_title  = font.Font(family="Courier New", size=20, weight="bold")
        self.f_label  = font.Font(family="Courier New", size=10)
        self.f_input  = font.Font(family="Courier New", size=13)
        self.f_imc    = font.Font(family="Courier New", size=48, weight="bold")
        self.f_cat    = font.Font(family="Courier New", size=16, weight="bold")
        self.f_small  = font.Font(family="Courier New", size=9)
        self.f_btn    = font.Font(family="Courier New", size=12, weight="bold")

        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=30, pady=(28, 0))

        tk.Label(hdr, text="[ IMC ]", font=self.f_title,
                 fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text="STATS PERSONNELLES", font=self.f_label,
                 fg=MUTED, bg=BG).pack(side="left", padx=(12, 0), pady=(6, 0))

        self._sep()

        card = tk.Frame(self, bg=CARD, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="x", padx=30, pady=10)

        self.age_var    = tk.StringVar()
        self.taille_var = tk.StringVar()
        self.poids_var  = tk.StringVar()
        self.sexe_var   = tk.StringVar(value="H")

        self._field(card, "ÂGE",          "ans",  self.age_var,    0)
        self._field(card, "TAILLE",        "cm",   self.taille_var, 1)
        self._field(card, "POIDS",         "kg",   self.poids_var,  2)
        self._sexe_field(card, 3)

        self._sep()

        btn = tk.Button(self, text="▶  CALCULER L'IMC",
                        font=self.f_btn, fg=BG, bg=ACCENT,
                        activebackground="#00cc66", activeforeground=BG,
                        bd=0, pady=12, cursor="hand2",
                        command=self._calculate)
        btn.pack(fill="x", padx=30, pady=4)

        btn_reset = tk.Button(self, text="↺  RESET",
                        font=self.f_small, fg=MUTED, bg=CARD,
                        activebackground=BORDER, activeforeground=TEXT,
                        bd=0, pady=6, cursor="hand2",
                        command=self._reset)
        btn_reset.pack(fill="x", padx=30)

        self._sep()

        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(fill="both", expand=True, padx=30, pady=0)

        self._placeholder()

    def _sep(self):
        f = tk.Frame(self, bg=BORDER, height=1)
        f.pack(fill="x", padx=30, pady=10)

    def _field(self, parent, label, unit, var, row):
        row_f = tk.Frame(parent, bg=CARD)
        row_f.pack(fill="x", padx=20, pady=8)

        tk.Label(row_f, text=label, font=self.f_small,
                 fg=MUTED, bg=CARD, width=10, anchor="w").pack(side="left")

        entry = tk.Entry(row_f, textvariable=var, font=self.f_input,
                         fg=TEXT, bg=BG, insertbackground=ACCENT,
                         bd=0, highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT,
                         width=10)
        entry.pack(side="left", ipady=6, padx=4)

        tk.Label(row_f, text=unit, font=self.f_small,
                 fg=MUTED, bg=CARD).pack(side="left", padx=4)

    def _sexe_field(self, parent, row):
        row_f = tk.Frame(parent, bg=CARD)
        row_f.pack(fill="x", padx=20, pady=(8, 14))

        tk.Label(row_f, text="SEXE", font=self.f_small,
                 fg=MUTED, bg=CARD, width=10, anchor="w").pack(side="left")

        for val, lbl in [("H", "Homme"), ("F", "Femme")]:
            rb = tk.Radiobutton(row_f, text=lbl, variable=self.sexe_var,
                                value=val, font=self.f_small,
                                fg=TEXT, bg=CARD,
                                activebackground=CARD, activeforeground=ACCENT,
                                selectcolor=BG,
                                indicatoron=0, bd=0,
                                padx=14, pady=5,
                                highlightthickness=0,
                                cursor="hand2",
                                relief="flat",
                                command=self._style_radios)
            rb.pack(side="left", padx=3)
            if not hasattr(self, '_radios'):
                self._radios = []
            self._radios.append((rb, val))
        self._style_radios()

    def _style_radios(self):
        for rb, val in self._radios:
            if self.sexe_var.get() == val:
                rb.config(fg=BG, bg=ACCENT)
            else:
                rb.config(fg=MUTED, bg=BORDER)

    def _placeholder(self):
        for w in self.result_frame.winfo_children():
            w.destroy()
        tk.Label(self.result_frame,
                 text="Remplissez les champs\npuis cliquez Calculer",
                 font=self.f_small, fg=MUTED, bg=BG,
                 justify="center").pack(expand=True)

    def _calculate(self):
        try:
            age    = int(self.age_var.get())
            taille = float(self.taille_var.get())  # cm
            poids  = float(self.poids_var.get())   # kg

            if age <= 0 or taille <= 0 or poids <= 0:
                raise ValueError
            if age > 120 or taille > 250 or poids > 500:
                raise ValueError

        except ValueError:
            self._show_error("Valeurs invalides.\nVérifie tes saisies.")
            return

        taille_m = taille / 100
        imc = poids / (taille_m ** 2)
        cat, color = get_category(imc)

        if self.sexe_var.get() == "H":
            poids_ideal = taille - 100 - (taille - 150) / 4
        else:
            poids_ideal = taille - 100 - (taille - 150) / 2.5

        diff = poids - poids_ideal

        self._show_result(imc, cat, color, poids_ideal, diff, age)

    def _show_result(self, imc, cat, color, poids_ideal, diff, age):
        for w in self.result_frame.winfo_children():
            w.destroy()

        tk.Label(self.result_frame, text=f"{imc:.1f}",
                 font=self.f_imc, fg=color, bg=BG).pack(pady=(10, 0))

        tk.Label(self.result_frame, text="IMC (kg/m²)",
                 font=self.f_small, fg=MUTED, bg=BG).pack()

        badge = tk.Frame(self.result_frame, bg=color)
        badge.pack(pady=8)
        tk.Label(badge, text=f"  {cat.upper()}  ",
                 font=self.f_cat, fg=BG, bg=color).pack(padx=2, pady=4)

        self._draw_scale(imc, color)

        det = tk.Frame(self.result_frame, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
        det.pack(fill="x", pady=8)

        diff_txt = f"+{diff:.1f} kg" if diff > 0 else f"{diff:.1f} kg"
        diff_col = ORANGE if diff > 1 else GREEN

        infos = [
            ("Poids idéal (Lorentz)", f"{poids_ideal:.1f} kg"),
            ("Écart au poids idéal",  diff_txt),
        ]
        if age < 18:
            infos.append(("⚠ Remarque", "IMC indicatif < 18 ans"))

        for k, v in infos:
            row = tk.Frame(det, bg=CARD)
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=k, font=self.f_small,
                     fg=MUTED, bg=CARD, anchor="w").pack(side="left")
            col = diff_col if "Écart" in k else ACCENT2
            tk.Label(row, text=v, font=self.f_small,
                     fg=col, bg=CARD, anchor="e").pack(side="right")

    def _draw_scale(self, imc, color):
        c = tk.Canvas(self.result_frame, bg=BG, highlightthickness=0,
                      height=36, width=440)
        c.pack(pady=4)

        segs = [
            (0,  16,   "#ff6b9d"),
            (16, 18.5, "#ffa502"),
            (18.5,25,  "#00ff88"),
            (25, 30,   "#ffa502"),
            (30, 35,   "#ff6348"),
            (35, 40,   "#ff4757"),
            (40, 50,   "#c0392b"),
        ]
        min_v, max_v = 10, 50
        W = 440

        for lo, hi, col in segs:
            x0 = (lo - min_v) / (max_v - min_v) * W
            x1 = (hi - min_v) / (max_v - min_v) * W
            c.create_rectangle(x0, 14, x1, 26, fill=col, outline="")

        clamp = max(min_v, min(imc, max_v))
        px = (clamp - min_v) / (max_v - min_v) * W
        c.create_polygon(px, 0, px-7, 12, px+7, 12,
                         fill=color, outline=BG, width=1)
        c.create_rectangle(px-2, 12, px+2, 28, fill=color, outline="")
        c.create_text(px, 34, text=f"{imc:.1f}",
                      font=self.f_small, fill=color, anchor="s")

    def _show_error(self, msg):
        for w in self.result_frame.winfo_children():
            w.destroy()
        tk.Label(self.result_frame, text="⚠  ERREUR",
                 font=self.f_cat, fg=RED, bg=BG).pack(pady=(20, 4))
        tk.Label(self.result_frame, text=msg,
                 font=self.f_small, fg=MUTED, bg=BG, justify="center").pack()

    def _reset(self):
        self.age_var.set("")
        self.taille_var.set("")
        self.poids_var.set("")
        self.sexe_var.set("H")
        self._style_radios()
        self._placeholder()

if __name__ == "__main__":
    app = IMCApp()
    app.mainloop()