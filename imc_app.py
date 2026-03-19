import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox
import math
import datetime
import json
import os

PROFILS_FILE = "profils_imc.json"

CATEGORIES: tuple = (
    ("Dénutrition",   0.0,  16.0,  "#FF6B9D"),
    ("Maigreur",     16.0,  18.5,  "#FFA552"),
    ("Normal",       18.5,  25.0,  "#3DFFC0"),
    ("Surpoids",     25.0,  30.0,  "#FFA552"),
    ("Obésité I",    30.0,  35.0,  "#FF7043"),
    ("Obésité II",   35.0,  40.0,  "#FF4757"),
    ("Obésité III",  40.0, 999.0,  "#C0392B"),
)

JOURS_SEMAINE: list = ["Lundi","Mardi","Mercredi","Jeudi",
                       "Vendredi","Samedi","Dimanche"]

THEME: dict = {
    "bg":      "#0A0E1A",
    "panel":   "#0F1623",
    "card":    "#141C2E",
    "card2":   "#1A2338",
    "border":  "#1E2D47",
    "border2": "#253554",
    "accent":  "#3DFFC0",
    "accent2": "#38BDF8",
    "accent3": "#818CF8",
    "red":     "#FF4757",
    "text":    "#E8EDF5",
    "muted":   "#4A5568",
    "muted2":  "#64748B",
    "success": "#3DFFC0",
    "warning": "#FFA552",
    "danger":  "#FF4757",
}


