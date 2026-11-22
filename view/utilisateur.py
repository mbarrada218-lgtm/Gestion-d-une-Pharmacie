import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from controleur.controlleur_login import (enregistre_les_donnees, creation_utilisateur,
                                          modifie_utilisateur, supprime_utilisateur)

Font_texte = ("Bookman Old Style", 11, "bold")

def utilisateur(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY, ECRITURE, COLOR_BTN,
                clear_content, on_enter, on_leave):
    clear_content()

    F1 = Frame(content_frame, bd=3, relief="groove", bg=BG_MAIN)
    F1.place(y=10, width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES UTILISATEURS ", font=("Bookman old style", 18, "bold"),
                  width=110, height=3, bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    Label(F1, text="Nom de Utilisateur ", font=Font_texte, bg=BG_MAIN).place(x=35, y=110)
    util_input = Entry(F1, font=Font_texte, highlightbackground="#5B9E96", highlightthickness=2)
    util_input.place(x=240, y=110, height=30)

    Label(F1, text="Mot de passe", font=Font_texte, bg=BG_MAIN).place(x=50, y=165)
    password = Entry(F1, font=Font_texte, highlightbackground="#5B9E96", highlightthickness=2, show="*")
    password.place(x=240, y=165, height=30)

    Label(F1, text="Confirmer le Mot de passe ", font=Font_texte, bg=BG_MAIN).place(x=1, y=220)
    conf_password = Entry(F1, font=Font_texte, highlightbackground="#5B9E96", highlightthickness=2, show="*")
    conf_password.place(x=240, y=220, height=30)

    Label(F1, text="Rôle de l'Utilisateur ", font=Font_texte, bg=BG_MAIN).place(x=30, y=278)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", font=("Bookman old style", 11),
                    background=COLOR_ENTRY, foreground=ECRITURE, arrowcolor=ECRITURE,
                    relief="groove", borderwidth=2)
    style.map("TCombobox", fieldbackground=[("readonly", COLOR_ENTRY)],
              foreground=[("readonly", ECRITURE)])
    style.configure("Treeview.Heading", font=("Bookman Old Style", 8, "bold"), background=BG_MAIN)
    style.configure("Treeview", font=("Bookman old style", 8), background=BG_MAIN)

    liste_roles = ["Admin", "Utilisateur"]

    les_choix = ttk.Combobox(F1, values=liste_roles, font=("Bookman old style", 11),
                             state="readonly", width=20)
    les_choix.place(x=240, y=278, height=30)
    les_choix.option_add("*TCombobox*Listbox.font", ("Bookman old style", 11))
    les_choix.option_add("*TCombobox*Listbox.background", COLOR_ENTRY)
    les_choix.option_add("*TCombobox*Listbox.foreground", ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectBackground", ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectForeground", COLOR_ENTRY)
    les_choix.current(0)

    F2 = Frame(F1, width=450, height=200, relief="groove", border=5)
    F2.place(x=480, y=110)
    original_img = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "img3.png"))
    resize_original = original_img.resize((400, 190))
    img_final = ImageTk.PhotoImage(resize_original)
    img_label = Label(F2, image=img_final)
    img_label.image = img_final
    img_label.pack(expand=True)

    F3 = Frame(F1, width=800, height=260, bg=BG_MAIN)
    F3.place(x=70, y=360)

    treeview = ttk.Treeview(F3, columns=(1, 2, 3, 4), height=11, show="headings", style="Treeview")

    sc = ttk.Scrollbar(F3, orient="vertical", command=treeview.yview)
    sc.place(x=775, y=5, height=248)
    treeview.config(yscrollcommand=sc.set)

    treeview.heading(1, text="N°")
    treeview.heading(2, text="Nom de Utilisateur ")
    treeview.heading(3, text="Mot de passe")
    treeview.heading(4, text="Rôle de l'Utilisateur")

    treeview.column(1, width=50)
    treeview.column(2, width=180)
    treeview.column(3, width=180)
    treeview.column(4, width=180)
    treeview.place(x=180, y=5)

    wb, ws = creation_utilisateur(treeview)

    btn_ajout = Button(F1, text="AJOUTER", fg=BG_MAIN, bg=COLOR_BTN, font=Font_texte,
                       command=lambda: enregistre_les_donnees(treeview, util_input, password,
                                                              conf_password, les_choix, ws, wb),
                       width=15, height=1)
    btn_ajout.place(x=70, y=370)
    btn_ajout.bind("<Enter>", on_enter)
    btn_ajout.bind("<Leave>", on_leave)

    btn_modifier = Button(F1, text="MODIFIER", fg=BG_MAIN, bg=COLOR_BTN, font=Font_texte,
                          command=lambda: modifie_utilisateur(treeview, util_input, password,
                                                              les_choix, wb),
                          width=15, height=1)
    btn_modifier.place(x=70, y=420)
    btn_modifier.bind("<Enter>", on_enter)
    btn_modifier.bind("<Leave>", on_leave)

    btn_sup = Button(F1, text="SUPPRIMER", fg=BG_MAIN, bg=COLOR_BTN, font=Font_texte,
                     command=lambda: supprime_utilisateur(treeview, ws, wb),
                     width=15, height=1)
    btn_sup.place(x=70, y=470)
    btn_sup.bind("<Enter>", on_enter)
    btn_sup.bind("<Leave>", on_leave)
