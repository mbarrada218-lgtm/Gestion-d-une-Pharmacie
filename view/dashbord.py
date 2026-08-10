from tkinter import *
from PIL import Image, ImageTk
from view import medicaments


# =================== VARIABLES GLOBALES ===================
F1 = None
content_frame = None  # ← la frame qui change de contenu

# Couleurs/police gardées en mémoire pour éviter de les repasser
# en paramètre à chaque page (fram_accueil, etc.)
_BG_MAIN = None
_COLOR_ENTRY = None
_COLOR_TEXT = None
_COLOR_BTN = None
_ECRITURE = None
_FONT_TITLE = None
_on_enter = None
_on_leave = None


# =================== CLEAR CONTENT ONLY ===================
def clear_content():
    for w in content_frame.winfo_children():
        w.destroy()


# =================== DASHBOARD ===================
def open_dashboard(root, role, username, BG_MAIN,
                    COLOR_ENTRY, COLOR_TEXT, COLOR_BTN,
                    ECRITURE, FONT_TITLE, on_enter, on_leave):
    
    global F1, content_frame
    global _BG_MAIN, _COLOR_ENTRY, _COLOR_TEXT, _COLOR_BTN, _ECRITURE, _FONT_TITLE, _on_enter, _on_leave

    # on garde le thème en mémoire pour les autres pages du dashboard
    _BG_MAIN, _COLOR_ENTRY, _COLOR_TEXT, _COLOR_BTN = BG_MAIN, COLOR_ENTRY, COLOR_TEXT, COLOR_BTN
    _ECRITURE, _FONT_TITLE, _on_enter, _on_leave = ECRITURE, FONT_TITLE, on_enter, on_leave

    # supprime la page de login
    for w in root.winfo_children():
        w.destroy()

    root.title("TABLEAU DE GESTION DU STOCK PHARM")
    root.geometry("1200x700")
    root.config(bg=BG_MAIN)

    # Sidebar fixe
    F1 = Frame(root, bg=COLOR_TEXT, relief="raised", bd=3)
    F1.place(width=200, height=700)

    Label(F1, text="✚", font=("Bookman old style", 30, "bold"),
          bg=COLOR_TEXT, fg=BG_MAIN).pack(pady=15)
    Label(F1, text="PharmaGest", font=FONT_TITLE,
          bg=COLOR_TEXT, fg=BG_MAIN).pack()

    Frame(F1, height=2, width=150, bg=BG_MAIN).pack(pady=20)

    B1 = Button(F1, text="ACCUEIL ➜]", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2,
                command=fram_accueil)
    B1.pack(pady=10)
    B1.bind("<Enter>", on_enter)
    B1.bind("<Leave>", on_leave)

    B2 = Button(F1, text="MEDICAMENT", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2 , 
                command=lambda:medicaments.medicament(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,ECRITURE, COLOR_BTN
                     ,clear_content ,on_enter,on_leave))
    B2.pack(pady=10)
    B2.bind("<Enter>", on_enter)
    B2.bind("<Leave>", on_leave)

    B3 = Button(F1, text="VENTE", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2)
    B3.pack(pady=10)
    B3.bind("<Enter>", on_enter)
    B3.bind("<Leave>", on_leave)

    B4 = Button(F1, text="STATISTIQUE", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2)
    B4.pack(pady=10)
    B4.bind("<Enter>", on_enter)
    B4.bind("<Leave>", on_leave)

    B5 = Button(F1, text="CREER UN UTILISATEUR", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2)
    B5.pack(pady=10)
    B5.bind("<Enter>", on_enter)
    B5.bind("<Leave>", on_leave)

    B6 = Button(F1, text="QUITTER", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_BTN, width=20, fg=BG_MAIN, relief="raised", height=2,
                command=exit)
    B6.pack(pady=10)
    B6.bind("<Enter>", on_enter)
    B6.bind("<Leave>", on_leave)

    # Content frame fixe — c'est ici que le contenu change
    content_frame = Frame(root, bg=BG_MAIN)
    content_frame.place(x=210, y=0, width=990, height=700)

    Label(F1, text=f"👤 {username}",
          font=("Bookman Old Style", 9, "bold"),
          bg=COLOR_TEXT, fg=BG_MAIN).pack()
    Label(F1, text=f"🔰 {role}",
          font=("Bookman Old Style", 9),
          bg=COLOR_TEXT, fg=BG_MAIN).pack(pady=5)

    fram_accueil()  # ← affichée dès le départ