def charger_profils() -> dict:
    """Charge les profils depuis le fichier JSON."""
    if os.path.exists(PROFILS_FILE):
        with open(PROFILS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def sauvegarder_profils(profils: dict) -> None:
    """Sauvegarde les profils dans le fichier JSON."""
    with open(PROFILS_FILE, "w", encoding="utf-8") as f:
        json.dump(profils, f, ensure_ascii=False, indent=2)


def sauvegarder_profil(nom: str, data: dict) -> None:
    """Sauvegarde ou met à jour un profil."""
    profils = charger_profils()
    data["derniere_maj"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    profils[nom] = data
    sauvegarder_profils(profils)


def supprimer_profil(nom: str) -> None:
    """Supprime un profil."""
    profils = charger_profils()
    if nom in profils:
        del profils[nom]
        sauvegarder_profils(profils)


def valider_age(age: int) -> tuple:
    """
    Vérifie que l'âge est dans la plage valide pour l'IMC (18-65).
    Retourne (valide: bool, message: str)
    """
    if age < 18:
        return False, (f"Tu as {age} ans — la formule IMC n'est pas\n"
                       f"applicable avant 18 ans. Pour les mineurs,\n"
                       f"un médecin utilise des courbes de croissance.")
    if age > 65:
        return False, (f"Tu as {age} ans — la formule IMC n'est pas\n"
                       f"fiable après 65 ans (masse musculaire réduite).\n"
                       f"Consulte un professionnel de santé.")
    return True, ""


def calculer_imc(poids: float, taille_cm: float) -> float:
    """Calcule l'IMC (Q23)."""
    taille_m = taille_cm / 100
    return poids / (taille_m ** 2)


def get_categorie(imc: float) -> tuple:
    """Retourne (label, couleur) — Q19+Q20."""
    for label, lo, hi, couleur in CATEGORIES:
        if lo <= imc < hi:
            return label, couleur
    return "Obésité III", "#C0392B"


def calculer_poids_ideal(taille_cm: float, sexe: str) -> float:
    """Formule de Lorentz (Q28)."""
    if sexe == "H":
        return taille_cm - 100 - (taille_cm - 150) / 4
    else:
        return taille_cm - 100 - (taille_cm - 150) / 2.5


def calculer_objectif(poids: float, taille_cm: float, sexe: str) -> dict:
    """
    Calcule combien de kg prendre/perdre pour être en zone normale.
    Retourne un dict avec les infos d'objectif.
    """
    imc_actuel   = calculer_imc(poids, taille_cm)
    poids_ideal  = calculer_poids_ideal(taille_cm, sexe)
    taille_m     = taille_cm / 100

    poids_min_normal = 18.5 * (taille_m ** 2)
    poids_max_normal = 25.0 * (taille_m ** 2)

    diff_ideal = poids - poids_ideal
    diff_min   = poids - poids_min_normal
    diff_max   = poids - poids_max_normal

    return {
        "imc":              imc_actuel,
        "poids_ideal":      poids_ideal,
        "poids_min_normal": poids_min_normal,
        "poids_max_normal": poids_max_normal,
        "diff_ideal":       diff_ideal,
        "diff_min":         diff_min,
        "diff_max":         diff_max,
    }


def calculer_annee_naissance(age: int) -> int:
    """Q36 : datetime dynamique."""
    return datetime.datetime.now().year - age


def construire_rapport(infos: dict) -> list:
    """Q11/Q12/Q26/Q31/Q32/Q33."""
    imc   = infos["imc"]
    poids = infos["poids"]
    imc_arrondis: list = [round(imc, n) for n in range(0, 3)]

    rapport: list = [
        ("IMC calculé",           f"{imc:.2f} kg/m²"),
        ("Compréhension [0,1,2]", str(imc_arrondis)),
        ("math.sqrt(poids)",      f"{math.sqrt(poids):.3f}"),
        ("math.pi",               str(round(math.pi, 5))),
        ("Année de naissance",    str(calculer_annee_naissance(infos["age"]))),
    ]
    return rapport



class IMCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TP002 — Calculateur IMC")
        self.geometry("600x860")
        self.resizable(False, False)
        self.configure(bg=THEME["bg"])

        self.F = {
            "title": tkfont.Font(family="Courier New", size=15, weight="bold"),
            "sub":   tkfont.Font(family="Courier New", size=8),
            "label": tkfont.Font(family="Courier New", size=8, weight="bold"),
            "input": tkfont.Font(family="Courier New", size=12),
            "big":   tkfont.Font(family="Courier New", size=42, weight="bold"),
            "cat":   tkfont.Font(family="Courier New", size=12, weight="bold"),
            "small": tkfont.Font(family="Courier New", size=8),
            "btn":   tkfont.Font(family="Courier New", size=10, weight="bold"),
            "mono":  tkfont.Font(family="Courier New", size=9),
            "tag":   tkfont.Font(family="Courier New", size=7, weight="bold"),
            "obj":   tkfont.Font(family="Courier New", size=10, weight="bold"),
        }

        self.v_nom    = tk.StringVar()
        self.v_age    = tk.StringVar()
        self.v_taille = tk.StringVar()
        self.v_poids  = tk.StringVar()
        self.v_sexe   = tk.StringVar(value="H")
        self.v_profil = tk.StringVar()  

        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=THEME["bg"])
        hdr.pack(fill="x", padx=28, pady=(20, 0))

        lh = tk.Frame(hdr, bg=THEME["bg"])
        lh.pack(side="left")
        pill = tk.Frame(lh, bg=THEME["accent3"])
        pill.pack(anchor="w", pady=(0,5))
        tk.Label(pill, text=" TP002  PROJET FINAL ",
                 font=self.F["tag"], fg=THEME["bg"],
                 bg=THEME["accent3"]).pack(padx=2, pady=2)
        tk.Label(lh, text="CALCULATEUR IMC",
                 font=self.F["title"], fg=THEME["text"],
                 bg=THEME["bg"]).pack(anchor="w")
        tk.Label(lh, text="Statistiques personnelles  Python 3",
                 font=self.F["sub"], fg=THEME["muted2"],
                 bg=THEME["bg"]).pack(anchor="w")

        rh = tk.Frame(hdr, bg=THEME["bg"])
        rh.pack(side="right", anchor="ne")
        tk.Label(rh, text=datetime.datetime.now().strftime("%d %b %Y  %H:%M"),
                 font=self.F["sub"], fg=THEME["accent2"],
                 bg=THEME["bg"]).pack(anchor="e")
        tk.Label(rh, text=f"pi = {math.pi:.4f}",
                 font=self.F["sub"], fg=THEME["muted"],
                 bg=THEME["bg"]).pack(anchor="e")

        tk.Frame(self, bg=THEME["accent"], height=1).pack(fill="x", padx=28, pady=(12,0))
        tk.Frame(self, bg=THEME["border"], height=1).pack(fill="x", padx=28, pady=(1,0))

        body = tk.Frame(self, bg=THEME["bg"])
        body.pack(fill="both", expand=True, padx=28, pady=8)

        self._section_label(body, "GESTION DES PROFILS", "json — sauvegarde locale")
        prof_card = self._card(body)
        self._build_profil_section(prof_card)

        self._section_label(body, "IDENTITÉ & MESURES", "Q2 Q3 Q4 Q23 Q28 Q36")
        form_card = self._card(body)
        self._row2(form_card,
                   ("NOM",    self.v_nom,    "texte"),
                   ("AGE",    self.v_age,    "ans"))
        self._row2(form_card,
                   ("TAILLE", self.v_taille, "cm"),
                   ("POIDS",  self.v_poids,  "kg"))

        sx_f = tk.Frame(form_card, bg=THEME["card"])
        sx_f.pack(fill="x", padx=16, pady=(4, 14))
        tk.Label(sx_f, text="SEXE", font=self.F["small"],
                 fg=THEME["muted"], bg=THEME["card"],
                 width=8, anchor="w").pack(side="left")
        self._radios = []
        for val, lbl in [("H","  Homme  "), ("F","  Femme  ")]:
            rb = tk.Radiobutton(sx_f, text=lbl, variable=self.v_sexe,
                                value=val, font=self.F["small"],
                                fg=THEME["muted"], bg=THEME["border"],
                                activebackground=THEME["card"],
                                selectcolor=THEME["bg"],
                                indicatoron=0, bd=0,
                                padx=4, pady=5,
                                highlightthickness=0,
                                cursor="hand2", relief="flat",
                                command=self._style_radios)
            rb.pack(side="left", padx=(0,6))
            self._radios.append((rb, val))
        self._style_radios()

        btn_row = tk.Frame(body, bg=THEME["bg"])
        btn_row.pack(fill="x", pady=(10, 0))

        tk.Button(btn_row, text="  CALCULER",
                  font=self.F["btn"],
                  fg=THEME["bg"], bg=THEME["accent"],
                  activebackground="#2DE8A8",
                  activeforeground=THEME["bg"],
                  bd=0, pady=12, cursor="hand2",
                  command=self._calculate).pack(side="left", fill="x",
                                                expand=True, padx=(0,4))

        tk.Button(btn_row, text="SAUVEGARDER",
                  font=self.F["btn"],
                  fg=THEME["bg"], bg=THEME["accent2"],
                  activebackground="#5BC8F5",
                  activeforeground=THEME["bg"],
                  bd=0, pady=12, cursor="hand2",
                  command=self._save_profil).pack(side="left", fill="x",
                                                   expand=True, padx=(0,4))

        tk.Button(btn_row, text="Reset",
                  font=self.F["small"],
                  fg=THEME["muted2"], bg=THEME["card"],
                  activebackground=THEME["border"],
                  bd=0, pady=12, cursor="hand2",
                  width=7,
                  command=self._reset).pack(side="right")

        tk.Frame(body, bg=THEME["border"], height=1).pack(fill="x", pady=(10,4))
        self.res_frame = tk.Frame(body, bg=THEME["bg"])
        self.res_frame.pack(fill="both", expand=True)
        self._placeholder()

    def _build_profil_section(self, parent):
        row = tk.Frame(parent, bg=THEME["card"])
        row.pack(fill="x", padx=16, pady=12)

        tk.Label(row, text="PROFIL", font=self.F["tag"],
                 fg=THEME["muted2"], bg=THEME["card"]).pack(side="left",
                                                             padx=(0,10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TCombobox",
                        fieldbackground=THEME["bg"],
                        background=THEME["bg"],
                        foreground=THEME["text"],
                        bordercolor=THEME["border2"],
                        arrowcolor=THEME["accent"],
                        selectbackground=THEME["card"],
                        selectforeground=THEME["text"])

        self.combo = ttk.Combobox(row, textvariable=self.v_profil,
                                  font=self.F["mono"],
                                  style="Dark.TCombobox",
                                  state="readonly", width=22)
        self.combo.pack(side="left", ipady=5, padx=(0, 8))
        self.combo.bind("<<ComboboxSelected>>", self._load_profil)
        self._refresh_combo()

        tk.Button(row, text="Charger",
                  font=self.F["small"],
                  fg=THEME["bg"], bg=THEME["accent3"],
                  activebackground="#9DA8FF",
                  activeforeground=THEME["bg"],
                  bd=0, padx=10, pady=5,
                  cursor="hand2",
                  command=self._load_profil).pack(side="left", padx=(0,4))

        tk.Button(row, text="Supprimer",
                  font=self.F["small"],
                  fg=THEME["text"], bg=THEME["danger"],
                  activebackground="#FF6B6B",
                  activeforeground=THEME["text"],
                  bd=0, padx=10, pady=5,
                  cursor="hand2",
                  command=self._delete_profil).pack(side="left")

        self.lbl_count = tk.Label(row, text="",
                                  font=self.F["small"],
                                  fg=THEME["muted"], bg=THEME["card"])
        self.lbl_count.pack(side="right")
        self._update_count()

    def _refresh_combo(self):
        profils = charger_profils()
        noms    = list(profils.keys())
        self.combo["values"] = noms
        if noms and not self.v_profil.get():
            self.combo.current(0)

    def _update_count(self):
        n = len(charger_profils())
        self.lbl_count.config(text=f"{n} profil(s)")

    def _load_profil(self, event=None):
        nom = self.v_profil.get()
        if not nom:
            return
        profils = charger_profils()
        if nom not in profils:
            return
        d = profils[nom]
        self.v_nom.set(d.get("nom", nom))
        self.v_age.set(str(d.get("age", "")))
        self.v_taille.set(str(d.get("taille", "")))
        self.v_poids.set(str(d.get("poids", "")))
        self.v_sexe.set(d.get("sexe", "H"))
        self._style_radios()

    def _save_profil(self):
        nom = self.v_nom.get().strip()
        if not nom:
            messagebox.showwarning("Sauvegarde",
                                   "Entre un nom avant de sauvegarder.",
                                   parent=self)
            return
        try:
            age    = int(self.v_age.get())
            taille = float(self.v_taille.get())
            poids  = float(self.v_poids.get())
        except ValueError:
            messagebox.showwarning("Sauvegarde",
                                   "Remplis toutes les mesures avant de sauvegarder.",
                                   parent=self)
            return

        data = {
            "nom":    nom,
            "age":    age,
            "taille": taille,
            "poids":  poids,
            "sexe":   self.v_sexe.get(),
        }
        sauvegarder_profil(nom, data)
        self._refresh_combo()
        self._update_count()
        self.v_profil.set(nom)
        messagebox.showinfo("Sauvegarde",
                            f"Profil « {nom} » sauvegardé !",
                            parent=self)

    def _delete_profil(self):
        nom = self.v_profil.get()
        if not nom:
            return
        ok = messagebox.askyesno("Supprimer",
                                  f"Supprimer le profil « {nom} » ?",
                                  parent=self)
        if ok:
            supprimer_profil(nom)
            self.v_profil.set("")
            self._refresh_combo()
            self._update_count()

    def _section_label(self, parent, title, hint=""):
        f = tk.Frame(parent, bg=THEME["bg"])
        f.pack(fill="x", pady=(12,5))
        tk.Label(f, text=title, font=self.F["label"],
                 fg=THEME["accent2"], bg=THEME["bg"]).pack(side="left")
        if hint:
            tk.Label(f, text=f"   {hint}", font=self.F["sub"],
                     fg=THEME["muted"], bg=THEME["bg"]).pack(side="left")

    def _card(self, parent):
        c = tk.Frame(parent, bg=THEME["card"],
                     highlightbackground=THEME["border"],
                     highlightthickness=1)
        c.pack(fill="x", pady=2)
        return c

    def _row2(self, parent, left, right=None):
        row = tk.Frame(parent, bg=THEME["card"])
        row.pack(fill="x", padx=16, pady=8)
        self._entry_field(row, *left)
        if right:
            tk.Frame(row, bg=THEME["border"], width=1).pack(
                side="left", fill="y", padx=14)
            self._entry_field(row, *right)

    def _entry_field(self, parent, label, var, unit):
        f = tk.Frame(parent, bg=THEME["card"])
        f.pack(side="left", fill="x", expand=True)
        tk.Label(f, text=label, font=self.F["tag"],
                 fg=THEME["muted2"], bg=THEME["card"]).pack(anchor="w", pady=(0,3))
        ef = tk.Frame(f, bg=THEME["bg"],
                      highlightbackground=THEME["border2"],
                      highlightthickness=1)
        ef.pack(fill="x")
        e = tk.Entry(ef, textvariable=var, font=self.F["input"],
                     fg=THEME["text"], bg=THEME["bg"],
                     insertbackground=THEME["accent"],
                     bd=0, width=10)
        e.pack(side="left", ipady=8, padx=(10,4))
        tk.Label(ef, text=unit, font=self.F["small"],
                 fg=THEME["muted"], bg=THEME["bg"]).pack(side="right", padx=8)
        e.bind("<FocusIn>",  lambda ev, w=ef:
               w.config(highlightbackground=THEME["accent"]))
        e.bind("<FocusOut>", lambda ev, w=ef:
               w.config(highlightbackground=THEME["border2"]))

    def _style_radios(self):
        for rb, val in self._radios:
            if self.v_sexe.get() == val:
                rb.config(fg=THEME["bg"], bg=THEME["accent"])
            else:
                rb.config(fg=THEME["muted"], bg=THEME["border"])

    def _placeholder(self):
        for w in self.res_frame.winfo_children():
            w.destroy()
        ph = tk.Frame(self.res_frame, bg=THEME["panel"],
                      highlightbackground=THEME["border"],
                      highlightthickness=1)
        ph.pack(fill="x", pady=4)
        tk.Label(ph, text="Remplis les champs puis clique CALCULER",
                 font=self.F["small"], fg=THEME["muted"],
                 bg=THEME["panel"]).pack(pady=18)

    def _calculate(self):
        try:
            nom    = self.v_nom.get().strip() or "Etudiant"
            age    = int(self.v_age.get())
            taille = float(self.v_taille.get())
            poids  = float(self.v_poids.get())
            sexe   = self.v_sexe.get()
            if taille <= 0 or poids <= 0:
                raise ValueError
        except ValueError:
            self._show_error("Valeurs invalides !\nVérifie tes saisies.")
            return

        age_ok, age_msg = valider_age(age)
        if not age_ok:
            self._show_age_warning(age_msg, age)
            return

        imc      = calculer_imc(poids, taille)
        cat, col = get_categorie(imc)
        obj      = calculer_objectif(poids, taille, sexe)

        infos: dict = {
            "nom": nom, "age": age,
            "taille": taille, "poids": poids,
            "sexe": sexe, "imc": imc,
        }
        rapport = construire_rapport(infos)
        self._show_result(infos, cat, col, obj, rapport)

    def _show_result(self, infos, cat, col, obj, rapport):
        for w in self.res_frame.winfo_children():
            w.destroy()

        imc  = infos["imc"]
        nom  = infos["nom"]
        age  = infos["age"]

        annee_n = calculer_annee_naissance(age)
        msg_card = tk.Frame(self.res_frame, bg=THEME["card"],
                            highlightbackground=col, highlightthickness=1)
        msg_card.pack(fill="x", pady=(0,8))
        inner = tk.Frame(msg_card, bg=THEME["card"])
        inner.pack(fill="x", padx=14, pady=8)
        tk.Label(inner, text="*", font=self.F["mono"],
                 fg=col, bg=THEME["card"]).pack(side="left", anchor="n",
                                                padx=(0,8))
        tf = tk.Frame(inner, bg=THEME["card"])
        tf.pack(side="left")
        tk.Label(tf, text=f"Bonjour {nom}, {age} ans",
                 font=self.F["mono"], fg=THEME["text"],
                 bg=THEME["card"]).pack(anchor="w")
        tk.Label(tf, text=f"Né(e) en {annee_n}",
                 font=self.F["small"], fg=THEME["muted2"],
                 bg=THEME["card"]).pack(anchor="w")

        top = tk.Frame(self.res_frame, bg=THEME["bg"])
        top.pack(fill="x")

        tk.Label(top, text=f"{imc:.1f}",
                 font=self.F["big"], fg=col,
                 bg=THEME["bg"]).pack(side="left", anchor="s")
        tk.Label(top, text=" kg/m²",
                 font=self.F["sub"], fg=THEME["muted"],
                 bg=THEME["bg"]).pack(side="left", anchor="s", pady=(0,10))

        rt = tk.Frame(top, bg=THEME["bg"])
        rt.pack(side="right", anchor="ne", pady=8)
        badge = tk.Frame(rt, bg=col)
        badge.pack(anchor="e")
        tk.Label(badge, text=f"  {cat.upper()}  ",
                 font=self.F["cat"], fg=THEME["bg"],
                 bg=col).pack(padx=6, pady=6)

        self._draw_scale(imc, col)

        self._build_objectif(obj, col)

        self._section_label(self.res_frame,
                            "RAPPORT PEDAGOGIQUE", "notions TP002")
        rep_f = tk.Frame(self.res_frame, bg=THEME["card"],
                         highlightbackground=THEME["border"],
                         highlightthickness=1)
        rep_f.pack(fill="x")

        for i, (label, valeur) in enumerate(rapport):
            bg = THEME["card"] if i % 2 == 0 else THEME["card2"]
            row = tk.Frame(rep_f, bg=bg)
            row.pack(fill="x")
            tk.Label(row, text=f"  {label}",
                     font=self.F["mono"], fg=THEME["muted2"],
                     bg=bg, anchor="w", width=26).pack(side="left", ipady=4)
            tk.Label(row, text=f"{valeur}  ",
                     font=self.F["mono"], fg=THEME["accent"],
                     bg=bg, anchor="e").pack(side="right", ipady=4)

        jours_pairs: list = [j for i, j in enumerate(JOURS_SEMAINE)
                             if i % 2 == 0]
        footer = tk.Frame(rep_f, bg=THEME["panel"])
        footer.pack(fill="x")
        tk.Label(footer,
                 text=f"  [Q25] filtre jours pairs  {jours_pairs}",
                 font=self.F["small"], fg=THEME["muted"],
                 bg=THEME["panel"], anchor="w").pack(anchor="w", padx=4, pady=5)

    def _build_objectif(self, obj, col):
        """Section 'Objectif poids' — combien prendre/perdre."""
        self._section_label(self.res_frame, "OBJECTIF POIDS",
                            "zone normale IMC 18.5 - 25")
        obj_f = tk.Frame(self.res_frame, bg=THEME["card"],
                         highlightbackground=THEME["border"],
                         highlightthickness=1)
        obj_f.pack(fill="x", pady=2)

        diff_ideal = obj["diff_ideal"]
        diff_min   = obj["diff_min"]
        diff_max   = obj["diff_max"]
        pi         = obj["poids_ideal"]
        pmin       = obj["poids_min_normal"]
        pmax       = obj["poids_max_normal"]
        imc        = obj["imc"]

        # Message principal
        if 18.5 <= imc < 25:
            msg      = "Tu es dans la zone normale !"
            msg_col  = THEME["success"]
            detail   = (f"Maintiens ton poids entre {pmin:.1f} kg et {pmax:.1f} kg.")
        elif imc < 18.5:
            kg_manquants = abs(diff_min)
            msg      = f"Prendre {kg_manquants:.1f} kg pour atteindre la zone normale"
            msg_col  = THEME["warning"]
            detail   = (f"Poids idéal (Lorentz) : {pi:.1f} kg\n"
                        f"Zone normale : {pmin:.1f} — {pmax:.1f} kg")
        else:
            kg_perdre = diff_max
            msg      = f"Perdre {kg_perdre:.1f} kg pour atteindre la zone normale"
            msg_col  = THEME["warning"]
            detail   = (f"Poids idéal (Lorentz) : {pi:.1f} kg\n"
                        f"Zone normale : {pmin:.1f} — {pmax:.1f} kg")

        inner = tk.Frame(obj_f, bg=THEME["card"])
        inner.pack(fill="x", padx=14, pady=10)

        # Icône + message
        icon_col = THEME["success"] if 18.5 <= imc < 25 else THEME["warning"]
        icon     = "✓" if 18.5 <= imc < 25 else "→"
        tk.Label(inner, text=icon, font=self.F["obj"],
                 fg=icon_col, bg=THEME["card"]).pack(side="left",
                                                      anchor="n", padx=(0,10))
        tf = tk.Frame(inner, bg=THEME["card"])
        tf.pack(side="left", fill="x", expand=True)
        tk.Label(tf, text=msg, font=self.F["obj"],
                 fg=msg_col, bg=THEME["card"],
                 anchor="w").pack(anchor="w")
        tk.Label(tf, text=detail, font=self.F["small"],
                 fg=THEME["muted2"], bg=THEME["card"],
                 anchor="w", justify="left").pack(anchor="w")

        # Ligne ecart ideal
        tk.Frame(obj_f, bg=THEME["border"], height=1).pack(
            fill="x", padx=14)
        bot = tk.Frame(obj_f, bg=THEME["card2"])
        bot.pack(fill="x", padx=0, pady=0)
        diff_txt = f"{diff_ideal:+.1f} kg vs poids idéal Lorentz"
        diff_col = THEME["muted2"]
        tk.Label(bot, text=f"  {diff_txt}",
                 font=self.F["small"], fg=diff_col,
                 bg=THEME["card2"]).pack(anchor="w", pady=5)

    def _draw_scale(self, imc, color):
        W  = 540
        cv = tk.Canvas(self.res_frame, bg=THEME["bg"],
                       highlightthickness=0, height=46, width=W)
        cv.pack(pady=4)
        min_v, max_v = 10, 50

        for label, lo, hi, col in CATEGORIES:
            x0 = (max(lo, min_v) - min_v) / (max_v - min_v) * W
            x1 = (min(hi, max_v) - min_v) / (max_v - min_v) * W
            cv.create_rectangle(x0, 20, x1-1, 34, fill=col, outline="")

        clamp = max(min_v, min(imc, max_v))
        px    = (clamp - min_v) / (max_v - min_v) * W
        cv.create_polygon(px, 4, px-8, 18, px+8, 18,
                          fill=color, outline=THEME["bg"], width=1)
        cv.create_rectangle(px-2, 18, px+2, 36, fill=color, outline="")
        cv.create_text(px, 44, text=f"{imc:.1f}",
                       font=self.F["small"], fill=color, anchor="s")
        cv.create_text(0,  44, text="10",
                       font=self.F["small"], fill=THEME["muted"], anchor="sw")
        cv.create_text(W,  44, text="50+",
                       font=self.F["small"], fill=THEME["muted"], anchor="se")

    def _show_age_warning(self, msg, age):
        """Affiche un message d'avertissement si l'âge est hors plage 18-65."""
        for w in self.res_frame.winfo_children():
            w.destroy()

        warn = tk.Frame(self.res_frame, bg=THEME["card"],
                        highlightbackground=THEME["warning"],
                        highlightthickness=2)
        warn.pack(fill="x", pady=4)

        top_w = tk.Frame(warn, bg=THEME["card"])
        top_w.pack(fill="x", padx=16, pady=(14,6))
        tk.Label(top_w, text="⚠", font=self.F["cat"],
                 fg=THEME["warning"], bg=THEME["card"]).pack(side="left",
                                                              padx=(0,10))
        tk.Label(top_w, text="FORMULE IMC NON APPLICABLE",
                 font=self.F["cat"], fg=THEME["warning"],
                 bg=THEME["card"]).pack(side="left")

        tk.Frame(warn, bg=THEME["border"], height=1).pack(fill="x", padx=16)

        tk.Label(warn, text=msg,
                 font=self.F["mono"], fg=THEME["text"],
                 bg=THEME["card"], justify="left").pack(
                     anchor="w", padx=24, pady=(10,4))

        note = ("La formule IMC (poids / taille²) est calibrée\n"
                "pour les adultes de 18 à 65 ans uniquement.")
        tk.Label(warn, text=note,
                 font=self.F["small"], fg=THEME["muted2"],
                 bg=THEME["card"], justify="left").pack(
                     anchor="w", padx=24, pady=(0,14))

    def _show_error(self, msg):
        for w in self.res_frame.winfo_children():
            w.destroy()
        err = tk.Frame(self.res_frame, bg=THEME["card"],
                       highlightbackground=THEME["danger"],
                       highlightthickness=1)
        err.pack(fill="x", pady=4)
        tk.Label(err, text="ERREUR DE SAISIE",
                 font=self.F["cat"], fg=THEME["danger"],
                 bg=THEME["card"]).pack(pady=(14,4))
        tk.Label(err, text=msg, font=self.F["mono"],
                 fg=THEME["muted"], bg=THEME["card"],
                 justify="center").pack(pady=(0,14))

    def _reset(self):
        for v in (self.v_nom, self.v_age, self.v_taille, self.v_poids):
            v.set("")
        self.v_sexe.set("H")
        self.v_profil.set("")
        self._style_radios()
        self._placeholder()


if __name__ == "__main__":
    print("Bonjour, monde !")
    print(f"Pi = {math.pi:.5f}")
    app = IMCApp()
    app.mainloop()