# =================== PAGES ===================
def fram_accueil():
    clear_content()

    BG_MAIN = _BG_MAIN
    COLOR_TEXT = _COLOR_TEXT
    ECRITURE = _ECRITURE

    # =================== FRAME PHOTO ===================
    F2 = Frame(content_frame, bd=3, relief="raised")
    F2.place(x=580, y=50, width=390, height=485)
    F2.pack_propagate(False)

    original_img = Image.open("img2.png")
    resize_original = original_img.resize((400, 480))
    img_final = ImageTk.PhotoImage(resize_original)
    img_label = Label(F2, image=img_final)
    img_label.image = img_final
    img_label.pack(expand=True)

    # =================== FRAME INFO ===================
    F_info = Frame(content_frame, bg=BG_MAIN)
    F_info.place(x=50, y=50, width=520, height=500)

    # -------- Features & Summary --------
    F_features = Frame(F_info, bg="white", bd=2, relief="sunken")
    F_features.pack(fill="x", pady=5)

    Label(F_features, text="📋 Fonctionnalités & Résumé",
          font=("Bookman Old Style", 11, "bold"),
          bg=COLOR_TEXT, fg="white").pack(fill="x", padx=0, pady=0, ipadx=5, ipady=5)

    row1 = Frame(F_features, bg="white")
    row1.pack(fill="x", padx=10, pady=8)

    Label(row1, text="Valeur Totale du Stock", font=("Bookman Old Style", 9),
          bg="white", fg=ECRITURE, relief="solid", bd=1).pack(side="left", padx=5, ipadx=8, ipady=4)
    Label(row1, text="Métriques Totales", font=("Bookman Old Style", 9),
          bg="white", fg=ECRITURE, relief="solid", bd=1).pack(side="left", padx=5, ipadx=8, ipady=4)

    # Alerts
    F_alert = Frame(F_features, bg="white")
    F_alert.pack(fill="x", padx=10, pady=5)

    Label(F_alert, text="⚠ Alertes", font=("Bookman Old Style", 10, "bold"),
          bg="white", fg=ECRITURE).pack(anchor="w")
    Label(F_alert, text="💊 Vérifiez les dates d'expiration des produits",
          font=("Bookman Old Style", 9), bg="white", fg="red").pack(anchor="w", pady=3)

    # -------- Application Status --------
    F_status = Frame(F_info, bg="white", bd=2, relief="sunken")
    F_status.pack(fill="x", pady=5)

    Label(F_status, text="🖥 Statut de l'Application",
          font=("Bookman Old Style", 11, "bold"),
          bg=COLOR_TEXT, fg="white").pack(fill="x", ipadx=5, ipady=5)

    infos = [
        ("📋 Application", "Gestion de Pharmacie"),
        ("📅 Année",       "2026 / 2027"),
        ("🔢 Version",     "1.0.0"),
        ("✅ Statut",      "Actif"),
    ]

    for label, valeur in infos:
        row = Frame(F_status, bg="white")
        row.pack(fill="x", padx=15, pady=4)
        Label(row, text=label, font=("Bookman Old Style", 9, "bold"),
              bg="white", fg=COLOR_TEXT, width=16, anchor="w").pack(side="left")
        Label(row, text=valeur, font=("Bookman Old Style", 9),
              bg="white", fg=ECRITURE, anchor="w").pack(side="left")

    # -------- User Guidelines --------
    F_guide = Frame(F_info, bg="white", bd=2, relief="sunken")
    F_guide.pack(fill="x", pady=8)

    Label(F_guide, text="📖Guide d'utilisation",
          font=("Bookman Old Style", 11, "bold"),
          bg=COLOR_TEXT, fg="white").pack(fill="x", ipadx=5, ipady=5)

    conseils = [
        "💊 Vérifiez les dates d'expiration régulièrement",
        "📦 Mettez à jour le stock après chaque vente",
        "🔒 Déconnectez-vous après chaque utilisation",
        "📊 Consultez les statistiques pour suivre les ventes",
        "🔔 Signalez tout médicament en rupture de stock",
    ]

    for conseil in conseils:
        Label(F_guide, text=conseil, font=("Bookman Old Style", 9),
              bg="white", fg=ECRITURE).pack(anchor="w", padx=15, pady=4)
